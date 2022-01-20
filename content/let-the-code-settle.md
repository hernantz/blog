Title: Let the code settle
Date: 2022-01-20
Summary: Gain confidence when deploying critical changes.
Category: Programming
Tags: best-practices

When working on an important feature for a live product, the risk of breaking
some crucial part of it is higher.

Automated tests, CI pipelines, QA workflows, PR reviews and feature flags are
there to catch any possible errors before any change hits production.

The risk will never be zero though.

The production database might be orders of
magnitude bigger than your testing database, users might be clicking buttons
around in ways you could not anticipate, weird race conditions pop up, etc.

It is better to deploy changes in small chunks that let you revert or
immediately identify and fix a regression/bug that has just been introduced.

But these errors not always pop up immediately.

Your product's rush-hour could be in a different timezone; there are cronjobs
that only execute at one moment in a day/week; some bugs are not detectable
through an crash but rather it's a busyness logic that is wrong, so someone has
to raise a complain, and not every user is eager to waste that time contacting
your support team; etc.

This is why, for critical changes, is best to *let the code settle*.

Wait up a couple hours/days/weeks before deploying more critical changes. You will
give the code enough exposure to real users and gain confidence for your next
deployment.
