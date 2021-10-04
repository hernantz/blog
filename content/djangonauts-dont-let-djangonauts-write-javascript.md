Title: Djangonauts don't let djangonauts write Javascript
Date: 2017-05-25
Category: Programming
Tags: python, django, javascript, rants
Status: Draft

![The canonical website architecture](/images/djangonauts.png "The canonical website architecture")

> JS Fatigue happens when people use tools
> they don't need to solve problems they
> don't have.
  >
> <cite> ― Lucas F. Costa, [The Ultimate Guide to JavaScript Fatigue: Realities of our industry][1]</cite>


## Documents vs Apps

90%, if not more, of websites are just [documents][2]. They render text, images and
forms on your screen. The rest are apps.

Apps have their own needs. They mimic a desktop UI, have custom widgets, need to
work offline sometimes and handle lot's of state and complex workflows.

Apps don't feel like they belong to the web. Can you open multiple tabs of the
same site? Is text selectable? Can you read a printable version of it? Does back
and forth navigation work? Are URLs semantic and [bookmarkable][3]? Can screen
readers understand your site? Is it crawlable and SEO friendly?

If you say no to most of this questions, then you are in presence of an app, not
a web page. Maybe a website is not best suited for this type of projects.

A native app would be better instead of re-implementing entire cross platform
libraries and frameworks to work on top of a document rendering engine. Yet the
industry has pushed/forced websites to become surrogates of native apps. But
this is a symptom of a much deeper problem.

I guess the market fragmentation of OS's is to blame here. Browsers are becoming
a layer of sanity on top of all the different platforms and run-times out there,
where developers only care about implementing some API's to bridge to the
camera, network, disk, etc, built on top of open standards. Webapps become
discoverable, portable and easily installable.

But still, the DOM and Javascript lag behind as a cross-platform GUI framework
that can replace native apps. Either wasm will fill this gap someday, or Java
applets make a comeback, maybe?

## Architecture smells

Every architecture has a [Complexity Budget][4]. It is important to define what
the best way to spend it is. What features will need more attention, what's the
essence of the application, what purpose it serves, in what problem space it
dwells.

Not spending the complexity budget wisely means cognitive overhead in your
codebase, over-engineered solutions, accidental complexity, reduced speed of
development.

Single page apps (SPAs) are a form of micro services architecture. A
decentralized architecture where there are clients and servers.

Micro services in general and client-server architectures in particular are hard
to get right. They can be an overkill for most projects, specially websites.

A lot of infrastructure is needed, coordination between specialized teams,
multiple points of failure, API deprecation policies, etc, that increase
development and maintainability costs. There's a lot that can go wrong.

As code smells, architecture smells do exists too.

A poor micro services architecture can be detected when in order to develop a
feature, you need to touch three repos and instantiate several services to test
it locally. In a similar note, if you have to modify the client code along with
the server code to reflect a new change in a page and deploy both changes at the
same time, it may be that you didn't need a SPA to begin with.

The tight coupling between client and server (which indicates that it is still a
monolith), or between micro services (another monolith), are one of those smells
or thinks that feel wrong.

Another architecture smell is using your SPA as the [only consumer of your API][5].

Creating a JSON API just because in the future you might need for other clients
indicates an early optimization decision. [YAGNI][6]. JSON APIs are targeted for
code consumption, not for human interaction, are usually generic or agnostic
from any UI, are stable and versioned, etc. Generic APIs might suffer [from an
expressivity/security tradeoff][7], because everything you make available to the
UI, could also be leaked for malign users. Moreover, this single client SPA
requires duplication of logic, models, validation, etc, which the backend will
also have to implement since clients cannot be trusted.

## You probably don't need a SPA

[SPAs are hard][10]. If not done correctly, you could be [adding megabytes worth
of code][11] that needs to be downloaded and executed, probably contributing to
the current [web obesity][12] crisis.

Latest tendencies in the JS world show a [comeback to the old ways][9]. Server
side rendering so that we don't load a blank page as splash screen, GraphQL as a
poor attempt to get back to the trusted backend's SQL, per page hot-loading of
bundles trying to break up huge javascript files that bundle entire templates and
models that might not be needed everywhere, etc.

