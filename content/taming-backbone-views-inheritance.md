Title: Taming Backbone view's inheritance
Date: 2015-05-15
Category: Programming
Status: draft
Tags: backbone, javascript
Summary: Some strategies to reuse code in your views 


![X-Ray by Eric Drooker](/images/x-ray.jpg "X-Ray by Eric Drooker")

The idea of this post is to show some possible approaches to reuse code
in your backbone views.

Firts things first, let's see what views are, or should be. In the
[Backbone docs][1] there's a clear indication that views are a component that
should just pipe user input into models and display the model's state in a
reactive manner.

![Pelican a static site publishing tool](/images/backbone-model-views-flow.png)

By following this pattern, views become very lightweight and straightforward to
reason about. So, if your views have too much code in them, then your are very
probably doing it wrong.

## First approach: extend a generic view
MarionetteJS item view y collectionview
podes tener 100 de estos tipos de vistas, y cambian muy pocas cosas, como el template.


## First approach: extend a parent view

```js
var BaseView = Backbone.View.extend();
var ChildView = Backbone.View.extend(BaseView, {});
```

## Second approach: parent view contains child views 

[1]: http://backbonejs.org/

LEER http://blog.siftscience.com/blog/2015/best-practices-for-building-large-react-applications
Ejemplo de MarionetteJS.Behaviour
Ejemplo modales + login o las columnas del dashboard de divvy
LEER https://code.mixpanel.com/2015/04/08/straightening-our-backbone-a-lesson-in-event-driven-ui-development/
