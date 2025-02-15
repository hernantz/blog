Title: talks
Date: 2017-04-29
Category: personal
Tags: personal
Summary: Talks I've given
Url: talks.html
Save_as: talks.html


## Django UI components for perfectionists with deadlines

We pay great attention to how to write composable python code (with inheritance,
decorators, modules, namespaces, etc). But when it comes to architecting the
templates of your website, this is often overlooked, which rapidly degenerates
in tons of copy&paste of html, css and javascript.  Some might say that this is
what React or Vue (et al) are all about and already solve, but having to render
HTML on the client can increase the complexity of the application (introducing
build steps, another language, more dependencies, etc).

Writing reusable and composable UI components can be achieved using the good 'ol
django templates, with the help of some libraries to fill in the gaps (like
django-components, django-cotton and TailwindCSS) that we will explore and
suggest as a possible solution.

This talk was presented at [DjangoCon US][10] (2024-09-24) and can be watched
online on [Youtube][11]


## Djangonautas! No dejen que djangonautas escriban Javascript!

Knowing Javascript has become indispensable for web development, but perhaps too
complicated, to the point that there is something known as javascript fatigue.
In recent times, libraries and frameworks have emerged that propose a pattern
more similar to how the websites of before were, but without skimping on the
dynamism of modern websites. In this talk we discuss patterns and libraries such
as htmx, django-unicorn, etc. designed to make a Django website more dynamic.

This talk was given at [PyconAr 2021][7] (2021-10-26) and it's based on the blog
post [Djangonauts! Don't let djangonauts write Javascript!][8] and can be watched
online on [Youtube][9].


## El fin esta cerca!

2012 passed and the world did not end. Well, scheduling the next world's
doomsday can be tricky, because working with dates is so. In this talk I try to
share some basic tips and gotchas I learned the hard way while building a
calendaring app, that hopefully will make this task easier for you. The
contents of this talk are based on this post: [Calendaring events with
Python][1].

This talk was given at an in-company session at Machinalis offices
(2017-04-13) and at [Pycon Argentina 2017][2] (2017-11-17).


## Tenemos que dejar de escribir else por dos años

In Python we strongly emphasize that code must be elegant and easy to
interpret, but with PEP8 alone is not enough, many times our logic can be
nested in a cataract of if(s) and else(s) difficult to maintain. In this talk
we explored some strategies to avoid that unnecessary complexity.

This talk was given at the first [Cordoba Python Meetup][0] (2015-12-04).


## Cada mock es un moco

While sometimes mocks are needed, they should not be the first tool you use to
write tests. In this talk I try to explain why It is a pity to be mocking your
code when you could be writing meaningful tests at *almost* the same cost.  The
title reffers to moco (snot in spanish) and mock being *homonyms*. The contents
of this talk are based on the contents of this post: [Mock yourself not your
tests][5].

This talk was given at an in-company session at Machinalis offices
(2015-07-27).


## The ring goes south

In the early days, Django didn't ship a built-in migrations framework. South
was the most popular app to do that. This talk exposed some common pitfalls and
quirks, some of them might still apply to newer Django versions. The title is
based on a song from the Lord Of the Rings soundtrack.

This talk was given at an in-company session at Machinalis offices
(2014-04-30).



[0]: https://www.meetup.com/Cordoba-Python-Meetup/events/226908468/ "Python Meetup Event"
[1]: {filename}/calendaring-events-with-python.md "Calendaring events with Python"
[2]: http://ar.pycon.org/ "PyconAr"
[3]: {filename}/one-configpy-to-config-all.md "One config.py to configure them all"
[4]: https://pydaylp.python.org.ar/ "Pyday La plata 2018"
[5]: {filename}/mock-yourself-not-your-tests.md "Mock yourself not your tests"
[6]: https://eventos.python.org.ar/events/pyconar2019/schedule "PyconAr 2019"
[7]: https://eventos.python.org.ar/events/pyconar2021/activity/452/ "PyconAr 2021"
[8]: {filename}/djangonauts-dont-let-djangonauts-write-javascript.md "Djangonauts! Don't let djangonauts write Javascript!"
[9]: https://www.youtube.com/watch?v=dEg-K3kMj60 "PyConAr 2021 - Djangonautas! no dejen que los djangonautas escriban Javascript!"
[10]: https://2024.djangocon.us/talks/reusable-django-template-components-for-perfectionists-with-deadlines/ "Django UI Components for Perfectionists with Deadlines"
[11]: https://www.youtube.com/watch?v=VQV-nkWTEiU " Django UI Components for Perfectionists with Deadlines with Hernan Lozano"
