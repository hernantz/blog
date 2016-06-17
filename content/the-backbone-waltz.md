Title: The Backbone waltz
Summary: Orchestrating an event-driven UI with Backbone.
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
            'success': function (model, response, options) {
                 model.trigger('custom-save', model, response, options);
            },
            'error': function (model, response, options) {
                model.trigger('custom-error', model, response, options);
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


## Representing complex data

Usually you will have models that depend of data contained in other models, because
you a relational database behind, and you have done a good job normalizing it.

If your data is presented by the server inlining all related data:

```js
{
    'id': 1,
    'uri' '/some/model/1/'
    'some_field': 'some value',
    'related_model': {
        'id': 1
        'uri': '/other/model/1/'
        'some_field': 'some value',
    },
}
```
By overriding the parse method we can hydrate an instance of the related model using
the data sent from the server.

```js
var Model = Backbone.Model.extend({
    parse: function (response) {
        this.relatedModel = new RelatedModel(response['related']);
        return response;
    }
});
```

But this way, can potentially have two independant instances
that refer to the same data, but they don't know about the existance of each other, so 
if one of them changes that data, the other one doesn't get updated with the same changes. 

Multiple instances are best kept inside collections. If only the Model instance acepted
a related collection, then we could store all related models just once.

```js
var Model = Backbone.Model.extend({
    initialize: function (options) {
        // TODO: ver si esto no pisa los datos del modelo
        // TODO: ver la firma del initialize 
        this.related = options.relatedCollection;
    },
    parse: function (data) {
        this.relatedModel = this.related.add(data['related'], {'merge': true});
        return response;
    }
});
```

Now we have a single instance per relation so that if it gets updated in one place 
of the code base, those changes get reflected everywhere.  But the problem now is
that we need to pass this related collection every time we create a new instance. 

Better off is to have both type of models into their respective collections and
and do:

```js
var Model = Backbone.Model.extend({
    associate: function (relatedCollection, options) {
        var opts = options || {};

        // 'related' is not modified in the parse method when obtained
        // from the response and is stored as part of the model's data
        // directly by Backbone.
        var rel = this.get('related'); 

        // Be carefull here with 'merge', since the data that is inside
        // relatedCollection could be more fresh that the one merging now.
        this.relatedModel = relatedCollection.add(rel, {'merge': true});

        // optionally, notify that this model is fully packed now
        if (!opts.silent) {
            this.trigger('change', this);
        }
    }
});

// Then, somewhere in your codebase...
var relatedCollection = new RelatedCollection(),
    model = new Model({
        'foo': 'bar',
        'related': {'id': 1}
    });

model.associate(relatedCollection);
```

TODO hablar de que el JSON response puede no venir inline model, solo el id
por lo que hay que obtener los datos desde otro recurso, con id=1,2,3

TODO: wait for a sync-related event triggered by the model or the entire collection

```javascript
var ModelCollection = Backbone.Collection.extend({
    model: Model,
    associate: function (relatedCollection) {
        // call each model's associate method
        this.invoke('associate', relatedCollection, {'silent': true});

        // optionally, notify that all models in this collection are
        // fully packed now
        this.trigger('update', this);
    }
});
```


If we remember the Backbone way of doing things, not only models can be attached to
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

When/Where to fetch your data?
Mostrar el approach de usar bacbkone como lo hacen en mixpanel:
https://code.mixpanel.com/2015/04/08/straightening-our-backbone-a-lesson-in-event-driven-ui-development/

Usar MarionetteJS.Object?

## Displaying any state of your data

Ideally views receive instances, because those instances are shared among other views.
The view shouldn't assume that the model has a certain state.
It could be possible that there is an undergoing event in the background.
The view should be able to render the model in whatever that state might be.
Cada vista deberia solamente preocuparse de lo suyo

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

Comentar como hacer validacion, devolviendo un hash
```javascript
{
    'campo1': ['error1', 'error2'],
    'campo2': ['error1'],
    '_non-field-errors': ['error1', 'error2']
}
```
Cuando creamos un modelo nuevo, es el mismo caso que `.clone()`
No queremos que el model apenas se muestra tenga errores como "este campo es requerido".


Firts things first, let's see what views are, or should be. In the
[Backbone docs][1] there's a clear indication that views are a component that
should just pipe user input into models and display the model's state in a
reactive manner.

By following this pattern, views become very lightweight and straightforward to
reason about. So, if your views have too much code in them, then your are very
probably doing it wrong.



# Don't overreact
https://github.com/facebook/react/blob/master/examples/jquery-mobile/js/app.js
https://github.com/facebook/react/tree/master/examples/jquery-bootstrap

[0]: http://backbonejs.org/#View-remove "View remove()"
