#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'hernantz'
SITENAME = u'what\'s the point'
SITEURL = 'http://hernantz.github.io'

TIMEZONE = 'America/Buenos_Aires'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_RSS = 'rss.xml'

# A list of tuples (Title, URL) for links to appear on the header.
LINKS = (('posts', '/'),)

# Social widget
SOCIAL = (('Twitter', 'http://twitter.com/hernantz'),
          ('Github', 'http://github.com/hernantz'),
          ('RSS', '/rss.xml'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = '/home/hernantz/devel/pelican-left/'

SITESUBTITLE = 'Mostly lies and rants in plain text'
