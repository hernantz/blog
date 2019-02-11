Title: Pythonistas don't let pythonistas write Javascript
Date: 2017-05-25
Tags: python, javascript
Status: Draft



In the beginning there was static HTML, and it scaled.
Now the are lots of frameworks and services running fiercely to dinamically generate HTML.
It's great, but if your site happens to get an increasing amount of users, then you hire an expert
that will tell you "best practices" to turn your dinamically generated HTML into a
static one (mostly throw complex caching technique). Your site will scale again.
All the dynamicity is still there, but behind a caching wall.

Cacheable content requires to don't change very often and to be generic for all visitors.
The problem is that your perfectly cacheable content has some dinamically changing pieces, like the
welcome user22!. This could be fixed with some Javascript of course.

Now, going a bit further. Im not downloading my phone apps every time I enter them,
I just get the bits of data that make it seem alive and kicking. Do I need to download Youtube HTML
every time I visit it? or would it make more sense to install the app and follow the
pattern mentioned above?

Makes me wonder if at some point it would be better to get back to roots and
build HTML with a static site generator or force the site to be installed to be consumed.
Shall we compare the traffic generated from a chached website vs an installed version
of the site (be it a native app or an installed webapp) to arrive to a conclusion.

Poner imagen de jesus rompiendo los puestos en el mercado
Poner imagen del principito

casi siempre la principal justificacion para hacer una SPA es la fuidez en la exp de usuario que se logra. Yo opino que podes llegar a algo parecido con turbolinks, prefetch, caching, etc + algunos widgets en js
sobre todo considerando que el 90% de los sitios son forms + texto
y eso es un problema ya resuelto ^

React vs Marionettejs
Reducers: Object es un controller disponible como singleton
Actions -> radio requests

http://blog.mattwoodward.com/2015/02/dynamically-adding-forms-to-and.html
http://wgross.net/essays/spas-are-harder
https://sonniesedge.co.uk/blog/a-day-without-javascript
https://www.theatlantic.com/technology/archive/2017/02/why-some-apps-use-fake-progress-bars/517233/?single_page=true
https://micro-frontends.org/

https://blog.mgechev.com/2018/05/09/introducing-guess-js-data-driven-user-experiences-web/
https://www.youtube.com/watch?v=eEVRapHQFKI
https://www.django-rest-framework.org/topics/html-and-forms/

los bundles de webpack son lo mismo que cargar las paginas de antes

Modernizr v3.6 and Normalize

cache de partes renderizadas?

https://daverupert.com/2015/12/intrinsic-placeholders-with-picture/

You don't need javascript
- server side rendering: https://news.ycombinator.com/item?id=14776780 (for fast initial loads and no caveats around SEO)
- js minimo https://www.engineyard.com/blog/using-jquery-with-rails-how-to
- turbolinks & preload attr
  native datepickers in firefox
- pjax
- ajax forms
- https://jspm.io/
- stimulus https://m.signalvnoise.com/stimulus-1-0-a-modest-javascript-framework-for-the-html-you-already-have-f04307009130
- offline views -> caching?
- new tags for progressive images https://www.html5rocks.com/en/tutorials/responsive/picture-element/ o https://jmperezperez.com/medium-image-progressive-loading-placeholder/ http://daverupert.com/2015/12/intrinsic-placeholders-with-picture/
- ajax snippets
- minimal dependency injection https://hackcabin.com/post/managing-async-dependencies-javascript/
- http://antulik.com/2016-10-02-parallel-rendering-in-rails.html
- https://semaphoreci.com/blog/2017/06/08/speeding-up-rails-pages-with-render-async.html
- http://www.chrisharrison.net/index.php/Research/ProgressBars2
https://unpoly.com/
https://www.oreilly.com/ideas/its-time-to-rebuild-the-web
http://intercoolerjs.org/docs.html
https://www.256kilobytes.com/content/show/4399/get-these-dependencies-off-my-lawn-5-tasks-you-didnt-know-could-be-done-with-pure-html-and-css
