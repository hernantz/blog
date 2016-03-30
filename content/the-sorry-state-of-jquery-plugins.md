Title: The sorry state of jQuery plugins
Date: 2016-03-29
Category: Programming
Tags: backbone, javascript, bootstrap, jquery
Summary: A rant on plugins and widgets that do too much.
Status: draft


When adding jQuery widgets to enhance your web app, you'll find **two possible
approaches** in their implementation: On one the plugin does everything for
you (and by *everything* I simply mean *too much*), on the other, the plugin
does the minimum. But of course there is a wide range in between. I'll try to
expose the good?, the bad? and the ugly?

![Bootstrap 3 popovers](/images/popovers.png "Bootstrap 3 popovers")

## The way of jQuery plugins - the ugly? 

To begin, lets see what Boostrap offers for using it's plugins. A plugin
(ie. popover) can be instantiated directly via HTML with lots of `data-`
attributes that will be picked up automatically:

```html
<a tabindex="0" class="btn btn-danger" role="button" data-trigger="focus" 
data-toggle="popover" title="Dismissible popover" data-placement="bottom"
data-content="And here's some amazing content. It's very engaging. Right?">
Click me!</a>
```

Or using JavaScript:

```javascript
$('#example').popover(optionsAndCallbacks);
```

But both can be combined so that the JavaScript options override the `data-`
attributes. Either way, most plugins follow these techniques and **allow
certain amount of customization** so that we can hook into some of it's
functionality via options and callbacks.


## Going down the rabbit hole - the bad?

A more radical example would be the [fullCalendar][3] plugin. It is in charge
of rendering a rather complex [DOM hierachy][4] inside an empty `div` you
define, and everything from fetching events to be displayed on the calendar,
to determining how to behave when you click on an event is done through
configuration, it is controlling some inner state, so you are forced to
initialize it and follow the rules this plugin immposes. 

This may work for simple scenarios, but when you need more control, you'll be
forced to implement *hacky tricks* or even roll your own solution. 

For example, the API of this plugin does not expose a way to handle a double
click on an event, but we can set up this behaviour because this plugin
provides a `eventRender` callback to manipulate a rendered event.

```javascript
$('#calendar').fullCalendar({
  // ... more options here
  eventRender: function (event, element) {
    element.dblclick(function () {
      alert('do something useful!');
    });
  }
});
```

Should you need something more custom like be able to drag-n-drop events
between months, which could be implemented with an infinite scroll of months,
you would be really close to having to fork the entire project.


## Take over popovers - the good?

One of the best things about Bootstrap's widgets is that they can be represented
entirely with HTML, without the need to initialize them through JavaScript.

As a follow up of the popover example, the snippet below shows how to represent
a popover widget. Notice how we can use classes like `bottom` to specify the state
we want for this popover.

```html
<div class="popover bottom">
  <div class="arrow"></div>
  <h3 class="popover-title">Popover title</h3>

  <div class="popover-content">
    <p>Popover content here.</p>
  </div>
</div>
```

Yes, it won't be positioned, and won't be dismissed when you click somewhere
else in the page, but it can be reused as a template for your custom widget.

Say we needed to take full control of a popover. I wrote a simple Backbone view
to achieve that:

```javascript
var PopoverBottom = Backbone.View.extend({
  template: _.template($popoverTmpl),
  attributes: {
    'class': 'popover bottom',
    'tabindex': '-1'  // so that we can focus/blur
  },
  events: {
    'blur': 'remove'
  },
  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    return this;
  }
});
```

We've got a minimum working piece of popover that we control, but it's not
positioned. So we can make use of another library that knows how to position
elements. In this case I'll use [Tether][1] and modify the popover view so
that it can clean up itself before it's removed.

```javascript
var Popover = Backbone.View.extend({
  template: _.template(popoverTmpl),
  attributes: {
    'class': 'popover bottom fade in',
    'tabindex': '-1'
  },
  events: {
    'blur': 'close'
  },
  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    return this;
  },
  show: function($target) {
    this.$el.appendTo(document.body)
    this.$el.css('display', 'block').focus();
    this.tether = new Tether({
      element: this.$el,
      target: $target,
      attachment: 'top middle',
      targetAttachment: 'bottom middle'
    });
  },
  close: function() {
    if (this.tether) { this.tether.destroy(); }
    this.remove();
  }
});
```

We have combined Bootstrap for presentation, Backbone for logic and Tether as
a helper for positioning elements. Live demo [here][2].

## Wishful thinking - the best?

It's perfectly fine if plugins expose a simple way to cover the 80% of use cases
or some basic functionality. But it's clear that pure libraries tend to
outperform ready-made plugins in terms of flexibility. I often see plugins
hiding their methods behind closures, when they could be opening them as
**documented building blocks** to be used at your will. If only plugins allowed
a **clear separation of UI and logic** then you would be able seamlessly
integrate it with the rest of your frameworks.


[1]: http://github.hubspot.com/tether/ "Tether"
[2]: https://jsfiddle.net/p82fsx06/1/ "Live demo"
[3]: http://fullcalendar.io/ "A JavaScript event calendar"
[4]: http://fullcalendar.io/js/fullcalendar-2.6.1/demos/agenda-views.html "Rendered calendar"
