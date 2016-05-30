Title: Taming Backbone Views: Part 1
Date: 2014-08-25 19:42
Category: Programming
Tags: backbonejs, best-practices, javascript
Author: hernantz
Status: draft
Summary: Some bro tips I learned the hard way when dealing with Backbone views

It often seems to me that Backbone developers sometimes do not trust that the 
`view.el` property be present when needed, eg: when rendering the view.

# "el", you there? 
But the true story is that Backbone ensures this element is up and running 
for us, since the view construction.  These snippets where taken directly from 
Backbone's source and show a bit of two methods that are ment to be used internally 
by Backbone when instantiating a new View:

```javascript
_ensureElement: function() {
      /* check if this view was not initialize 
         with an {el: '.selector'} option  */
      if (!this.el) {  
        /* ... after constructing an `attrs` object with
           the param options for `id`, `className` and `attributes` 
           create the element specified by `tagName` */
        var $el = Backbone.$('<' + _.result(this, 'tagName') + '>').attr(attrs);

        // now attach this.$el and this.el properties
        this.setElement($el, false);
      }     
      // ... more here omited for brevity
}
```
```javascript
delegateEvents: function(events) {
    // ...
    this.undelegateEvents();
    for (var key in events) {
        // ...
        // the the context of the callback to `this`
        method = _.bind(method, this);
        // set a unique namespace to be easyly unbindable later
        eventName += '.delegateEvents' + this.cid;
        // ...
        // lazyly listen to the event
        this.$el.on(eventName, selector, method);
    }
```
`_ensureElement` will construct our element a attach it to the view instance and 
`delegateEvents()` will lazyly bind DOM events for that element, and all this without worring about 
the element having to be inserted into the DOM to interact with it's view.

Backbone being very flexible, lets us override the `el` property with some other element.
We can pass a jquery object or simply a selector and backbone will handle it.

```javascript
// Backbone also lets us override the `el` with either of these ways 
var view = new Backbone.View({el: '#selector'});
var view = new Backbone.View({el: $('#selector')});
```

In the example above, we need to make sure that, at the moment that View is declared or
executed, the `#selector` exists in the DOM. Otherwise we won't have any html to get from 
the View. So, continueing with the previous example and with a little help from jquery we 
can be sure that `#selector` element can be reached.

```javascript
$(document).ready(function () {
    var view = new Backbone.View({el: '#selector'});
});
```

But even if we make sure of that, **is it a good practice to pass around the `el` object to the
View?**

I'll try to cover the pros and cons of dealing with an encapsulated `el` property vs passing it 
directly to the view in the following post.

it uses event delegation for the events hash, so as long as the element eventually exists


<domino14> if i define an event in a Backbone view, like in events { 'click #btn': 'someFunction'}  does the button have to exist when the view is created?
<domino14> i was under the impression that it didn't
<domino14> yet my "someFunction" isn't executing when i click the button...
<corbanb> yes it has to be in the scope of that view
<domino14> ive had plenty of times where render() creates the buttons that are defined in events {}
<domino14> and the click works
<domino14> render would presumably be created after




# Live preview of edits
Use model.clone() to use inside a CRUD view so that you can modify it and have a cancel button which discards
the changes.
```javascript
events {
    'click .save': 'onSave'
},
initialize: function() {
    this.clone = this.model.clone();
    this.listenTo(this.clone, 'change', 'render');
},
onSave: funtion (event) {
    this.model.save(this.clone.attributes);
}
```

# React without react
Understanding the principles, implementing with Backbone
USE swig template engine to share templates and do server side rendering
Mostrar una lib donde se hace rerender sin el shadow dom
Mostrar como usando los mismos templates se puede hacer renderizado del lado del server.
Mostrar como hacer una "ui loading" que empieza a renderizarse en el server y termina en el frontend
