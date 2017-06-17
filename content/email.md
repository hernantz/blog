Title: Make usenets great again
Date: 2016-04-29
Category: Programming
Tags: ideas, rants
Summary: How all communication means converge into the email platform.
Status: Draft

![Air Mail Envelope Eiffel Tower](/images/air-mail-envelope-eiffel-tower.png "Air Mail Envelope Eiffel Tower")


## Problems

Everyone has an email address, and uses email. It's based on open standards,
it's protocol is distributed in nature.

It used to be the norm for contacting people in the past, but not anymore.

Apparently there is a whole new world of communication needs that email was not
able to solve, and now is being left behind by many alternative apps and
protocols. Too many. Slack, Whatsapp, IM, IRC, SMS, RSS, blog comments, online forums, etc.

Email feels odd for realtime communication. Threads are impossible to follow,
quoting is hard.

VER usenets, protocolos privados, apps para usar mail como chat.
https://tools.ietf.org/html/rfc977


Not easy to create lists.


## What if everything was an email
UI problem, default subject like `chat with Sara` and Sara will see `chat with Frank`
or a group that can be named.

But every email that has a subject set is a new conversation. E.g: vacations planning.

Remember to support both formats: text and html (emojis, gifs, embedded videos)
Ideally we should use something like markdown or rst when writing the email
and then the client would format it. These formats are meant to represent formatted text but still human readable.
I understand companies will want all the customization css + html allows.

News sites and forums should converge to mailing lists, where every topic or article
is an email, and replies are comments. This would also replace RSS.

A distributed social network could be built on top of this idea.
To share anything, just send an email to your personal mailing-list, anyone who
is subscribed will receive your social updates. Following a friend, would be
the same as subscribing to a new mailing-list.

We still need to introduce the concept of channels. Channels are lists of lists.
This allows you to further classify messages under a shared context (subforums or chatrooms?).

What about inline comments in other apps? like photo albums or google docs?
Well for every piece of content that can be commented, there should be a list.
mailto: ?

Attachments are an antipattern. Anything but text should be a link to a
resource better handled elsewhere. Eventually, email clients would have plugins
that ease the interaction with photos/pdfs/calendar events/etc. File sharing,
voice chat or videoconferencing are problems not addressed by email and should
be solved by other programs. You would share a link to that app, as an email of
course.

New meta: 
The sender should have the oportunity to suggest labels for emails: like event,
task, work or discount. The receiver could choose to accept them or not based
on some criteria. Moreover, labels could be hierarchical like `event:birthday`,
`event:conference`, etc.

Also, some emails could just be text-less and only contain meta information.
This would be perfect for reactions (like, heart, angry face, etc) or sending
"email received/seen" events.

User info should include profile info like avatar, status (maintained as a heartbeat msg), signature (that would get displayed on first email only), full name.

Allow editing/versioning: send new emails with diffs, then apps will display the latest version or handle it somehow.

Approving/Rejecting posts.

COmo hace retweets?
Passwords are also emails: You can create a new password everytime, and get it emailed.


## All hail the email overlord

This way, we have replaced blogs, forums, social networks, IM apps. Apps
would simply present emails in a different UI, but all textual means of
communication have converged into the email platform. All hail the new
communication overlord.

http://nullprogram.com/blog/2017/03/12/ -> encryption
https://josefsson.org/inline-openpgp-considered-harmful.html -> encryption
