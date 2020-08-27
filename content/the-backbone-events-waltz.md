Title: The Backbone events waltz
Summary: Snippets that will show you that minimalist means versatile.
Date: 2016-05-04
Category: Programming
Tags: backbone, javascript, best-practices


![The Dance of Death by Isaac Cruikshank](/images/dance-of-death.jpg "The Dance of Death by Isaac Cruikshank")


It is said that perfection is achieved not when there is nothing else to add,
but when there is nothing else to be removed.

[Backbone](https://backbonejs.org/) is a minimalist library that tries to bring some sanity for javascript
interaction and state management. As of today, is falling down in popularity,
but I still believe it offers a great ratio of usability to simplicity.

The idea of this post is to show to show how versatile backbone can be, through
some snippets of use cases that you might find in any app.


## Reacting to *specific* changes in a model

The core idea is that data and business logic is managed by models or
collections, that not only can be shared throughout the app but also rendered
in many different data-less views.

The way this is achieved is through events.

```js
var View = Backbone.View.extend({
    initialize: function () {
        this.listenTo(this.model, 'sync', this.onSave);
        this.listenTo(this.model, 'error', this.onError);
    }
});
```

In the snippet above we made a view react to events that ocurr on a model.  The
first thing you'll notice is that we are using `listenTo()` over `on()` so that
the view is put in charge of tracking the events instead of the model and
therefore we avoid the changes of leaking memory with zombie views, since it
would stop listening to these events once it gets removed.

As models can be attached to multiple views, it is possible that more than one
view is manipulating the model and reacting to the same events, which results
in the developer loosing track of all moving pieces.

The solution to this problem is becoming more specific.

Backbone's `save()` and `fetch()` methods accept **callbacks to react
specifically** to a successful of failed interaction.

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

In this case we are guaranteed that the `onSave()` and `onError()` callbacks are
called as a result of the form submit event that this view handles, whilst
other views can still hook to generic events emitted by the same model.

Unfortunately there is a problem with this approach and it's that the model is
holding references to a potential *zombie* view. The issue can be easily
spotted when the interaction with the server takes a while to finish or the
view's use case is ephemeral in nature (like an inline edit interface). If the
view is destroyed when the server has not responded yet, then the success or
error callbacks will get executed, resurrecting the view from the death.

We need something similar to the first snippet, where the view was in charge of
keeping a reference to the model, but we also need to have specificity.

Through the use of custom triggers, we can get close to that:

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
            'success': function (model, response, opts) {
                 model.trigger('custom-save', model, response, opts);
            },
            'error': function (model, response, opts) {
                model.trigger('custom-error', model, response, opts);
            },
        });
    }
});
```

But, that looks like too much boilerplate, doesn't it? Lucky for us, there
is a cleaner way to achieve the same, and is to use the options param when
calling `save()`.

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
        this.model.save(null, {'action': 'form-submit'});
    },
    onSave: function (model, response, options) {
        if (options.action === 'form-submit') { 
            // do something
        }
    },
    onError: function (model, response, options) {
        if (options.action === 'form-submit') { 
            // do something
        }
    },
});
```

This `options` object is useful to modify the behaviour of the underlying
ajax request, but since it is also passed to the listening functions, we
can add any extra information we need, like where is this event coming from.

This way, every callback that needs to only perform some *action* if the event
corresponds to a specific user interaction, it's just a matter of checking the
value of that parameter. If a given callback should always be run, no matter
what the action was, then it would simply omit this check. As you can see **the
solution requires following a convention**.


## Using custom events

If we remember the Backbone way of doing things, not only models can be
attached to multiple views, but views can depend on multiple pieces of data
too. What if we need to listen to an event that is affected by multiple models?
How can this situation be handled? Well, here is my attempt:

```javascript

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
    onRefreshSuccess: function (res1, res2) {
        // do something
    },
    onRefreshError: function () {
        // do something
    }
});
```

Here we are using Backbone as a channel, an intermediary object to track the
status of multiple models and collections, other views can also listen to this event,
maybe at some point you can start using namespaces:

```javascript
Backbone.trigger('my-module:refresh-success');
```


## Modifying a replica

Any CRUD view needs a model that will be modified, but for this modifications you might see a live preview of edits, and have a cancel button which discards the changes.

Instead of the original model, use `model.clone()` to use inside the view as a replica.

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

This is so that other views that share this same model don't receive events and get intermediate updates (possibly errors too). We only update the original model if the changes can be confirmed.

Since we might extend that to any server interaction, we can also get an error from the backend. So let's only apply the changes if we have a successful state:

```javascript
var View = Backbone.View.extend({
    events {
        'click .save': 'onSave'
    },
    initialize: function() {
        this.clone = this.model.clone();
        this.listenTo(this.clone, 'change error', this.render);
        this.model.listenTo(this.clone, 'sync', 'onCloneSave');
    },
    onSave: funtion (event) {
        event.preventDefault();
        this.clone.save();
    },
    onCloneSave: function () {
        this.model.set(this.clone.toJSON());
    }
});
```


## Displaying any state of your data

Ideally views receive instances, because those instances are shared among other views. The view shouldn't assume that the model has a certain state.  

```javascript
var myModel = new MyModel();
var view = new View({model: myModel});
myModel.fetch() // view should show a loading spinner
view.render() // will render empty
```

In the example above, the view received a model whose lifecycle is managed
outside.
The view should be able to render the model in whatever that state might be.

But it seems that we need a model that has that state: loading & loaded. This state is not a responsibility of the data model. We need models for views state.

```javascript
var ViewState = Backbone.Model.extend({
	initialize: function (attributes, options) {
		this.model = attributes.model;
		this.listenTo(this.model, 'request', 'setLoading');
		this.listenTo(this.model, 'sync error', 'setLoaded');
    },
	setLoading: function () { this.set({'loading': true}); },
    setLoaded: function () { this.set({'loading': false}); },
})
```

And now, to remediate the original example above:

```javascript
var myModel = new MyModel();
var viewState = new ViewState({model: myModel, loading: false});
var view = new View({model: viewState});
myModel.fetch()
view.render() // will show a loading spinner
```

We now keep track of any event undergoing in a data model that represents the state of the view. In this state model we can any other data that we need to display our data model correctly, like which tab is active, or is a button disabled, etc.

## Final thoughts

As stated in the docs, philosophically, Backbone is an attempt to discover the minimal set of data-structuring (models and collections) and user interface (views and URLs) primitives that are generally useful when building web applications with JavaScript.

With backbone you are in charge of managing state. So we saw some examples of real-world apps and their requirements.

I think it succeeds in it's goals, and leaves the developer with a set of tools (instead of products) to be used as needed. But some best-practices and patterns need to evolve organically.

Maybe the next step from here is a set of new tools, like [Marionette](https://marionettejs.com/) proposes?