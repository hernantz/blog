Title: In the beginning there was static HTML
Date: 2013-10-02
Category: Internet
Tags: cache, internet 
Slug: in-the-beginning-there-was-static-html
Author: hernantz 
Summary: In the beginning there was static HTML, and it scaled
Status: draft


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