This shows little or no benefit to end users of you website, but clearly incurs
into costly development cycles: An ever-changing amount of frameworks, tooling
(transpilers, bundlers, linters), libraries, DSLs and state management patterns
that all compete to be the next hot thing in the industry. This contributes to
churn in development teams that need to keep up with the [javascript
fatigue](https://javascript.works-hub.com/learn/a-javascript-free-frontend-61275).

Big frontend codebases have become a [liability][13].

Devs nowadays seem to just skip all this analysis, and are eager to start every
project with:

```js
npm install create-react-app graphql
```

It all comes down to [tradeoffs][23]. What's driving these frontend heavy
industry standards to be the default go to?

The answer to that could range from peer pressure, job stability, FOMO or
probably not knowing other alternatives to create snappy websites.

## No JS / Low JS sites

As the common proverb says: *“What has been will be again, what has been done
will be done again; there is nothing new under the sun”*, server side
rendering and static site generators are [reviving][14].

This HTML centric architecture can be a very competitive alternative for
interactive websites when modernized with a few tweaks.

If data is going to be represented as HTML, why not serve HTML directly? This
has the nice property of less time to interactive websites, since there's no
need for extra round-trips and hydrate/dehydrate JSON.
Serving HTML isn't significantly more expensive than JSON. Like any text format
it compresses well, browsers are very performant at parsing and rendering it.

The server describes the UI, it is the single source of truth, it has all the
tools it needs to do so and it's [cheaper][15] to implement.

You go from using a JSON representation of your data:

```json
{
  "account": {
    "account_number": 42,
    "balance": {
      "currency": "usd",
      "value": 100.00
    },
    "links": {
      "deposits": "/accounts/42/deposits",
      "withdrawals": "/accounts/42/withdrawals",
      "transfers": "/accounts/42/transfers",
      "close-requests": "/accounts/42/close-requests"
    }
  }
}
```

To using it's HTML representation:

```html
<dl>
  <dt>Name:</dt>
  <dd>John Doe</dd>
  <dt>Account number:</dt>
  <dd>42</dd>
  <dt>Balance:</dt>
  <dd>100</dd>
</dl>
<nav>
  <a href="/accounts/42/deposit">Deposit</a>
  <a href="/accounts/42/withdraw">Withdraw</a>
  <a href="/accounts/42/transfer">Email</a>
  <a href="/accounts/42/close">Close</a>
</nav>
```

This is known as the [HATEOAS][16], just one aspect of REST. We still use
endpoints (URIs to locate resources on the web), HTTP verbs to perform actions
on them, and HTML to represent those resources.

When using **HTML as the technology to render the app state**, the browser is
the client, not your SPA. User will always get the latest representation of your
data, and what can be done with it. It treats synchronous API payloads as a kind
of declarative UI language for full state interactions.

The question is, how powerful is HTML alone?

It is very powerful and expressive, and getting better still. We now have [async
and defer][17] attributes to load non-blocking `<script>`'s in parallel,
[semantic markup tags][18] to enrich human and program readability,
[preload][19] `<link>` directives for increasing performance of any document
(pre-resolving DNS, pre-rendering another document, etc), the `<picture>` tag
can be used to load [responsive images][20], `<form>` elements have native
widgets for things like datetime pickers and [validation][21] built-in,
offscreen `<img>` can be [loaded lazily][22], there's even a built-in toggle
using the `<details>` and `<summary>` tags!

But as powerful as it its, it still lacks some directives to make it more
dynamic and reactive.

It's not that we need a Javascript everywhere solution for this. But Javascript
can help with a **progressive enhancement approach, through lightweight and
unobtrusive libraries**, to provide a smoother experience for end users.

One of such libraries is [htmx][24]. It doesn't advertise itself as a JS
library, but as a backend agnostic HTML enhancer, extending it's capabilities
with custom attributes, lazy loading or [partial rendering][41] small sections
of the page through AJAX directives and smooth transitions.

```html
<!-- Load from unpkg, jspm.org or skypack.dev, just 10kb, no need for npm! -->
<script src="https://unpkg.com/htmx.org@1.5.0"></script>

<!-- have a button POST a click via AJAX -->
<button hx-post="/clicked" hx-swap="outerHTML">
  Click Me
</button>
```

In the example above, we can see that **we are enhancing the HTML we already
have**, with some `hx-` directives to perform an http post request and replace
the button with the server response.


### Perceived performance

When loading websites, some latency is expected, but too much can lead users to
multi task and abandon the page.

Pages have to load fast, and one of the best ways to make sure that's the case
is to make extensive use of caching headers.

But even so, the user might still experience the blink of a full page load.

If instead you use ajax to fetch a link and swap the `<body>` while you display
a nice animation for the transition.

Similar to what [turbolinks][25] does, with htmx, this [can be done][26] with
the `hx-boost` attribute.

```html
<div hx-boost="true">
  <a href="/blog">Blog</a>
</div>
```

This progressive enhancement trick can be improved by using something like
[Nprogress][27] increase [perceived performance][28].

```js
htmx.on("htmx:beforeSend", function(evt){
  NProgress.configure({ trickleSpeed: 100 });
  NProgress.start();
  NProgress.set(0.4);
});

htmx.on("htmx:afterOnLoad", function(evt){
  NProgress.done();
});
```

The progress bar can be manipulated by changing their speed, so users have
something to watch and stay on your page.

Hooking to some htmx events, we can plug our code to display the progress bar.

In this case we show a big first step and then every 100 ms we update the
progress until it is completed.

### It's turbo time!

Although progress bars and ajax links can make your application *feel* fast,
there's a technique that can make it actually *be* faster.

This technique consists on intelligently pre-fetching links before they get
accessed.

When the user hovers over a link it takes about 300ms to actually click the
link. [Test your own hover timing here][29]. Those wasted milliseconds can be
used to preload the contents of the link.

Libraries like [instant.page][30] or [instantclick][31]  are drop-in scripts
that take use this strategy. Another interesting strategy is what
[quicklink][32] offers, which is to load visible links when the browser is idle.

Htmx doesn't lag behind, since it support extensions, you can make use of the
[preload][33] directive to trigger it on `mouseover` or `mousedown` events.

```html
<div hx-ext="preload">
  <a href="/my-next-page" preload="mouseover" preload-images="true">Next Page</a>
</div>
```

This tools need to be used carefully since you might be over-fetching lots of
pages that the user won't ever need, so it makes sense for certain navigation
links like main menu or a tabbed pane.

### Partial rendering

It often happens that the vast majority of the page is static, but there is a
tiny portion that needs to be updated in response to an action, like clicking
on a paginated list of results.

When htmx communicates with the backend, it sets certain HTTP headers that can
be used to render partial content instead without screwing up scroll positions.

In Django land, [django-htmx][34] provides some helpers that allow our views to
render different content depending on the `request.htmx` flag.

```python
def my_view(request):
    if request.htmx:
        template_name = "partial.html"
    else:
        template_name = "complete.html"
    return render(template_name)
```

Then in the `complete.html` template, we can use:

```html
{% extends "base.html %}

{% block main %}
<main>

  <h1>Static content that doesn't change</h1>

  {% include "partial.html" %}

</main>
{% endblock %}
```

And in the `partial.html` template we just include only what is dynamic.

```html
<div hx-target="this" hx-swap="outerHTML">
  <p>It is {% now "SHORT_DATETIME_FORMAT" %}</p>
  <a hx-get="/my-view/" href="#">Refresh</a>
</div>
```

A nice addition to using partials, the [slippers][35] library lets you write
reusable components that can be extended in your in your templates, which are
more versatile than what Django offers out of the box.

If the snippet requires more interactivity, like a real time form validation,
something like [django-unicorn][36] can be a good choice, since it uses
morphdom, which [htmx also supports][37] to do HTML diffing, which can help
preserve the focused element for example, instead of replacing the entire DOM
sub-tree.

### Async rendering

It often happens that the vast majority of the page is generic to every user,
but there is a tiny portion that needs to be custom for logged in users, like
the *"Hi user222"* snippet included in most nav bars, which depends on each user
being logged in or not.

This is a bummer, since the entire page could be perfectly cachable, if it
wasn't for that piece of user specific content.

One way to overcome this is, is to use lazy/async rendering of those snippets.

Other times some parts of the page take more time to load, and it would be
better to defer the rendering for later, once the user has loaded the rest of
the content.

```html
<div hx-get="/profile" hx-trigger="load" hx-swap="outerHTML">
  <img class="htmx-indicator" src="/spinner.gif" />
</div>
```

The `hx-trigger` is activated when the element is `load`ed (but can also accept
other triggers like `revealed`, `intersect`, etc). The `htmx-indicator` class is
used to toggle it's visibility, useful to display some sort of placeholder or
spinner.

### Javascript is fine

The techniques mentioned are good alternatives to SPA or heavy frameworks, but
there is no silver bullet. More alternatives do exist, like [alpine][38] or
[hyperscript][39], that let you express more UI behaviors within an HTML
element.

Some libraries can be included from CDNs like unpkg, jspm.org or skypack.dev and
using minimal dependency loaders like [fetch-inject][40], so that no bundlers
are required.

When the complexity budget of your project allows for it, there is nothing wrong
with using Jquery, React or Vue for certain pages that are inherently complex
and dynamic.

## &lt;/article&gt;

Going through my notes, I realized I started drafting this post circa 2017,
when I first noticed the JS-all-the-things trend in the industry.

Four years later, the state of things hasn't gotten better, yet projects like
htmx are gaining traction for small / hobby projects, which is promising.

Maybe this post inspires you to start your next project as a MPA, instead of a
SPA, to avoid JS fatigue, save time and money.


[1]: https://lucasfcosta.com/2017/07/17/The-Ultimate-Guide-to-JavaScript-Fatigue.html
[2]: https://mckinley.cc/blog/20210831.html "Documents ≠ Programs"
[3]: https://jeffhuang.com/designed_to_last/ "This Page is Designed to Last"
[4]: https://htmx.org/essays/complexity-budget/ "Complexity Budgets"
[5]: https://htmx.org/essays/splitting-your-apis/ "Splitting Your Data & APIs: Going Further"
[6]: https://max.engineer/server-informed-ui "Don’t Build A General Purpose API To Power Your Own Front End"
[7]: https://intercoolerjs.org/2016/02/17/api-churn-vs-security.html "The API Churn/Security Trade-off"
[8]: https://intercoolerjs.org/2016/05/08/hatoeas-is-for-humans.html "HATEOAS is for Humans"
[9]: https://macwright.com/2020/05/10/spa-fatigue.html "Second-guessing the modern web"
[10]: http://wgross.net/essays/spas-are-harder "SPAs Are Just Harder, and Always Will Be"
[11]: https://svelte.dev/blog/virtual-dom-is-pure-overhead "Virtual DOM is pure overhead"
[12]: https://javascript.works-hub.com/learn/a-javascript-free-frontend-61275 "Developing a Javascript-free frontend"
[13]: https://www.gregnavis.com/articles/the-architecture-no-one-needs.html "The Architecture No One Needs"
[14]: https://paramaggarwal.substack.com/p/how-websites-evolved-back-to-static-html-css-js-files-57ce549f81db "How Websites Evolved Back to Static HTML/CSS/JS Files"
[15]: https://www.timr.co/server-side-rendering-is-a-thiel-truth "Server-Side Rendering is a Thiel Truth"
[16]: https://intercoolerjs.org/2016/05/08/hatoeas-is-for-humans.html "HATEOAS is for Humans"
[17]: https://calendar.perfplanet.com/2016/prefer-defer-over-async/ "Prefer DEFER Over ASYNC"
[18]: https://html.com/semantic-markup/ "What On Earth Is Semantic Markup? (And Why Should You Learn To Write It)"
[19]: https://3perf.com/blog/link-rels/ "Preload, prefetch and other <link> tags"
[20]: https://www.html5rocks.com/en/tutorials/responsive/picture-element/ "Built-in Browser Support for Responsive Images"
[21]: https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation "Client-side form validation"
[22]: https://addyosmani.com/blog/lazy-loading/ "Native image lazy-loading for the web!"
[23]: https://journal.plausible.io/you-probably-dont-need-a-single-page-app "You probably don't need a single-page application"
[24]: https://htmx.org/ "high power tools for HTML"
[25]: https://github.com/turbolinks/turbolinks "Turbolinks"
[26]: https://htmx.org/docs/#boosting "HTMX Boosting"
[27]: https://ricostacruz.com/nprogress/ "Nprogress.js"
[28]: http://www.chrisharrison.net/index.php/Research/ProgressBars2 "Faster Progress Bars: Manipulating Perceived Duration with Visual Augmentations"
[29]: http://instantclick.io/click-test "Instaclick | Click test"
[30]: https://instant.page/ "Make your site’s pages instant in 1 minute and improve your conversion rate noticeably."
[31]: http://instantclick.io/ "InstantClick is a JavaScript library that dramatically speeds up your website, making navigation effectively instant in most cases."
[32]: https://github.com/GoogleChromeLabs/quicklink "Quicklink"
[33]: https://htmx.org/extensions/preload/ "htmx | The preload Extension"
[35]: https://mitchel.me/slippers/docs/getting-started/ "Build reusable components in Django without writing a single line of Python."
[36]: https://www.django-unicorn.com/ "A magical full-stack framework for Django"
[37]: https://htmx.org/extensions/morphdom-swap/ "The morphdom-swap Extension"
[38]: https://alpinejs.dev/ "Your new, lightweight, JavaScript framework."
[39]: https://hyperscript.org/ "hyperscript is an easy and approachable language designed for modern front-end web development"
[40]: https://habd.as/post/managing-async-dependencies-javascript/ "Managing Async Dependencies with JavaScript"
[41]: https://github.com/utapyngo/django-render-partial "Django render partial"
