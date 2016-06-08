Title: The Backbone waltz
Summary: Orchestrating an event-driven UI with Backbone.
Date: 2016-05-04
Category: Programming
Tags: backbone, best-practices
Status: draft

![the arsenic waltz](/images/the-arsenic-waltz.jpg "The arsenic waltz")


We know that Backbone has done a great job at provinding the **bare minimum
structure** to build apps that separate logic from presentation, and thus, making them
easier to reason about.

Because we are given just the basic tools in an unopinionated way, the implementation
is left for the developer to design.

This post is an attempt to share some strategies I find useful for **building an
event-driven UI**.

## Reacting to changes in a model

The core idea is that data and buiseness logic is managed by models or collections,
that not only can be shared throughout the app but also rendered in many diferent data-less views.

The way this is achieved is through events.


```js
var View = Backbone.View.extend({
    initialize: function () {
        this.listenTo(this.model, 'sync', this.onSave);
        this.listenTo(this.model, 'error', this.onError);
    }
});
```

In the snippet above we made a view react to events that ocurr on a model.
The first thing you'll notice is that we are using `listenTo()` over `on()`
so that the view is put in charge of tracking the events instead of the model
and therefore we avoid the changes of leaking memory with zombie views, since
it would stop listening to these events once it gets [removed][0].

As models can be attached to multiple views, it is possible that more than one
view is manipulating the model and reacting to the same events, which results
in the developer loosing track of all moving pieces.

The solution to this problem is becoming more specific.

Backbone's `save()` and `fetch()` methods accept **callbacks to react specifically** to
a successful of failed interaction.

```js
var View = Backbone.View.extend({
    events: {
        'submit form': 'onFormSubmit'
    },
    onFormSubmit: function (event) {
        event.preventDefault();
        this.model.save(null, {
            'success': this.onSave.bind(this),
            'error': this.onError.bind(this)
        });
    }
});
```

In this case we are waranteed that the `onSave()` and `onError()`
callbacks are called as a result of the form submit event that this view handles,
whilst other views can still hook to generic events emitted by the same model.

Unfortunatelly there is a problem with this approach and it's that the model
is holding references to a potential *zombie* view. The issue can be easyly spotted
when the interaction with the server takes a while to finish or the view's use case is
esphimeral in nature (like an inline edit interface). If the view is destroyed
when the server has not responded yet, then the success or error callbacks will
get executed, resurrecting the view from the death.


We need something similar to the first snippet, where the view was in charge of
keeping a reference to the model, but we also need to have specificity.

Usando el custom triggers
```js
var View = Backbone.View.extend({
    events: {
        'submit form': 'onFormSubmit'
    },
    initialize: function () {
        this.listenTo(this.model, 'custom-save', this.onSave);
        this.listenTo(this.model, 'custom-error', this.onError);
    },
    onFormSubmit: function (event) {
        event.preventDefault();
        this.model.save(null, {
            'success': function (model) { model.trigger('custom-save'); },
            'error': function (model) { model.trigger('custom-error'); },
        });
    }
});
```

Usando listenTo + data 
```js
var View = Backbone.View.extend({
    events: {
        'submit form': 'onFormSubmit'
    },
    initialize: function () {
        this.listenTo(this.model, 'sync', this.onSave);
        this.listenTo(this.model, 'error', this.onError);
    },
    onFormSubmit: function (event) {
        event.preventDefault();
        this.model.save(null, {'event': 'form-submit'});
    },
    onSave: function (model, xhr, options) {
        if (options.event === 'form-submit') { 
            // do something
        }
    },
    onError: function () {
        if (options.event === 'form-submit') { 
            // do something
        }
    },
});
```

Reacting to multiple events at once
If we remember the Backbone way of doing thins, not only models can be attached to
multiple views, but views can depend on multiple pieces of data too. How can this
situation be handled? Well, here is my attempt:

```js

var trigger = Backbone.trigger.bind(Backbone),
    success = _.partial(trigger, 'refresh-success'),
    error = _.partial(trigger, 'refresh-error');

var View = Backbone.View.extend({
    events: {
        'click .refresh': 'onRefresh'
    },
    initialize: function (options) {
        this.products = options.products;
        this.discounts = options.discounts;
        this.listenTo(Backbone, 'refresh-success', this.onRefreshSuccess);
        this.listenTo(Backbone, 'refresh-error', this.onRefreshError);
    },
    onRefresh: function (event) {
        event.preventDefault();
        $.when(this.products.fetch(), this.discounts.fetch())
            .then(success, error);
    },
    onRefreshSuccess: function (attr1, attr2) {
        // TODO: what arguments do we get?
        // do something
    },
    onRefreshError: function () {
        // TODO: what arguments do we get?
        // do something
    }
});
```
This bad behaviour can be omitted by using an intermediary.

## Representing any state of your data
Reacting to ongoing events
Mostrar el approach de usar bacbkone como lo hacen en mixpanel:
https://code.mixpanel.com/2015/04/08/straightening-our-backbone-a-lesson-in-event-driven-ui-development/

When/Where to fetch your data?
using fetch callbacks, views should be able to handle empty models/collections, and listen to 
the collection/model events to respond to changes, 
Cada vista deberia solamente preocuparse de lo suyo
Las vistas tambien tienen que poder renderizar los datos cualquiera sea su estado.
```javascript
var myModel = new MyModel();
view = new view({model: myModel});
myModel.fetch()
```

Ej: loading y Backbone.SOS


## Modifying a replica

Use model.clone() to use inside a CRUD view so that you can modify it, see a live preview of edits, and have a cancel button which discards
the changes.

```javascript
var View = Backbone.View.extend({
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
});
```

Aca ver si conviene

```javascript
var View = Backbone.View.extend({
    events {
        'click .save': 'onSave'
    },
    initialize: function() {
        this.clone = this.model.clone();
        this.listenTo(this.clone, 'change', this.render);
        this.model.listenTo(this.clone, 'sync', "TODO QUE VA ACA?")
    },
    onSave: funtion (event) {
        this.clone.save();
    }
});
```

# Don't overreact
https://github.com/facebook/react/blob/master/examples/jquery-mobile/js/app.js
https://github.com/facebook/react/tree/master/examples/jquery-bootstrap

[0]: http://backbonejs.org/#View-remove "View remove()"
