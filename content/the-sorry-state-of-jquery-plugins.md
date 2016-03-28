Title: Take over popovers 
Date: 2015-10-13
Category: Programming
Status: draft
Tags: backbone, javascript, bootstrap, jquery
Summary: Some strategies to reuse code in your views 

![Bootstrap 3 popovers](/images/popovers.png "Bootstrap 3 popovers")

## The sorry state of jQuery plugins

When adding custom widgets to enhance your web app, you'll find two possible implementation approaches:
On one the plugin does everything for you and there's the plugin that put you in charge of everything.
But of course there is a wide range in between, and by *everything* I simply mean *too much*.

Generally with jQuery plugins we do something like: 

```javascript
$('#myDiv').jPlugin(manyOptionsAndCallbacks);
```

where we are instantiating the plugin in what could be an empty `div` or a minimal HTML structure with lots of `data-` attributes,
that will be picked up automatically by the plugin. Either way, we try to hook into some of it's functionality via options and callbacks.

Lets see how a jQuery mobile widget for rendering a controlgroup works: 

```html
<div data-role="controlgroup" data-type="horizontal">
  <a href="#" data-role="button" data-icon="delete" data-iconpos="left">Left</a>
</div>
```

Gets converted into this:

```html
<div data-role="controlgroup" data-type="horizontal" 
     class="ui-corner-all ui-controlgroup ui-controlgroup-horizontal" 
     aria-disabled="false" data-disabled="false" data-shadow="false" 
     data-corners="true" data-exclude-invisible="true" data-mini="false" 
     data-init-selector=":jqmData(role='controlgroup')">
  <div class="ui-controlgroup-controls">
    <a href="#" data-role="button" data-icon="delete" data-iconpos="left" 
       data-corners="true" data-shadow="true" data-iconshadow="true" 
       data-wrapperels="span" data-theme="c" 
       class="ui-btn ui-shadow ui-btn-corner-all ui-btn-icon-left ui-btn-up-c">
      <span class="ui-btn-inner">
        <span class="ui-btn-text">Left</span>
        <span class="ui-icon ui-icon-delete ui-icon-shadow">&nbsp;</span>
      </span>
    </a>
  </div>
</div>
```

This is a plugin that is in charge of controling and drawing the widget, by doing
heavy DOM manipulation.
aquellos que separan la presentacion del control completamente donde las manipulaciones del DOM son 
menores al punto de consistir en add/remove css classes.


 and work for simple scenarios, but when you need 
more control, you'll need to roll our own solution.
y si bien sus plugins en javascript parecen ser una exepcion, 

Algo bueno que tiene bootstrap en el dise;o de sus widgets es 
que la estructura de los mismos se puede representar enteramente en 
markup html, sin necesidad forzosa de inicializarlos a travez de javascript.


```html
<div class="popover bottom">
  <div class="arrow"></div>
  <h3 class="popover-title">Popover title</h3>

  <div class="popover-content">
    <p>Popover content here.</p>
  </div>
</div>
```

The snippet above shows how to represent a popover widget. Yes, it won't be possitioned,
and won't be dismissed when you click somewhere else in the page.


## Taking control of your widgets

Bootstrap's approach is crearly better in the sense that we can reuse it's
html markup to implement our custom widget.

```javascript

var popoverTmpl = [
  '<div class="arrow"></div>',
  '<h3 class="popover-title"><%=title%></h3>'

  '<div class="popover-content">',
  '<p><%=content%></p>',
  '</div>'
].join('');

var PopoverBottom = Backbone.View.extend({
  template: _.template(popoverTmpl),
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
possitioned. So we can make use of another library that knows how to possition
elements. In this case I'll use [Tether][1], and modify the popover view so
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

This is how we can combine Bootstrap for presentation, Backbone for logic and
Tether as a helper for possitioning elements. Live demo [here][2].

I believe something similar would happen with other widgets, like select2.


[1]: http://github.hubspot.com/tether/ "Tether"
[2]: https://jsfiddle.net/p82fsx06/1/ "Live demo"
