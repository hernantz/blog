Title: The Backbone data waltz
Summary: Orchestrating data relationships in your models 
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

TODO: override toJSON de cada modelo para que incluya esos datos en la vista?
TODO: override del initialize del model para que tenga ya una instancia vacia del related?


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

1. A le pide los ids a B
2. B se fija qque tiene y que pide lo que le falta
3. B notifica que se actualizo
4. A asocia sus datos con B

```javascript
var View = Backbone.View.extend({
    events: {
        'click .refresh': 'onRefresh'
    },
    initialize: function (options) {
        this.products = options.products;
        this.listenTo(this.products, 'related-sync', this.onRefreshSuccess);
        this.listenTo(this.products, 'related-error', this.onRefreshError);
    },
    onRefresh: function (event) {
        event.preventDefault();
        this.products.fetch()
    },
    onRefreshSuccess: function () {
        // do something
    },
    onRefreshError: function () {
        // do something
    }
});
```


If we remember the Backbone way of doing things, not only models can be attached to
multiple views, but views can depend on multiple pieces of data too. How can this
situation be handled? Well, here is my attempt:

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
