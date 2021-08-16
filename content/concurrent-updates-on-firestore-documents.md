Title: Concurrent updates on Firestore documents
Date: 2021-08-16
Summary: Can we achieve eventual consistency? Maybe something close to it?
Category: Programming
Tags: database, firebase, firestore

[Firestore][0] (by Firebase) is a JSON document-oriented database (as a
service), that allows concurrent updates to documents, from different clients or
the same client in different points in time, since it offers offline support for
client apps that hold a dynamic local cache, that will eventually be synced with
the server.

This doesn't mean that you don't have to also think about concurrent updates
yourself. Eventual consistency is a topic on it's own, that involves a lot of
academic papers and algorithms (like [CRDTs][1] for instance).

When designing the structure of your documents, it's important to plan
for how will they converge to the final state or shape, leveraging on some
Firestore primitives.

### Upsert merges

In Firestore, data is stored in documents within collections. Each document has
a unique reference, in the form of a path: `/users/joe`, where `/users/` is the
collection and `joe` is the document in this case.

When writting simultaneosly to different documents (or paths) there is no
problem whatsoever, `/users/annie` and `/users/joe` can receive concurrent
updates without affecting each other.

Dividing data in as many divergent document paths as possible is the best way to
deal with concurrency. But it is not always convinient to have that many
documents and subcollections for each possible value we want to update.

Each document might have multiple attributes. Each attribute is also a path to a
value, if you will. Attributes can also be embedded maps with more attributes.

Here, the `/users/joe` document, has the `name` and the `hobbies.reading` paths
for example.

```json
{
	"name": "Joe",
	"surname": "Doe",
	"hobbies": {
		"skiing": true,
		"reading": false
	}
}
```

Imagine having a *profile* section in your app and a separate *hobbies* screen.
Two concurrent operations could update the same user, since we can effectively
write to different paths in the document, without causing any clashes with other
attributes.

```js
await firebase.firestore().doc('/users/joe').set({
	'hobbies.reading': true,
	'hobbies.painting': false
}, { 'merge': true });
```

You may have noticed we are using `set()` with the `{merge: true}` parameter.

When storing data, the *upsert* operation becomes really handy, so that we don't
have to check if a document exists or not before creating it. An, if it exists,
we can also update/merge just attributes we care about (or adding another one
like `hobbies.painting`).

One big caveat we need to consider is that we are aiming for some eventual
consistency, by dividing a big JSON document into smaller paths that can be
updated in little chunks. Since conflict resolution in Firestore is super
simple: it's a *last write wins map*, we need to think of the state of your app
as a big JSON tree that is mutated by lots of JSON-diff patches that may be
applied out of order.

Firestore offers transactions, but this comes at the cost of giving up a lot of
concurrency (and offline support).

We are not achieving eventual consistency, but something close to it by avoiding
conflicts as much as possible.

One last key concept to keep in mind is that we need our state tree to only ever
grow, and never delete data. That way you never upsert data that has been
deleted by another update, hence, a simple `deleted=true|false` flag on every
document should achive the same result. Later upserts will not bring the
document back to life.

```js
// Remove the joe document
await firebase.firestore().doc('/users/joe').set({
	'deleted': true,
}, { 'merge': true });
```

### Sentinel values

Sometimes, dividing the state tree of your app is not enough. Some attributes
require special treatment, like counters, arrays or dates. Since the ordering of
updates is something we don't want to solve, and this scenario will is noticible
when enabling offline support, we need to make use of sentinel values.

[Sentinels][2] act like on-the-spot transactions to transform or update an attribute
by considering it's current value at the moment the upsert occurs.

```js
await firebase.firestore().collection('user').doc('joe').set({
	'sessions': firebase.firestore.FieldValue.increment(1),
	'lastUpdated': firebase.firestore.FieldValue.ServerTimestamp()
}, { 'merge': true });
```

Here we can log each `session` in the app, by incrementing a counter. We don't
care about the exact previous value, just that it is one extra unit. The same
goes with the `lastUpdated`, we simply mark it to be whatever date the server
has at the time of the update.


### Default sentinel (I wish)

Now that we now how handy these sentinel values are, I would like to have
another one that only sets a value in a document if it is empty or missing.

It could have an optional param `setDefault('default', existing=undefined)`.
So this will result in the value *default* being set only if the existing value
is `undefined` (meaning not set).

An example use case is setting a value that should only be set once (like
`dateCreated`):

```js
await firebase.firestore().collection('users').doc('joe').set({
	'dateCreated': firebase.firestore.FieldValue.SetDefault(firebase.firestore.FieldValue.ServerTimestamp()),
	'name': 'Joe',
	'surname': 'Doe'
}, { 'merge': true });
```

Without having to check that this user exists and has the `dateCreated` set.

Unfortunately this feature does not exists at the moment. The workaround is to
first fetch the current document and if that value is not set or needs and
update, we do update it.

```js
const user = await firebase.firestore().collection('users').doc('joe').get();
const dateCreated = user.get('dateCreated') || firebase.firestore.FieldValue.ServerTimestamp();

await user.ref.set({
	dateCreated,
	'name': 'Joe',
	'surname': 'Doe'
}, { 'merge': true })
```

But this is not ideal, since there are no strong guarantees that this field
would not be set more than once by concurrent transactions. It may be still be
useful for backend code though.

[0]: https://firebase.google.com/products/firestore "Firestore by Google"
[1]: https://www.youtube.com/watch?v=DEcwa68f-jY "dotJS 2019 - James Long - CRDTs for Mortals"
[2]: https://firebase.google.com/docs/reference/android/com/google/firebase/firestore/FieldValue "Sentinel values that can be used when writing document fields with set() or update()."
