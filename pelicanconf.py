#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'hernantz'
SITENAME = u'README.txt'
SITESUBTITLE = '- Mostly lies and rants in plain text.'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Buenos_Aires'
DATE_FORMATS = {
    'en': '%Y-%m-%d',
}

DEFAULT_LANG = 'en'

DEFAULT_PAGINATION = 20

DELETE_OUTPUT_DIRECTORY = True
OUTPUT_PATH = 'output/'
OUTPUT_RETENTION = ['.hg', '.git', '.bzr']

# Feed generation is usually not desired when developing
FEED_RSS = 'rss.xml'

# A list of tuples (Title, URL) for links to appear on the header.
LINKS = (('blog', '/'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/hernantz'),
          ('github', 'http://github.com/hernantz'),
          ('last.fm', 'http://last.fm/user/hernantz'),
          ('tomatoes', 'https://www.rottentomatoes.com/user/id/973196678'),)

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = '/home/hernantz/devel/pelican-left/'

STATIC_PATHS = ('images', 'extra/robots.txt', 'extra/humans.txt',)

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/humans.txt': {'path': 'humans.txt'},
    'extra/security.txt': {'path': 'security.txt'},
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
