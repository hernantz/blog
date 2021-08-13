Title: De-normalize with Firestore sub-collections for fun and profit
Date: 2020-12-08
Summary: Can subcollections help denormalization be a not so terrible idea?
Category: Programming
Tags: database, firebase, denormalization

[Firestore][0] (by Firebase) is a No-SQL JSON database (as a service) created with the premise of scaling horizontally, allowing concurrent updates to documents and even offline support for client apps, something traditional SQL backends cannot do without a good amount of optimization or [thoughtful design][1].

In this new world of No-SQL, some things you learned for SQL must be unlearned. One of the most important difference is that de-normalizing data is ok.


## When is denormalization a not so terrible idea?

It is a very common pattern to see that data is more often read that written. So optimizing for this case is a sensible thing to do.

This is why Firestore behaves like a giant cache of JSON documents that have been modeled to be consumed as is, like a cached REST API reponse.

Serving pre-computed or aggregated data is generally less expensive, a stack every booming startup needs to model to not blow their SQL database, usually with Memcached or Redis. In Firestore rule still applies, since you are billed for every document access.

## De-normalizing client side.

Another way to think about Firestore is as a big FUSE filesystem of JSON documents that checks access rules for accessing a file or modifying a document and triggers callbacks for every update/create/delete action.

Access rules are created using a [limited language][2] (for the sake of scalability) that only allows you to check the who and the what changes are being affected in a given document.

Say you have a collection of posts and you need to add the "liked by" feature ♥. Any client should only be able to add the current user as a new like, but not modify anything else in the document.

Example document in the `/posts/` collection:

```json
{
	"author": "jeff123",
	"title": "Like my post?",
	"likedBy": ["userABC", "jane_doe"]
}
```

Posts can only be written by the author.

```c
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /posts/{postId} {
      	allow write: if (request.auth.uid != null) && (request.resource.author == request.auth.uid);
		allow read;
	}
  }
}
```

How can we check that the `likedBy` list is written in a way that only the current logged in user adds himself as a new like? What if the user removes the like?

Sure we can start with an attempt that looks like this:

```js
function likedByIsCorrect () {
	let changedKeys = request.resource.data.diff(resource.data).affectedKeys();
	let likedByChanged = "likedBy" in changedKeys;
	let onlyLikedByChanged = changedKeys.hasOnly(["likedBy"]);
	let newLikedBy = request.resource.likedBy.toSet();
	let oldLikedBy = resource.likedBy.toSet();
	let change = newLikedBy.difference(oldLikedBy);
	let onlyCurrentUserChanged = request.auth.uid in change;
	return !likedByChanged || (likedByChanged && onlyCurrentUserChanged);
}
```

And update the rules to:

```c
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /posts/{postId} {

		function likedByIsCorrect () { ... }

      	allow write: if (request.auth.uid != null) && (request.resource.author == request.auth.uid) || likedByIsCorrect();

		allow read;
	}
  }
}
```

This is just to check that:

1. The author can change anything.
2. Other users can only change the `likedBy` list.
3. The only allowed change in the `likedBy` list is to add/remove yourself from the list.

This is too verbose and error prone! Imagine if we also had to add a timestamp to the `likedBy` list:

```json
{
	"likedBy": [
		{
			"user": "userABC",
			"timestamp": "2010-11-12T13:14:15Z"
		}
	]
}
```

Or a new `likesCount`, where we would need to check this counter stays in sync with the like action... More diffs to check, and more headaches!

## De-normalizing with sub-collections

Manipulating an object or an array with security rules is complicated as we just saw.

A better approach at this point is to use sub-collections of documents that contain all the metadata we need, but also act as a queue of pending documents to be denormalized by a firestore trigger.

In this case, nesting a `/likes` sub-collection for `/posts` can help simplify access rules.

```c
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /posts/{postId} {

		allow read;
      	allow write: if (request.auth.uid != null) && (request.resource.author == request.auth.uid);


      	match /likes/{userId} {
        	allow create, delete: if (userId == request.auth.uid)
      	}
	}
  }
}
```

The client only needs to write/delete a document to the `/posts/example/likes/userABC` path, and that's it:

```json
{
	"timestamp": "2010-11-12T13:14:15Z"
}
```

On the backend side we need to denormalize using a firestore trigger like this:

```js
const functions = require('firebase-functions');
const admin = require('firebase-admin');

admin.initializeApp();
const db = admin.firestore();


exports.newLike = functions.firestore.document("posts/{postId}/likes/{userId}").onCreate(async (snapshot, context) => {
    const postRef = db.doc(`/posts/${context.params.postId}`);
    const userId = context.params.userId;
    await postRef.update({
		likedBy: admin.firestore.FieldValue.arrayUnion(userId),
		likesCount: admin.firestore.FieldValue.increment(1)
	});
});

exports.removeLike = functions.firestore.document("posts/{postId}/likes/{userId}").onDelete(async (snapshot, context) => {
    const postRef = db.doc(`/posts/${context.params.postId}`);
    const userId = context.params.userId;
    await postRef.update({
		likedBy: admin.firestore.FieldValue.arrayRemove(userId),
		likesCount: admin.firestore.FieldValue.increment(-1)
	});
});
```

As you can see, the code is more maintainable and easier to reason about. We use the firestore triggers as routers and the subcollection as a queue of intents. Since denormalization happens in the backend, we know we can trust the end result.

[0]: https://firebase.google.com/products/firestore "Firestore by Google"
[1]: https://www.youtube.com/watch?v=DEcwa68f-jY "dotJS 2019 - James Long - CRDTs for Mortals"
[2]: https://firebase.google.com/docs/rules/rules-language "Security Rules language"
