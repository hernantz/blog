Title: Django UI components for perfectionists with deadlines
Date: 2024-09-24
Summary: Server side rendering and UI components for a modern frontend.
Category: Programming
Tags: htmx, django, css, architecture, best-practices, python, javascript

![Vintage bridge](/images/bridge.jpg "Vintage blueprint of a bridge")


Building a maintainable frontend architecture is a common problem any django
project needs to solve.

In Django we have ways to architect our code into reusable apps, views & models.

But when it comes to the frontend side of things, its not necessarily strongly
opinionated on this matter. Let's see what this means and what can we do about
it.

## Standing of the shoulders of giants

I don't remember where I heard this, but *Any fool can build a bridge*[^1] is phrase
that stuck with me. It meant that anyone can just throw money, people, energy,
take their time and eventually something will be built). It takes an engineer to
build the "right" bridge (timely and on budget).

This applies to any kind of project (that needs to take you from where you are
to where you want to be, like a bridge does). Software projects are not the
exception.

As engineers we must understand that we live in a world of constraints and
tradeoffs. Every project has a [complexity budget][2]: what features are worth it,
how to spend your time and resources. Budgeting your efforts is not an easy
task. You need to place your bets wisely.

Unless you are on the edge of innovation, most of the problems might already be
solved, you just need to stand on the shoulders of giants.

... or ride unicorns rather.

There is a reason Django's pet used to be a lovely winged pony. And there is a
reason why it's motto is *a framework for perfectionists with deadlines*.

After 19 years (as of today) it is a solid and cohesive framework that solves
most of your problems, with great docs and an awesome community, authentication,
admin interface, ORM & migrations, permissions, routing and 3rd party
extensions, it's 90% of what you will need. But, like we said, it doesn't have
strong opinions on how you build your frontend architecture.

Sadly that left an empty space for other frameworks and solutions outside our
loved django-land to take place. It is still very common to see frontend heavy
frameworks like Vue or React be used for this. But these frameworks introduce a
ton of accidental complexity:

- State management & synchronization between your frontend and backend
- API Churn (how much data to expose on your json endpoints)
- Your team skills are now divided, your codebase is now polyglot
- There is duplication of business logic and validation
- Framework wars and decision fatigue, with ton of changes version after version
- More build steps, more dependencies, you need to keep and eye on load times, etc
- Turns out you still need to make that db query and render that HTML after all


## Everything old is new again

We say that history doesn't repeat itself but often rhymes. Well guess what,
luckily for us, in the recent years the tides are turning.

Postgres was the DB you needed, monoliths are not seen as something necessarily
wrong, and server side rendering is cool again.

What are the problems a good frontend architecture needs to solve anyways?

For a modern frontend, you need three pillars: interactivity to dynamically
display or update fragments of the page, a maintainable & composable CSS
framework, and lastly, a way to create reusable snippets of HTML.


## Interactivity

A low code library that is becoming very popular is HTMX, which by adding some
attributes on you HTML templates lets you interact with the server and update
portions of the page.

```html
<script src="https://unpkg.com/htmx.org@2.0.2"></script>

<!-- have a button POST a click via AJAX -->
<button
  hx-post="/clicked"
  hx-swap="outerHTML"
  hx-target="#some-element">
    Click Me
</button>

<div id="some-element">
  <p>This content will be replaced with a server response</p>
</div>
```

