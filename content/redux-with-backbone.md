Title: Redux with backbone
Summary: Strategies to implement an event-driven UI.
Date: 2016-05-04
Category: Programming
Tags: backbone, javascript, best-practices
Status: draft

![the arsenic waltz](/images/the-arsenic-waltz.jpg "The arsenic waltz")


We know that Backbone has done a great job at provinding the **bare minimum
structure** to build apps that separate logic from presentation, and thus, making them
easier to reason about.

Because we are given just the basic tools in an unopinionated way, the implementation
is left for the developer to design.

This post is an attempt to share some strategies I find useful for **building an
event-driven UI**.


We need a way to pass data and events down a deep widget tree.
If views receive everything they need by param, they are easier
to understand and easier to test.

With events, they simply propagate them, marionette makes this transparent.

But with a deep hierarchy, at some point we need a Provider.
Provider implies a compromise between reusable child widgets, that
don't care were data comes from or where events go to.
A Provider gives all data it's child widget need.


# A mediator is needed

Remember that backbone encourages models and collections to be shared among
multiple views. Not only models can be attached to multiple views, but views
can depend on multiple pieces of data too.

Explicar que hay que empezar a extraer logica de las vistas a ese controlador.
Vista padre
Mucha jerarquia -> se complica ir pasando eventos en un arbol muy grande -> channels para solucionar eso.


This bad behaviour can be omitted by using an intermediary.

When/Where to fetch your data?
Mostrar el approach de usar bacbkone como lo hacen en mixpanel:
https://code.mixpanel.com/2015/04/08/straightening-our-backbone-a-lesson-in-event-driven-ui-development/

Usar MarionetteJS.Object?

https://www.youtube.com/watch?v=zKXz3pUkw9A

