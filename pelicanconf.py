#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'hernantz'
SITENAME = u'what\'s the point'
SITESUBTITLE = 'Mostly lies and rants in plain text'
SITEURL = ''

TIMEZONE = 'America/Buenos_Aires'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_RSS = 'rss.xml'

# A list of tuples (Title, URL) for links to appear on the header.
#LINKS = (('posts', '/'),
         #('foodly', 'http://foodly.com.ar'),)

# Social widget
SOCIAL = (('Twitter', 'http://twitter.com/hernantz'),
          ('Github', 'http://github.com/hernantz'),
          ('RSS', '/rss.xml'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = '/home/hernantz/devel/pelican-left/'

STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/humans.txt',]

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/humans.txt': {'path': 'humans.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

PLUGIN_PATHS = ['/home/hernantz/devel/pelican-plugins']
PLUGINS = ['sitemap']
