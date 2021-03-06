Title: The sorry state of jQuery plugins
Date: 2016-03-31
Category: Programming
Tags: backbone, javascript, bootstrap, jquery
Summary: Customization is not enough, some plugins simply do too much.


When adding jQuery widgets to enhance your web app, you'll find **two possible
approaches** in their implementation: On one the plugin does everything for
you (and by *everything* I simply mean *too much*), on the other, the plugin
does the minimum. But of course there is a wide range in between.

![Bootstrap 3 popovers](/images/popovers.png "Bootstrap 3 popovers")


## The way of jQuery plugins

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

A more extreme example would be the [fullCalendar][3] or the jQuery datepicker
plugins. They are in charge of rendering a rather complex DOM hierachy inside an
empty `div` or `input` you define, and everything is done through configuration.
Since the plugin is controlling some inner state you are forced to initialize it
and follow the rules it immposes.

This may work for simple scenarios, but when you need more control, you'll be
forced to implement *hacky tricks* or even roll your own solution.


## Take over popovers

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


## Wishful thinking

[This video][4] shows the process of hidding functionality and adding lots of
cruft to *jqueryfy* a piece of code. This is exactly what we need to avoid.
More often than not I see plugins hiding their methods behind closures, when
they could be opening them as **documented building blocks** to be used at your
will.

It's perfectly fine if plugins expose a simple way to cover the 80% of use cases
or some basic functionality. But it's clear that pure libraries tend to
outperform ready-made plugins in terms of flexibility.

If only plugins allowed a **clear separation of UI and logic**, and that logic
be easily extendable, then you would be able seamlessly integrate it with the
rest of your frameworks.

[1]: http://github.hubspot.com/tether/ "Tether"
[2]: https://jsfiddle.net/p82fsx06/1/ "Live demo"
[3]: http://fullcalendar.io/ "A JavaScript event calendar"
[4]: https://youtu.be/Qkm5h4032ko "Pamela Fox - Beyond jQuery Widgets: JS UI Library Design"
