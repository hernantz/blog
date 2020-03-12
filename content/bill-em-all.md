Title: Architecture of a billing system
Summary: Thought experiment to design a *generic* billing system.
Date: 2016-05-04
Category: Programming
Tags: ideas
Status: Draft


![One dollar](/images/one-dollar.jpg "One dollar")


## Abstract

This post is thougth experiment to design a billing system, trying to be generic
enough, so that hopefully it covers a wide range of situations (if not all of
them), in which transactions that involve money take place.


## Scope

A billing system is part of the lifecycle of every organization.
It is complex in nature and overlaps with other systems.

For instance, the **accounting system**, whose goal is to provide
information about the assets and liabilities an organization has.

It has also responsabilities about **permissions**, because depending on
your contract or credit balance you can access or not certain features.

It can be used as a **metrics tracking** system since certain
actions that clients perform may have an economic impact on your
app (ie: tickets sold in a cinema, are also a metric for how many people
watched the movie). It might also overlap with a stocks system, since each
purchase or refund has to be accounted as a monetary and material transaction.

Getting paid is a whole topic on it's own. You can issue single invoice
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
better off implemented separatelly.

Take for example the accounting system. There are legal regulations that
dictate how this is done, and they change from country to country.
Some financial transactions have to be approved by regulatory authorities.
The granularity level managed by the accounting system also differs, since
usually you only care about the totals, so maybe exporting aggregates obtained
by the billing or stocks system is enough.
Also in the case of the permissions systems, there are other considerations
taken into account, like credentials, user roles, locks, etc.
And finally payment gateways have [very strict security requirements][1] that
are better off delegated to a trusted third party system.

Because billing systems are also very tightly coupled with business rules,
it's really hard to build a generic catch-all solution, making it difficult to
attempt a proper sepparation of [mechanism and policy][0]. It's also evident
that the boundaries of these systems aren't so clear in terms of
responsabilities, but this doesn't mean that a common underlying architecture
cannot be identified.


## Requirements

From a 30k feet view, a billing system must:

* Determine what the customer's billing status is: ***who*** owes ***how much*** and
  ***why***.
* Articulate with other specialized systems (ie: be able to query and be
  queried, import/export data).
* Be flexible and fault tolerant. Flexible not only to ***adapt to ever changing
  business rules***, but also users should have the chance to change their
  contracts, receive refunds, benefit from a discount or even a free-trial, etc.


But first we must take a step back so that we can identify which are the sources
of profit:

* **Free**: the simplest one, no profits though.
* **One time charges**: when you purchase an item or single transaction service
  like train tickets or house cleaning.
* **Subscriptions**: cable tv, hotel rooms, insurance, fixed term deposits,
  where the amount is a product of time and a fixed plan fee.
* **Usage-based**: like power supply or cell data, there is a meter that
  meassures consumption that might have different rates depending on demand.
* **A combination** of all these.

All these sources of profit have to be translated to money somehow.
For this to happen, we need to **determine when to record that something has
generated some profit** that needs to be "collected".

In the case of single sales it's simple to identify that moment, since it's
usually when the buy order is submitted or when the user receives the product.
But to determine how much someone owes in case of subscriptions or usage-based
models, we need a ticking clock, that ticks every minute, day, fortnight, etc.

Buying and selling items is an *atomic* operation per se, but transactions which
are always *on-going* aren't and we have to make them atomic somehow. Non-atomic
operations need a recurring tick that will meassure or sample some quantity
and/or a rate, in order to determine the value of the transaction. Every
meassurement taken can be understood as a transaction that resulted in some
profit.

The other determination that needs to be taken is **when to charge the
customer**, and for that it's up to the business owner to say if to use a
**pay upfront model** (like when renting a house) or **pay later model** (like the
telephone bill).


## Billing entities

To acomplish the goals of a billing system we need some basic building blocks:

* **Event**: contains an atomic transaction and all it's context (type,
  timestamp, description, amount, metadata, etc), it can be an invoice, a
  refund, a product sale, a payment, etc.
* **Meter**: when billing based on consumption we need a meter that ticks every
  X amount of time (every minute, day, month) and meassures the consumption of
  time, data, electricity, etc to create an event to account for that
  transaction. The interval depends on business rules. In case of
  subscriptions, it's the same idea, what is being consumed is time under
  contract, the only difference is that since the time consumed chaned at a
  constant phase, we might only care on changes in the pricing plans and
  start/end dates, not every second that ticks.
* **Journal**: events are stored in an append-only journal. It contains all the
  billing history of an account. Can be used for an audit.
* **Processor**: The journal can be digested by procressors that can understand
  the deltas between each event to determine the current status of an account.
  Since the journal is immutable, you can cache results up to a point for
  performance reasons, to obtain intermediate balances, determine totals,
  debts, which accounts are past-due, etc, but replaying events becomes
  problematic over time also due to changes in schema, so your processor will
  need to understand every event, old and new.

Contracts, payment gateways, stock management systems, permission systems, etc
are all auxiliary entities that support a billing system.

This architecture is known as event-sourcing.


## Real world examples

So far I hope is clear what a billing system must do and what it needs to do it.
But we still haven't tested our theory we real world examples.

- EPEC cobra de acuerdo al horario y al consumo.
- Hotel
And these can be combined (rent a room in a hotel, and cosume
some snack from the mini-fridge). Holidays and weekends are more expensive, a change of room might happen.
- Ad clicks and views for website
- Sass app (trials, change in plan, discounts, etc)

Every change is represented by an event. An event should never be mutated.
Events should freeze all context needed to fully understand them.

Ability to schedule changes to take effect in the future. Example:
apply this new plan next month.
When applying changes (and even when scheduling them?), the system
should look for conflicts in all transactions, including the ones
that had not taken place yet. Payments should refer to the respective source invoice(s) = [1,2,3].

https://www.petekeen.net/stripe

Django billing

https://martinfowler.com/articles/201701-event-driven.html
https://techblog.commercetools.com/webhooks-the-devil-in-the-details-ca7f7982c24f#.5z8ej1fli
Lambda architecture

Happy billling!

[0]: https://web.archive.org/web/20161101134056/http://www.machinalis.com/blog/separating-mechanism-from-policy/ "Separating mechanism from policy"
[1]: https://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard "PCI copliance"