The server knows the state of your data, it has all the business logic, all the
validations and a privileged access to the DB. The client (your browser) simply
needs to request it and, since it already understands HTML natively, it will
draw the UI for you. The browser becomes your frontend application or client
(but one you didn't need to program).

Now, not all interactivity implies a need to reach to the server. There is the
need for client side state manipulation as well. For example disabling a button,
showing/hiding a dropdown, clearing a form, etc UI interactions that belong to
the frontend.

This is where a small library like alpine.js shines, which also follows the same
pattern of inlining directives as part of the HTML element declaration.

```html
<script src="//unpkg.com/alpinejs" defer></script>

<div x-data="{ open: false }">
    <button @click="open = true">Expand</button>

    <span x-show="open">
        Content...
    </span>
</div>
```

Like HTMX, Alpine.js has a handful of directives and plugins for extensibility, and don't require
any [build tools][14].


## Styles

Unless you are building a website for Japan, where every pixel is different (and
this is intended for cultural reasons)[^2], you will need to design some reusable
base styles for your product or brand to bring a cohesive user experience for
you visitors.

This is not as simple as it sounds. Writing maintainable CSS is very hard.

CSS is a global mutable object that every browser interprets with their nuances.
It's easy to start writing your generic names for classes (naming is hard) that
can cause collisions, or doing to much by mixing layout definitions with
coloring, spacing styles that aren't responsive, and then you need to add super
specific selectors to adjust the rules for each page, making your stylesheets
hard to maintain.

```css
.widget {
    position: absolute;
    top: 20px;
    left: 20px;
    background-color: red;
    font-size: 1.5em;
    text-transform: uppercase;
}

#content article h1:first-child .widget {
    width: 200px
}
```

Luckily for us, this has to be a solved issue right? Let's ride unicorns!

[TailwindCSS][3] (I'm sure you heard about it) is a utility first css framework that
provides composable classes for managing spacing, coloring, responsive layouts,
transition effects, etc that you can cherry pick and customize.

```css
<button class="bg-indigo-600 px-4 py-3 text-center text-sm font-semibold
    inline-block text-white cursor-pointer uppercase transition duration-200
    ease-in-out rounded-md hover:bg-indigo-700 focus-visible:outline-none
    focus-visible:ring-2 focus-visible:ring-indigo-600 focus-visible:ring-offset-2
    active:scale-95">
    Tailwind Button
</button>
```

Yes it looks like a ton of text on the screen but this is a technique called
[Atomic CSS][4], similar to the new trend called locality of behavior where you have
all the context you need when working on a piece of you codebase. And also, you
shouldn't copy and paste this everywhere you need a button.

In case you wanted to reduce the repetition, one way to do it is to extract some
styles into a single class and give it a semantic and descriptive name like
`btn-primary`.

But if you abuse of this technique you'll be re-creating a styles framework
again, we have deadlines to meet! Better off, we want to stand on the shoulders
of giants.

Let's ride unicorns! [DaisyUI][5] is a CSS library built on top of tailwind (one of
many) offering many of these classes (already well documented) that you can also
theme and customize to use in your templates.

```html
<button class="btn btn-primary">
    Click me
</button>
```

And remember, DaisyUI is tailwind after all, so you can mix these classes with
regular tailwind classes.

```html
<button class="btn w-64 rounded-full">
    Click me
</button>
```

## Components

Another way to reduce repetition of classes is to think in terms of widgets or
components. Daisy UI also [provides][6] a ton of widgets like cards, tabs, profile
pictures & forms ready to use.

The thing with the widgets is that they often include a mix of CSS + HTML
structure. And sometimes you need to have variations of those widgets. Like
having a product card widget show a button or some tags.

```html
<div class="card bg-base-100 w-96 shadow-xl">
  <figure>
    <img
      src="https://img.daisyui.com/image.webp" alt="Shoes" />
  </figure>
  <div class="card-body">
    <h2 class="card-title">Shoes!</h2>
    <p>If a dog chews shoes whose shoes does he choose?</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Buy Now</button>
      <!-- --- OR --- -->
      <div class="badge badge-outline">Fashion</div>
      <div class="badge badge-outline">Products</div>
    </div>
  </div>
</div>
```

The structure in this example includes some containers like the `.card` and
`.card-body` divs, and some child elements like `.card-title` and
`.card-actions` classes.

How would we turn this into a reusable template in Django?

Django already comes with a template engine that is pretty powerful. We can
parametrize text of course like the title or the description, but what about
child HTML nodes for the `.card-actions`?

```html
<div class="card bg-base-100 w-96 shadow-xl">
  <figure>
    <img
      src="{% static img %}" alt="Shoes" />
  </figure>
  <div class="card-body">
    <h2 class="card-title">{{ title }}</h2>
    <p>{{ description }}</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Buy Now</button>
      <!-- --- OR --- -->
      <div class="badge badge-outline">Fashion</div>
      <div class="badge badge-outline">Products</div>
    </div>
  </div>
</div>
```

In this case we would need to add each possible child element in an if/else
block.

```html
<div class="card bg-base-100 w-96 shadow-xl">
  <figure>
    <img
      src="{% static img %}" alt="Shoes" />
  </figure>
  <div class="card-body">
    <h2 class="card-title">{{ title }}</h2>
    <p>{{ description }}</p>
    <div class="card-actions justify-end">
      {% if action == 'button' %}
      <button class="btn btn-primary">Buy Now</button>
      {% else %}
      <div class="badge badge-outline">{{ tag }}</div>
      {% endif %}
    </div>
  </div>
</div>
```

And then we need to pass what type of widget we would like to render using the
builtin include tag. Every new possible variation of that widget would require
us to modify that `if`/`else` structure we implemented earlier.

```html
{% include 'product-card.html' with type='button' %}
```

Alternatively, if we wanted to allow for any type of `.card-actions` to be
inserted, we could create a base template with certain block tags (something
very common for page layouts).

```html
<div class="card bg-base-100 w-96 shadow-xl">
  <figure>
    <img
      src="{% static img %}" alt="Shoes" />
  </figure>
  <div class="card-body">
    <h2 class="card-title">{{ title }}</h2>
    <p>{{ description }}</p>
    <div class="card-actions justify-end">
      {% block actions %} {% endblock %}
    </div>
  </div>
</div>
```

And then use the extends template tag to create each variation of this component
or widget.

```html
{% extends 'product-card-base.html' }

{% block actions %}
    <button class="btn btn-primary">Buy Now</button>
{% endblock %}
```

And we elegantly solved the extensibility of the base product card for any type
of actions we want to include, but again, this might result in having multiple
instances of templates for each variation anyways.

```html
{% include 'product-card-button.html' %}
```

Is there a way to still write decoupled & re-usable widget templates with
minimal overhead?

A better solution for writing widgets as components that have small variations
is to use a [component library][7], like `django-cotton`:

```html
<div class="card bg-base-100 w-96 shadow-xl">
  <figure>
    <img
      src="{% static img %}" alt="Shoes" />
  </figure>
  <div class="card-body">
    <h2 class="card-title">{{ title }}</h2>
    {{ slot }}
    <div class="card-actions justify-end">
      {{ actions }}
    </div>
  </div>
</div>
```

In this case we are using regular template variables for the `title`, but you
will notice the `slot` special variable and the `actions` as well.

By placing this template in a special location in your project (like the
`cotton` folder within your apps) you have created a reusable component!

```html
<c-product title="Item Title">
    <p>Description of the product</p>
    <c-slot name="actions">
        <button class="btn btn-primary">Buy Now</button>
    </c-slot>
</c-product>
```

If you named the template `product.html`, you'll now have access to a special
tag derived from the name we have to this component.

You can pass still variables as text for the title, but also components can be
nested, and the `{{slot}}` variable will take any HTML enclosed in the component
tags.

The paragraph is what will replace the unnamed `{{slot}}` placeholder.

Lastly the `<c-slot>` element is interpreted as a named HTML snippet, that will
be placed in the `{{actions}}` placeholder.

With this approach we can instantiate *inline* any number of variations of our
product cards without any modifications to other templates.

You can also nest or embed components into other components. In this case I'm
showing that the button inside the `{{actions}}` slot could be a separate
component, this allows for great deal of composability of our widgets.

```html
<c-product title="Item Title">
    <p>Description of the product</p>
    <c-slot name="actions">
        <c-button type="primary">Buy Now</c-button>
    </c-slot>
</c-product>
```

I would like to also mention that `django-cotton` is one of many libraries
competing in this market.

`django-components` has [very similar features][8], but uses a python class first
approach, similar to how we work with forms or views, with many methods you can
override and a registration mechanism (like how we override django admin views).

```python
# In a file called [project root]/components/product/product.py
from django_components import Component, register

@register("product")
class ProductComponent(Component):
    template_name = "product.html"

    def get_context_data(self, title, description):
        return {
            "title": title.title(),  # titlelize!
            "description": description
        }

    class Media:
        css = "style.css"
        js = "script.js"
```

Here is an example of how would you render it, that will look more familiar hopefully.

```html
{% load component_tags %}

{% component "product" title="Title" description="Foo" %}
    {% fill "actions" %}
      <button class="btn btn-primary">Buy Now</button>
    {% endfill %}
{% endcomponent %}
```

As you can appreciate, this syntax is much closer to how other template tags are
used in django.


## A pragmatic frontend architecture

This is what I would suggest as a frontend architecture for perfectionists with
deadlines. Still building on top of what django provides, I believe it is a more
pragmatic approach without, too much overhead for the working dev.

These extra technologies you can learn in a weekend. And what's funny is that,
in their docs, they have references and examples of how they interoperate with
each other.

I would say Htmx and TailwindCSS are very solid choices now, and we shall see which
component library gains more popularity. Ideally some of these libraries to to
define and manipulate reusable components make it into the framework in the near
future.


## Noteworthy mentions

I would like to take a moment to mention some other libraries that are worth
checking out.

`django-template-partials` lets you define and render fragments of templates, which
works great when using Htmx for partial page updates. Also `django-unicorn` mixes
the idea of components with templates and views that can be updated dynamically.
Very interesting concept.

Another noteworthy mentions, but this time related to similar talks in the 2024
[DjangoConUS][13] conference are:

- API Maybe: Bootstrapping a Web Application circa 2024, by Carlton Gibson
- Django + Alpine.js + htmx Ups & Downs, by Karen Tracey
- Choosing Wisely: SPA vs. HTMX for Your Next Web Project, by Chris May
- An Opinionated Guide to Modern Django Forms, by Josh Thomas

All discussing some of the technologies I presented, which shows that there is
some consensus about the problems and their possible solutions. Hopefully this
gives you the encouragement to start playing with them and appreciate how they
solve these problems without too much overhead.


## One more thing

A very recent project was released called fasthml and it copies an idea other
present in other frameworks for solving the UI [composability problem][9].

```python
from fasthtml import ft

ft.Label(
    "Choose an option",
    ft.Select(
        ft.Option("one", value="1", selected=True),
        ft.Option("two", value="2", selected=False),
        ft.Option("three", value=3),
        cls="selector",
        _id="counter",
    ),
    _for="counter",
)
```

Templating HTML is nothing but building a tree of nodes.

By using python for building your template structure, you no longer need to
learn a new syntax and place logic in separate files. You have access to all the
language constructs and utilities: classes, functions, decorators, type
annotations, etc, Plus your favorite debugger now works.

I don't think something like this will ever make it into Django since it is
already married to templates, but it is an interesting idea nevertheless.


[1]: https://www.reddit.com/r/civilengineering/comments/qe3oik/any_idiot_can_build_a_bridge_that_stands_but_it/
[2]: https://htmx.org/essays/complexity-budget/ "Complexity Budget"
[3]: https://tailwindcss.com/ "Rapidly build modern websites without ever leaving your HTML"
[4]: https://johnpolacek.github.io/the-case-for-atomic-css/ "The Case for Atomic / Utility-First CSS"
[5]: https://daisyui.com/ "The most popular component library for Tailwind CSS"
[6]: https://daisyui.com/components/
[7]: https://django-cotton.com/ "Django Cotton - Modern UI Composition for Django"
[8]: https://emilstenstrom.github.io/django-components/latest/ "Create simple reusable template components in Django"
[9]: https://about.fastht.ml/components "Python HTML components"
[10]: https://randomwire.com/why-japanese-web-design-is-so-different/ "Why Japanese Web Design Is So… Different"
[11]: https://randomwire.com/japanese-web-design-redux/ "Japanese Web Design Redux"
[12]: https://www.youtube.com/watch?v=vi8pyS076a8 "Japanese web design: weird, but it works. Here's why"
[13]: https://2024.djangocon.us/schedule/
[14]: https://jvns.ca/blog/2023/02/16/writing-javascript-without-a-build-system/ "Writing Javascript without a build system"

[^1]: The original quote, which is, "Any idiot can build a bridge that stands, but it takes an engineer to build a bridge that barely stands" is attributed to Colin C. Williams (?). The [quote][1] emphasizes the importance of precision and efficiency in engineering, suggesting that anyone can build something strong with unlimited resources, but it takes real skill to design something that’s cost-effective and just strong enough.

[^2]: Japanese web design is [often noted][10] for its [unique approach][11] among the design community, characterized by information-dense layouts, rich use of text/imagery, and overwhelming visual aesthetics that prioritize content variety over minimalist trends (more common in the West). This style is often a reflection of [cultural preferences][12] for conveying more detailed information and providing users with many options upfront.
