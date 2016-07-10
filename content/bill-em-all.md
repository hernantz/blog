Title: Bill'em all
Summary: Thougth experiment to design a *generic* billing system.
Date: 2016-05-04
Category: Programming
Status: Draft


![One dollar](/images/one-dollar.jpg "One dollar")


## Abstract

This post is thougth experiment to design a billing system, trying to be generic
enought, so that hopefully it covers a wide range of situations (if not all of
them), in which transactions that involve money take place.


## Introduction

A billing system is part of the lifecycle of every organization.
It is complex in nature and overlaps with other systems.

For instance, the **accounting system**, whose goal is to provide
information about the assets and liabilities an organization has.

It has also responsabilities about **permissions**, because depending on
your contract or credit status you can access or not certain features.

It can be used as a **metrics tracking** system since certain
actions that clients perform may have an economic impact on your
app (ie: tickets sold in a cinema, are also a metric for how many people
watched the movie). It might also overlap with a stocks system, since each
purchase or refund has to be accounted as a monetary and material transaction.

Getting paid is a whole topic on it's own, you can issue single invoice
but get paid in several instalments for example. These systems are known as
**payment gateways**, an need to interact with the billing system too.

And finally it also has to articulate with certain **CRM** aspects,
as we need to record our interactions with clients and their billing information
to offer discounts, remind them of an contract expiration date, facilitate
nurturing, etc.

These systems exist in every organization that handles money,
but sometimes they turn invisible in the sense that they are embbeded in
another system that does something similar, an Excel spreadsheet most likely.

Naturally each of these different systems is a complex beast on it's own and is
better off implemented separatelly. And as a colorary of this, we can say that
you'll invevitably have duplication of data.

Take for example the accounting system. There are legal regulations that
dictate how this is done, and they change from country to country.
The granularity level managed by the accounting system also differs, since but
usually, you only care about the totals, so maybe exporting aggregates obtained
by the billing or stocks system is enought.
Also in the case of the permissions systems, there are other considerations taken
into account, like user roles, locks, etc.
TODO: PCI copliance <- payment gateways

Because billing systems are also very tightly coupled with business rules,
it's really hard to build a generic catch-all solution, making it difficult to
attempt a proper sepparation of [mechanism and policy][0]. It's also evident
that the boundaries of these systems aren't so clear in terms of
responsabilities, but this doesn't mean that a common underling architecture
cannot be identified.


## Goals

From a 30k feet view, a billing system must:

* Determine what his billing status is: ***who*** owes ***how much*** and
  ***why***.
* Articulate with other specialized systems (ie: be able to query and be
  queried, import/export data).
* Be flexible and fault tolerant. Flexible not only to ***adapt to ever changing
  business rules***, but also users should have the chance to change their
  contracts, receive refunds, benefit from a discount or even a free-trial, etc.


But first we must take a step back so that we can identify which are the sources of profit:

* **Free**: the simplest one, no profits though.
* **Single sales**: when you purchase an item or service like train tickets or house
  cleaning.
* **Subscriptions**: cable tv, hotels, insurance, fixed term deposits.
* **Usage-based**: like power supply or phone calls.
* **A combination** of all these.


All these sources of profit have to be translated to money somehow.
For this to happen, we need to determine when to record that something has generated some profit.
Non-atomic operations require a unit of messure and a rate to do this.

We see that there are atomic and non-atomic.
Buying and selling items is an atomic operation per se.
But the services which are on-going aren't and we have to make
them atomic somehow. 
They require a recurring tick that will issue an atomic event,
based on some kind of meassurement or sample, in order to determine the value
of the transaction.

When to issue the bill:
Pre-bill model (cellphone credit), post-bill model (telephone bill)


Tell what can a client do (permissions and available features). TODO esto no?


## Billing entities

User/Account that holds data about contracts, pricing plans, billing details, etc.

Events are stored in an append-only journal.

The clock

The journal contains all the billing history of an account or client.

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


## Real world examples
- EPEC
- Hotel
And these can be combined (rent a room in a hotel, and cosume
some snack from the mini-fridge).
- ISP
- Ad based website
- Sass app (trials, discounts, etc)

https://www.petekeen.net/stripe

Django billing

Lambda architecture
Command-query responsability separation (CQRS)
https://en.wikipedia.org/wiki/Command%E2%80%93query_separation

[0]: http://www.machinalis.com/blog/separating-mechanism-from-policy/ "Separating mechanism from policy"
