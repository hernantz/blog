Title: Taming Backbone Views: Part 2
Date: 2014-08-31 15:46
Category: Programming
Tags: backbonejs, best-practices, javascript
Author: hernantz
Status: draft
Summary: Some bro tips I learned the hard way when dealing with Backbone views

Here are some bro tips I learned the hard way when dealing with Backbone views. Hopefully
will make you play nicer with Backbone Views and their workflow.


# When to pass the "el" property to the view

Now we know that we don't have to wait for the DOM to be loaded to interact with views.
So, except for very simple cases, don't pass the el to the view, it simply doesn't scale.

A view should not make any assumptions of existing DOM elements, but rather handle their 
own DOM element, and its events in an encapsulated manner.

If your js application is in charge of rendering the content, then it is better to not pass the `el` 
property, instead if the backend is rendering the html, the it is probably a good idea to 
do so.

A small example of how to deal with both is the following
![](/static/images/backbone-view-events.gif)

```html5
<!-- The templates we will use for each mode -->
<script id="edit-mode" type="text/x-handlebars-template">
    <input type="text" value="<%= title %>" />
    <button class="done">done</button>
</script>
<script id="read-mode" type="text/x-handlebars-template">
    <h3><%= title %></h3>
    <button class="edit">edit</button>
</script>
```
```javascript
// A model and a view for interacting with it
var TitleModel = Backbone.Model.extend({
    defaults: {
        title: 'Lorem Ipsum'
    }
});

var TitleView = Backbone.View.extend({
    READ_MODE: 0,
    EDIT_MODE: 1,
    events: {
        'click .edit': 'onEdit',
        'click .done': 'onDone'
    },
    initialize: function (options) {
        this.mode = options.mode || this.READ_MODE;
        this.readTemplate = _.template($('#read-mode').html());
        this.editTemplate = _.template($('#edit-mode').html());
    },
    onEdit: function (event) {
        event.preventDefault();
        this.mode = this.EDIT_MODE; 
        this.render();
    },
    onDone: function (event) {
        event.preventDefault();
        this.mode = this.READ_MODE; 
        this.model.set('title', this.$('input').val());
        this.render();
    },
    render: function () {
        var context = this.model.toJSON();
        if (this.mode === this.READ_MODE) {
            this.$el.html(this.readTemplate(context));
        } else {
            this.$el.html(this.editTemplate(context));
        }
        return this;
    }
});
```
```javascript
// kick it off!
$(function () {
    var titleModel = new TitleModel();    
    var view = new TitleView({model: titleModel});
    $('body').append(view.render().el);
});
```

Events, how are they handled internally, to access lazyly "events buble"

```javascript
// while you can do this
$(document).ready(function() {
    // here the view will find `#selector` element
    var view = new Backbone.View({el: '#selector'});
}

// try using a more exceptic way
var view = new Backbone.View();
$(document).ready(function () {
    $('#selector').html(view.$el);
}
```

# Who is in charge here?
Following the encapsulation/isolation pattern of a view, the next topic is to determine who is in 
charge of controlling the view.

Ideally you would have a `controller` object, MarionetteJS has a component for that. But 
in plain Backbone, you usually have a "father view" that acts as one and handles it's child views.

Not to trigger `render()` on the view's `initialize()` method is generally a good idea. 
Instead the controlling object will take care of rendering and appending the view to 
where it belongs, when necessary.

It is a good practice that, to always return the object this, on methods that will be called by the 
controller object so that we gain a chainable api to manage the child view. For example, in the 
`render()` method, return the view instance and never rendered html string.

```javascript
var FatherView = Backbone.View.extend({
    // ...
    someMethod: function () {
        // we explicitly call the child's view render method
        this.$('.some-div').html(this.subView.render().el);
    }
});
```

For each `on()` call there should be the respective `off()`. But **be carefull** when calling `off()`,
to give it the same params you passed to `on()` when binding the event, otherwise you'll be unbinding
**all** events from that object, even the ones you didn't set up.
```javascript
var SomeView = Backbone.View.extend({
    // ...
    initialize: function (options) {
        Backbone.on('some:event', this.onSomeEvent, this);
        this.model.on('some:event', this.onModelEvent, this);
    },
    close: function () {
        /* Not this! this.model.off(), there might be other 
           components listening also */
        Backbone.off('some:event', this.onSomeEvent, this);
        this.model.off('some:event', this.onModelEvent, this);
        return this;  // always wellcome ;)
    }
});
```

Better do this
```javascript
var SomeView = Backbone.View.extend({
    // ...
    initialize: function (options) {
        this.listenTo(Backbone, 'some:event', this.onSomeEvent);
        this.listenTo(this.model, 'some:event', this.onModelEvent);
    },
    close: function () {
        /* This is no longer needed, 
           call the `destroy()` method directly */
    }
});
```

# When/Where to fetch your data?
using fetch callbacks, views should be able to handle empty models/collections, and listen to 
the collection/model events to respond to changes, 
```javascript
var myModel = new MyModel();
view = new view({model: myModel});
myModel.fetch()
```

Views are in charge of presentation, not models.
var model.editInModal();
Instead use some kind of helper
helper.editInModal(model);

For communication between views, consider the following options:
* events happening on some shared objects (collections or models)
* custom events explicitly triggered (See the How-To)
* But never call from one view to another (except one of them is a subview of the other).


# TODO
* Recomend Building Backbone Plugins from Derek Bailey and MarionetteJS
* Write about the Backbone.Events object and how it allows us to use listenTo, 'everything that has a trigger'
  and zombie views, close() and onClose()
* A view that represents one model
* View inheritance
