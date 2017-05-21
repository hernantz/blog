#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'hernantz'
SITENAME = u'README.txt'
SITESUBTITLE = '- Mostly lies and rants in plain text.'
SITEURL = ''

TIMEZONE = 'America/Buenos_Aires'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_RSS = 'rss.xml'

# A list of tuples (Title, URL) for links to appear on the header.
LINKS = (('blog', '/'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/hernantz'),
          ('github', 'http://github.com/hernantz'), )

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = '/home/hernantz/devel/pelican-left/'

STATIC_PATHS = ('images', 'extra/robots.txt', 'extra/humans.txt',)

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/humans.txt': {'path': 'humans.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

PLUGIN_PATHS = ['/home/hernantz/devel/pelican-plugins']
PLUGINS = ['sitemap']

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.toc': {'permalink': True}
    }
}
