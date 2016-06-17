Title: Taming Backbone view's inheritance
Date: 2015-05-15
Category: Programming
Status: draft
Tags: backbone, javascript, best-practices
Summary: Some strategies to reuse code in your views 


![X-Ray by Eric Drooker](/images/x-ray.jpg "X-Ray by Eric Drooker")

Alternative title: DRYing out your Backbone views

The idea of this post is to show some possible approaches to reuse code
in your backbone views.

Usar un timeline de recent activity feed como ejemplo. Tenemos cosas en comun (marcar como leido, por ejemplo) y cada
feed es diferente.

## First approach: extend a generic view
MarionetteJS item view y collectionview
podes tener 100 de estos tipos de vistas, y cambian muy pocas cosas, como el template.
Hacer prueba de instanciar una vista generica y solo pasarle el template, el $el, la coleccion, etc.

## Second approach: extend a parent view

```js
var BaseView = Backbone.View.extend();
var ChildView = Backbone.View.extend(BaseView, {});
```

## Third approach: parent view contains child views
## Forth approach: MarionetteJS.Behaviour

LEER http://blog.siftscience.com/blog/2015/best-practices-for-building-large-react-applications
Ejemplo modales + login o las columnas del dashboard de divvy
