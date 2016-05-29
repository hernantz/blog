Title: Orchestrating Backbone events
Summary: blah
Date: 2016-05-04
Category: Programming
Tags: backbone

![the arsenic waltz](/images/the-arsenic-waltz.jpg "The arsenic waltz")

Usando el listenTo
```js
var View = Backbone.View.extend({
    initialize: function () {
        this.listenTo(this.model, 'sync', this.onSave);
        this.listenTo(this.model, 'error', this.onError);
    }
});
```

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
var View = Backbone.View.extend({
    events: {
        'click .refresh': 'onRefresh'
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

Reacting to ongoing events
Ej: loading
