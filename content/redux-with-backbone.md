Title: Redux with backbone
Summary: Strategies to implement an event-driven UI.
Date: 2016-05-04
Category: Programming
Tags: backbone, javascript, best-practices
Status: draft

![The Dance of Death by Isaac Cruikshank](/images/dance-of-death.jpg "The Dance of Death by Isaac Cruikshank")


We know that Backbone has done a great job at provinding the **bare minimum
structure** to build apps that separate logic from presentation, and thus, making them
easier to reason about.

Because we are given just the basic tools in an unopinionated way, the implementation
is left for the developer to design.

This post is an attempt to share some strategies I find useful for **building an
event-driven UI**.


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

