Title: Endpoints matter
Date: 2021-09-18
Summary: Entities can be identified by IDs, but also paths.
Category: Programming
Tags: database, rest, api

In most applications, system entities do not exist aisolated from each other,
but connected in one to one, many to many or one to may type of relations.

This means that there is more than one way to reach to a specific entity.

Although all entities should have a unique id, the *path* to that entity is also
important when designing REST APIs.

For example, in an blog website, we have `Posts` and `Comment` entities. We
could imagine a posts endpoint in the form: `/posts/{postId}`, but what about
comments?

Comments only make sense in the context of a post, it would be akward to
reference a comment by `/comments/{commentId}` endpoint, or get all comments
from a post through a `/comments/?postId={postId}` filter or comments by their
author: `/user/{userId}/comments/{commentId}`.

A more semantic path to a comment would be
`/posts/{postId}/comments/` and a specific comment by
`/posts/{postId}/comments/{commentId}`.

One could argue that this pattern can also apply for comment replies in the
form: `/posts/{postId}/comments/{commentId}/replies/{replyId}` but it is
probably abusing the pattern and the path to an entity is no longer clear.
Although replies only make sense in the context of a comment they reply to.

Path design to reach connected entities will really depend what are the most
common access paterns to those entieties. There are always hierarchies
in the structure of any database after all.
