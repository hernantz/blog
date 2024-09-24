#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'hernantz'
SITENAME = 'README.txt'
SITESUBTITLE = '- Mostly lies and rants in plain text.'
SITEURL = 'localhost'

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
LINKS = (('readme', '/'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/hernantz'),
          ('github', 'http://github.com/hernantz'),
          ('last.fm', 'http://last.fm/user/hernantz'),
          ('tomatoes', 'https://www.rottentomatoes.com/user/id/973196678'),)

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = '/home/hernantz/devel/pelican-left/'

STATIC_PATHS = ('images', 'extra/robots.txt', 'extra/humans.txt', 'videos',)

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/humans.txt': {'path': 'humans.txt'},
    'extra/security.txt': {'path': 'security.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.toc': {'permalink': True}
    },
    'output_format': 'html5',
}

# SEO settings
SEO_REPORT = True
SEO_ENHANCER = True
SEO_ENHANCER_TWITTER_CARDS = True
SEO_ENHANCER_OPEN_GRAPH = True
