Title: Bill'em all
Summary: Implement a billing system that doesn't suck.
Date: 2016-05-04
Category: Programming
Status: Draft


![One dollar](/images/one-dollar.jpg "One dollar")


This post is thougth experiment to design a billing system,
trying to be abstract enought, so that hopefully it covers 
a wide range of sitations, if not all of them, in which
transactions that involve money occur.


## Motivation

A billing system is part of the lifecycle of every organization
It is complex in nature and overlaps with other systems.
For instance, the accounting system, whose goal is to provide
information about the goods and debts an organization has.
It has also responsabilities about permissions, because depending on
your contract or credit status you can access or not certain features.
It can be used as a metrics tracking system since certain
actions that clients perform may have an economic impact on your
app (ie: tickets sold for the cinema, are also a metric of how many people watched the movie). 
And finally it also has to articulate with certain CRM aspects,
as we need to record our interactions with clients and their billing information
to offer discounts, remind them of an contract expiration date, etc. 

These systems exist in every organization that handles money,
but sometimes they turn invisible in the sense that they are embbeded in
another system that does something similar, an Excel spreadsheet usually.

Naturally each of these different systems is a complex beast on it's own and are
better off implemented separatelly.

Take for example the accounting system.
Integration with stock and accounting systems.
There are legal regulations that dictate how this is done, and they change from country to country.
It also depends on the granularity you want to manage, but ussuarlly, you only care about the monthly totals, so maybe exporting aggregates
is enought.

A billing system must:
1. Tell what can a client do (permissions and available features).
2. Determine what his billing status is: who owes how much and why.
3. Articulate with other specialized systems (ie: export data)

Getting paid is a whole different topic. You can pay a single invoice
in several instalments for example.


Things that generate value:

1. Flow of time (renting a room, fixed term deposit)
2. Consumption (of electricity) or service (cleaning the house)
3. Buying/selling items (train tickets)

And these can be combined (rent a room in a hotel, and cosume
some snack from the mini-fridge).

We see that there are atomic and non-atomic.
Buying and selling items is an atomic operation per se.
But the services which are on-going aren't and we have to make
them atomic somehow. 
They require a recurring tick that will issue an atomic eventl,
based on some kind of meassurement, in order to determine the value
of the transaction.

## Billing History 
Events are stored in an append-only journal.

The journal can be digested by procressors that can understand
the deltas between each event to determine the current status
of an account.

## Handling changes
Every change is represented by an event. An event should never be mutated.
Events should freeze all context needed to fully understand them.

Ability to schedule changes to take effect in the future. Example:
apply this new plan next month.
When applying changes (and even when scheduling them?), the system
should look for conflicts in all transactions, including the ones
that had not taken place yet.

Payments should refer to the respective source invoice(s) = [1,2,3].


Pricing models:

1. Free
2. Single sales 
3. Subscription
4. Usage-based

Pre-bill model (cellphone credit), post-bill model (telephone bill)

We need it to be flexible and fault tolerant. For that we will have
to separate policy from mechanism as much as we can.

Flexible not only to adapt to changing business rules but also
users should have the chance to change their subcriptions, receive
returns, discounts, etc.



PCI copliance

https://www.petekeen.net/stripe

Django billing

Lambda architecture
Command-query responsability separation (CQRS)
