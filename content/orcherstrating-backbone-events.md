Title: The Backbone waltz
Summary: Orchestrating an event-driven UI with Backbone.
Date: 2016-05-04
Category: Programming
Tags: backbone, best-practices
Status: draft

![the arsenic waltz](/images/the-arsenic-waltz.jpg "The arsenic waltz")


We know that Backbone has done a great job at provinding the bare minimum
structure to build apps that separate logic from presentation, and thus, making them
easier to reason about.

The core idea is that data and buiseness logic is managed by models or collections,
that not only can be shared throughout the app but also rendered in many diferent data-less views.

The way this is achieved is through events.

## Reacting to changes in a model
Usando el listenTo vs .on
```js
var View = Backbone.View.extend({
    initialize: function () {
        this.listenTo(this.model, 'sync', this.onSave);
        this.listenTo(this.model, 'error', this.onError);
    }
});
```

El problema es que esta vista puede estar conviviendo con otras que tambien
escuchan a esos eventos.

## Becoming more specific

Usando el bind
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

Usando el custom triggers
```js
var View = Backbone.View.extend({
    events: {
        'submit form': 'onFormSubmit'
    },
    initialize: function () {
        this.listenTo(this.model, 'custom-sync', this.onSave);
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
