Title: Djangonauts don't let djangonauts write Javascript
Date: 2017-05-25
Category: Programming
Tags: python, django, javascript
Status: Draft


## Yet another Javascript rant

> JS Fatigue happens when people use tools
> they don't need to solve problems they
> don't have.
>
> <cite> ― Lucas F. Costa, [The Ultimate Guide to JavaScript Fatigue: Realities of our industry][1]</cite>


You probably don't need a SPA.


Sometimes it feels like you could hide in a bunker for 2 years, come out again,
to find out thousands of overengeneered frameworks and libraries that bloomed
and died solving the same old problems, state management and view rendering,
most of the time.


A woodsman was once asked, “What would you do if you had just five minutes to
chop down a tree?” He answered, “I would spend the first two and a half minutes
sharpening my axe.”

The desing of your forms would probably have to change a bit, for example, mark
all checkbox of todo items before hitting "mark a done" instead of marking them
as done as soon as you check their checkbox, or set all filters you need before
hitting "Apply Filters", instad of filtering as soon as you change them.

Yes, there is some overhead of rendering on the server side and sending extra
bits of html that you wouldn't have to if you compresed all that html into a
bundle.js (couple megabytes heavy) all at once, plus many json api calls, to
use the user's cpu time to generate the template.

That could be mitigated by using partial caching inside the page.


When building websites, some latency is expected. Use that to your favor!

https://timr.co/server-side-rendering-is-a-thiel-truth
JAM stack https://paramaggarwal.substack.com/p/how-websites-evolved-back-to-static-html-css-js-files-57ce549f81db


## Welcome user22!

In the beginning there was static HTML, and it scaled. Now the are lots of
frameworks and services running fiercely to dinamically generate HTML.  It's
great, but if your site happens to get an increasing amount of users, then
you hire an expert that will tell you "best practices" to turn your
dinamically generated HTML into a static one (mostly throw complex caching
technique). Your site will scale again.  All the dynamicity is still there,
but behind a caching wall.

Cacheable content requires to don't change very often and to be generic for
all visitors.  The problem is that your perfectly cacheable content has some
dinamically changing pieces, like the welcome user22!. This could be fixed
with some Javascript of course.

Now, going a bit further. Im not downloading my phone apps every time I enter
them, I just get the bits of data that make it seem alive and kicking. Do I
need to download Youtube HTML every time I visit it? or would it make more
sense to install the app and follow the pattern mentioned above?

Makes me wonder if at some point it would be better to get back to roots and
build HTML with a static site generator or force the site to be installed to
be consumed.  Shall we compare the traffic generated from a chached website
vs an installed version of the site (be it a native app or an installed
webapp) to arrive to a conclusion.

- ajax loaded html snippets (hello hernantz section that is not cachable) (https://github.com/dimkoug/tododjangoccb/blob/master/tododjangoccbv/cms/ajax_views.py)
- cache de partes renderizadas, por ejemplo una lista con los ultimos blog posts?
- http://antulik.com/2016-10-02-parallel-rendering-in-rails.html
- https://semaphoreci.com/blog/2017/06/08/speeding-up-rails-pages-with-render-async.html

## Loading scripts

- los bundles de webpack son lo mismo que cargar las paginas de antes
- https://jspm.io/
- https://calendar.perfplanet.com/2016/prefer-defer-over-async/
- https://github.com/bohdyone/adm.js


## The ilusion of speed
- offline views -> caching?
- https://css-tricks.com/prefetching-preloading-prebrowsing/
- js minimo https://www.engineyard.com/blog/using-jquery-with-rails-how-to
- turbolinks & preload attr (https://3perf.com/blog/link-rels/)
- pjax
- https://daverupert.com/2015/12/intrinsic-placeholders-with-picture/
- http://www.chrisharrison.net/index.php/Research/ProgressBars2
- https://instant.page/


## Maybe you don't need javascript at all
- https://javascript.works-hub.com/learn/a-javascript-free-frontend-61275
- https://addyosmani.com/blog/lazy-loading/
- https://www.256kilobytes.com/content/show/4399/get-these-dependencies-off-my-lawn-5-tasks-you-didnt-know-could-be-done-with-pure-html-and-css
  native datepickers in firefox
- new tags for progressive images https://www.html5rocks.com/en/tutorials/responsive/picture-element/ o https://jmperezperez.com/medium-image-progressive-loading-placeholder/ http://daverupert.com/2015/12/intrinsic-placeholders-with-picture/


## Unobstrusive js

- stimulus https://m.signalvnoise.com/stimulus-1-0-a-modest-javascript-framework-for-the-html-you-already-have-f04307009130
- minimal dependency injection https://habd.as/post/managing-async-dependencies-javascript/
http://blog.mattwoodward.com/2015/02/dynamically-adding-forms-to-and.html

Poner imagen de jesus rompiendo los puestos en el mercado
Poner imagen del principito
https://github.com/VVyacheslav/django-rest-framework-datatables-editor
casi siempre la principal justificacion para hacer una SPA es la fuidez en la
user experience que se logra. Yo opino que podes llegar a algo parecido con
turbolinks, prefetch, caching, etc + algunos widgets en js sobre todo
considerando que el 90% de los sitios son forms + texto y eso es un problema ya
resuelto ^

React vs Marionettejs
Reducers: Object es un controller disponible como singleton
Actions -> radio requests

https://chanind.github.io/rails/2019/03/28/why-i-miss-rails.html
http://wgross.net/essays/spas-are-harder
https://dev.to/winduptoy/a-javascript-free-frontend-2d3e
https://sonniesedge.co.uk/blog/a-day-without-javascript
https://www.theatlantic.com/technology/archive/2017/02/why-some-apps-use-fake-progress-bars/517233/?single_page=true
https://micro-frontends.org/
https://github.com/systemjs/systemjs

https://blog.mgechev.com/2018/05/09/introducing-guess-js-data-driven-user-experiences-web/
https://www.youtube.com/watch?v=eEVRapHQFKI
https://www.django-rest-framework.org/topics/html-and-forms/


Modernizr v3.6 and Normalize

-https://arp242.net/jquery.html
- https://www.pikapkg.com/blog/pika-web-a-future-without-webpack/#
- server side rendering with Jinja: https://news.ycombinator.com/item?id=14776780 (for fast initial loads and no caveats around SEO)
- ajax forms
https://unpoly.com/
https://www.oreilly.com/ideas/its-time-to-rebuild-the-web
http://intercoolerjs.org/docs.html -> https://htmx.org/
https://engineering.instawork.com/iterating-with-simplicity-evolving-a-django-app-with-intercooler-js-8ed8e69d8a52
https://journal.plausible.io/you-probably-dont-need-a-single-page-app
https://alistapart.com/article/responsible-javascript-part-1/
https://www.pika.dev/cdn (reducir babel y polyfills)
https://macwright.org/2020/05/10/spa-fatigue.html
https://solovyov.net/blog/2020/a-tale-of-webpage-speed-or-throwing-away-react/

[1]: https://lucasfcosta.com/2017/07/17/The-Ultimate-Guide-to-JavaScript-Fatigue.html
