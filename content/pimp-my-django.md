Title: Pimp my Django
Date: 2018-10-02
Category: Programming
Tags: django, docker, python, configuration, best-practices, tools
Summary: An opinionated guide to setup Django with Docker and Pipenv.
Status: draft

https://hynek.me/articles/python-app-deps-2018/
https://github.com/pypa/pipenv/issues/3285

# Managing dependencies

There are 3 main strategies:

- Without venv
- With venv inside the container
- With venv outside the container

# Configuration
Use `.env` file.

# For production
Another image without build tools, just the venv with production dependencies.

Docker ONBUILD

[1]: http://blog.getpelican.com/
