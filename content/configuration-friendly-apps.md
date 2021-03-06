Title: Configuration-friendly apps
Summary: Some guidelines for config management in general and Python apps in particular.
Date: 2018-05-11
Category: Programming
Tags: python, best-practices, configuration, architecture, tools

![configuration management](/images/configuration.png "Configuration management")

Configuration is just another API of your app. It allows us to preset or modify
it's behavior based on where it is installed and how it will be executed,
providing more flexibility to the users of such software.

Configuration management is an important aspect of the architecture of any
system. But it is sometimes overlooked.

The purpose of this post is to explore a proposed solution for proper config
management in general, and for a python app in particular.


## Types of configuration

Hold on a moment. Configuration understood as a mechanism of altering the state
and behavior of a program can be very broad.

We are interested in the *deterministic configuration* that presets the state
of a program, without having to interact with it, like static config files or
environment variables.

On the other hand, there's the *runtime configuration*, which is set when the
user interacts with the system. User preferences are a typical example of this
kind.

It may not always apply, but a general rule of thumb is to separate config by
how it affects code: Code that varies depending on where it is run (static),
as oposed on how it is used (runtime).

We make the distinction because the later is not very general and is up to the
developer to decide how to manage it. If it is a desktop app, a file or a
sqlite database might suffice, but for a cloud app, maybe a distributed
key-value store is needed.


## Project (app) vs Library

The first thing to determine is the type of software that needs to be
configured. There is a difference between configuring a library vs configuring
a project.

Lets see an example of how `sqlalchemy`, a database toolkit library, provides
us with the needed building blocks for us to use as we please.

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 
# Engine used to store data
engine = create_engine('sqlite:///sqlalchemy_example.db')
 
# Create all tables in the engine.
Base.metadata.create_all(engine)
```

A library is meant to be a reusable piece of code that should not make
assumptions on where and how it is going to be used. 

Imagine if `sqlalchemy` gathered it's engine configuration from an environment
variable `SQLALCHEMY_ENGINE=sqlite:///sqlalchemy_example.db` or a file in
`/etc/sqlalchemy/engine.cfg`. It would be complicated for an app reuse that
library to connect to different databases.

For this reason a library should be only configured through code, and never
require env variables or configuration files to exist in order to be used. 

A project might use many libraries that require different configs (a database
connector, s3 storage, etc). So it is in charge of gathering required config
and using these libraries.

In this case, it is the app's responsibility to gather the connection settings
and use the library to connect to two separate databases, because the app knows
what it needs, not the library.


## How to configure a project (or application)

It is important to provide a clear separation of configuration and code. This
is because config varies substantially across deploys and executions, code
*should* not. The same code can be run inside a container or in a regular
machine, it can be executed in production or in testing environments.


### Where to get configuration from

Configuration for a project might come from different sources, like `.ini`
files, envirionment variables, etc.

For example, there is a common pattern to read configurations in environment
variables[^0] that look similar to the code below:

```python
if os.environ.get("DEBUG", False):
    print(True)
else:
    print(False)
```

Why is getting config variables directly a bad idea?

If env var `DEBUG=False` this code will print `True` because
`os.environ.get("DEBUG", False)` will return an string `‘False’` instead of a
boolean `False`. And a non-empty string has a `True` boolean value. We can't
(dis|en)able debug with env var `DEBUG=yes|no`, `DEBUG=1|0`,
`DEBUG=True|False`. We need to start casting/parsing everywhere.

If we want to use this configuration during development we need to define this
env var all the time. We can't define this setting in a configuration file that
will be used if `DEBUG` envvar is not defined.

Well designed applications allow different ways to be configured. A proper
settings-discoverability chain goes as follows:

1. CLI args, mostly used to allow users do some exploration while running your program.
2. Environment variables, that can be set in `.bashrc` or `.env` files and, since they are global, they should have some sort of prefix like `MYAPP_*`.
3. Config files in different directories, that also imply some hierarchy. For
   example: config files in `/etc/myapp/settings.ini` are applied system-wide,
   while `~/.config/myapp/settings.ini` take precedence and are user-specific.
4. Hardcoded constants.

The rises the need to consolidate configuration in a single source of truth to
avoid having config management scattered all over the codebase. 

All this configuration management should be handled before the program starts,
to avoid parsing files, or passing CLI args everywhere. So ideally we would
have a single `config.py` file where settings are gathered, parsed and
processed. The app imports that config module and distributes it to all the
different libraries it is using.

An example startup script for your app could be:

```python
import argparse
import os
import configparser
from app import main
from collections import ChainMap

defaults = {'debug': False}

parser = argparse.ArgumentParser()
parser.add_argument('--debug')
args = parser.parse_args()
cli_args = {key: value for key, value in vars(args).items() if value}

iniparser = configparser.ConfigParser()
iniparser.read(['/etc/app/config.ini', os.path.expanduser('~/.myapp.ini')]
ini = iniparser['app']

config = ChainMap(cli_args, os.environ, ini, defaults)

if __name___ == '__main__':
    main(config)
```

This snippet uses `ChainMap`[^2] to lookup values in different dictionary-like objects. To our convenience, the `configparser` module has builtin support to read multiple `.ini` files and merge them.


### A single executable file

Another anti-pattern to be aware of is having as many configuration modules as
environment there are:  `dev_settings.py`, `staging_settings.py`,
`local_settings.py`, etc, and including different logic on them.

A very simple example of custom logic is:

```python
# base_settings.py
PLUGINS = ['foo', 'bar']


# dev_settings.py
from base_settings import *
PLUGINS = PLUGINS + ['baz']
```

Should be a single `settings.py`:


```python
# settings.py
config = ConfigParser('config.ini')

# this is what the app uses
PLUGINS = config['BASE_PLUGINS'] + config['EXTRA_PLUGINS']
```

Which gets its config from a local ini file for example:

```ini
# /etc/app/config.ini for everyone
BASE_PLUGINS = foo,bar

# ~/.config/app/config.ini that a user overrides based on the template
EXTRA_PLUGINS = baz
```

This way the only thing that changes is pure configuration variables, but the
same configuration code gets executed everywhere. We also were able to separate
configuration from code, which gives us some nice features:

1. Ship configuration separately from code. There is no need to modify code in
   order to change it's behavior.
2. Plain text files are *universal* [^4]. Can be edited with any text editor,
   no need to mess with db connectors/sql/scripts to configure an app.
3. No need to know a programming language to configure the app. [Vagrant][3],
   for example, uses Ruby for it's `Vagrantfile`, it is a bummer to have to
   learn the syntax of a language just to use a tool.
4. Since config files are not executable, they can partially override other
   config files in a line of hierarchy, as opposed to `.vimrc` files for
   example, that are executable and have to be *forked* to be adapted and a
   base config cannot be shared for all users in the system).

The example of configuring plugins is not accidental. The idea is to show that
if you need to enable the user to do some scripting as customization, do so
through a plugin system, but never through scriptable config files.


### The `settings.template` trick

We still need a way to bundle settings for different environments: QA, stating,
production, test, Bill's dev machine, etc

Also, a litmus test for whether an app has all config correctly factored out of
the code is whether the codebase could be made open source at any moment,
without compromising any credentials. What this means is that credentials and
secrets should also be kept outside the codebase and made configurable.

So secrets and environment dependant settings have to be handled somehow.

Config files are very convenient since they can be version-controlled, can be
put into templates by Config Management/Orchestration tools and come handy when
developing.

Following the example above, a `config.ini.template` could look like this:

```ini
# config.ini.template that each environment can implement
#
# EXTRA_PLUGINS = one_plugin,another_plugin
# SECRET_KEY = <change me>
```

Even env vars can be put into a file (typically named `.env`) that gets loaded
before the program starts. Many tools that manage processes/containers, like
[docker-compose][5] and [systemd][6], or even [libraries][8] have support for
loading them.

It is common practice to put an example `settings.template` file that is in the
VCS, and then provide a way to copy + populate that template to a name that is
excluded by your VCS so that we never accidentally commit that. These files
might also be tracked by VCS, but encrypted, like it is done with [Ansible
Vault][9].


### Devops tools

Code needs to be [packaged, distributed, configured, installed, executed and
monitored][4].

These are all steps that make use of [external tools][16] that are not part of the
codebase and should be replaceable. An app could be packaged for Ubuntu or
Windows differently, can be installed manually or put in a container. For this
reason, code should be as agnostic of these steps as possible and delegate that
to another actor called: *Installer/Builder*.

This new actor can be one or many tools combined, for example `docker-compose`,
`yum`, `gcc`, `ansible`, etc.

The installer actor is the one that knows how to bind code with the right
configuration it needs and how to do it (through env vars or files or cli args
or all of them). Because it knows the configuration it needs to inject into the
project, it makes a good candidate to manage configuration templates for
files, vars that will be injected into the environment, or how to keep
secret/sensitive information protected.

The development and operations flow has two clearly distinct realms:

```python
+-------+           +-------+          +--------+         +-------+         +-------+
|       |           |       |          |        |         |       |         |       |
| code  +---------->| build +--------->|        |<--------+service|<--------+ conf  +
|       |           |       |          |        |         |       |         |       |
+-------+           +-------+          |        |         +-------+         +-------+
                                       |        |
                    +-------+          |        |         +-------+         +-------+
                    |       |          |        |         |       |         |       |
                    | conf  +--------->|release |<--------+service|<--------+ conf  +
                    |       |          |        |         |       |         |       |
                    +-------+          |        |         +-------+         +-------+
                                       |        |
                    +-------+          |        |         +-------+         +-------+
                    |       |          |        |         |       |         |       |
                    | deps  +--------->|        |<--------+service|<--------+ conf  +
                    |       |          |        |         |       |         |       |
                    +-------+          +--------+         +-------          +-------+

+-------------------+---------------------------------------------------------------+
|    code realm     |                   Devops/CM/Orchestraion realm                |
+-------------------+---------------------------------------------------------------+
```

Notice that developers are also users of the software, that need to configure
it and are constantly doing micro-releases while developing.

If you use different tools when developing and when deploying, all these
scripts and templates will start to increase in number. Ideally, a project
should support [one set of build tools][2] and use it for development and
production. For example: docker everywhere.


### Managing config changes

Ideally, programs should have the ability to be notified when there are new 
configs to be picked up.

This is possible if configuration is provided through files, not so easy if we
used environment vars or CLI arguments, in which case we would have to restart
the program.

The [SIGHUP signal][7] is usually used to trigger a reload of configurations
for daemons.

In Python, this can be achieved with the `signal` module, as the following gist shows:

```python
import os
import signal

def get_config(rel=False):
    import config
    if rel:
        reload(config)
    return config

running = True

def run():
    while running:
        # do something with get_config().foo
    else:
        # teardown

def signal_handler(signum, frame):
    # Use kill -15 <pid>
    if signum == signal.SIGTERM:
        global running
        running = False  # terminate daemon

    # kill -1 <pid>
    elif signum == signal.SIGHUP:
        get_config(rel=True)  # reload config


signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    run()
```

Then, the program can be notified about new config by using `kill -1` or, with
systemd:

```sh
$ sudo systemctl reload application.service
```

If the app is part of a distributed cloud system, the same principle can still
be used. For example, Consul, a tool for service and configuration discovery
provides `consult-template`, a command to populate values from Consul [^3] into
automatically [updated templates][11] that can emit reload commands to programs
to pick it up.

```sh
$ consul-template \
    -template "/tmp/nginx.ctmpl:/var/nginx/nginx.conf:nginx -s reload" \
    -template "/tmp/redis.ctmpl:/var/redis/redis.conf:service redis restart" \
    -template "/tmp/haproxy.ctmpl:/var/haproxy/haproxy.conf"
```

As you can see, there is another tool in charge of managing configuration, building it and notifying our code about it.


## Introducing prettyconf

[Prettyconf][15] is a framework agnostic python library created to make easy
the separation of configuration and code. It lets you use the principles we
discribed about configuration-discovery.

```python
import argparse
from prettyconf import Configuration
from prettyconf.loaders import CommandLine, Environment, IniFile


parser = argparse.ArgumentParser()
parser.add_argument('--debug')

system_config = '/etc/myapp/config.ini'
user_config = '~/.config/myapp.ini'

config = Configuration(
    loaders=[
        CommandLine(parser=parser),
        Environment(),
        IniFile(user_config),
        IniFile(system_config)
    ]
)

DEBUG_MODE = config('debug', cast=config.boolean, default=False)
```

With the snippet above, the `debug` config will be discovered from the command
line args, the environment or different `.ini` files, even following good naming
conventions, like checking for `DEBUG` in the environment but `debug` in the
ini files, and pasing that to a boolean. All these loaders are optional, and
won't fail if the files are missing.

With prettyconf there are no excuses not to follow best pratices for
configuration management in your app [^1].


## Conclusions

Don't take responsibility of gathering configuration when developing a library.

In your app, always use a single `config.py` file that gathers all settings and
load it before starting the program.

Keep in mind what belongs to which realm when writing code/scripts. Everything
can live in the same repo, but at least they will be in different folders
(`src/` and `ops/`, for example). Configuration for each service (Nginx,
Postgresql, etc) should be handled separately, by specialized tools.

And speaking of tools, consolidate a very similar set of tool for dev and
production envs.  Containers are gaining popularity everywhere, use something
like [docker][13] or [ansible-container][14] for both realms.


[^0]: They are [very common][0], specially among cloud platforms, like AWS lambda
      functions. It's one of the simplest ways for configuring programs without the
      need to mess with files (which requires access to a filesystem) or CLI parsers,
      since this ENV vars are available as is, like an already parsed config file.

[^1]: Now, not everything that is configuration should me handled through prettyconf.
      For example, [lektor][12] is a flat-file cms, that lets you define the models
      in `.ini` files. This type of configuration that goes beyond doing a setting's
      key lookup, should be handled apart from prettyconf.

      Another responsability that doesn't belong to prettyconf is populating
      configuration files of setting variables in the environment, since it is
      someone else's duty, like [python-dotenv][18].

[^2]: Turns out that using `ChainMap` you can implement this very simple
      [lookup algorithm][17].

[^3]: A nice thing about `consul-template` is that it let's you use the same
      configuration system on any environment. So when developing locally, you
      don't care about Consul, you app simply reads a config file. When in
      production, you can inject dynamic settings and [even secrets][18] to the app
      lookup algorithm.

[^4]: The problem with using something other than plain text files is that you
      will necessarily have to execute a program in order to get the desired
      configuration out of it. A programming language has control structures, can
      make calls to the internet, etc, so you can't known in advance the output you
      will get. [PEP518][21] is a proposal to use a TOML file for this and other
      issues.

      Take as an example python's `setup.py`. You can't execute a `setup.py`
      file without knowing its dependencies, but currently there is no standard
      way to know what those dependencies are in an automated fashion without
      executing the `setup.py` file where that information is stored.

      Another application that faces a similar problem is Vim with it's
      `.vimrc` file, it's written in a custom language called `VimL`. The [Xi][20]
      editor, fixed this problem by switching to TOML files and plugins for
      extending functionality.


[0]: https://12factor.net/config "The twelve-factor app | config"
[1]: https://12factor.net/backing-services "The twelve-factor app | backing services"
[2]: https://12factor.net/dev-prod-parity "The twelve-factor app | dev/prod parity"
[3]: https://www.vagrantup.com/docs/vagrantfile/ "Vagrantfile"
[4]: https://12factor.net/build-release-run "The twelve-factor app | build, release, run"
[5]: https://docs.docker.com/compose/env-file/ "Declare default environment variables in file"
[6]: https://coreos.com/os/docs/latest/using-environment-variables-in-systemd-units.html "Using environment variables in systemd units"
[7]: https://en.wikipedia.org/wiki/Signal_(IPC)#SIGHUP "Posix signals"
[8]: https://github.com/theskumar/python-dotenv "python-dotenv"
[9]: https://docs.ansible.com/ansible/2.4/vault.html "Ansible Vault"
[10]: https://www.consul.io/ "Consul"
[11]: https://vimeo.com/109626825 "Consul template demo"
[12]: https://www.getlektor.com/ "Lektor"
[13]: https://www.docker.com/ "Docker"
[14]: https://github.com/ansible/ansible-container "Ansible Container"
[15]: https://github.com/osantana/prettyconf "Prettyconf"
[16]: https://twitter.com/raymondh/status/1039628786491248640
[17]: https://blog.florimondmanca.com/a-practical-usage-of-chainmap-in-python
[18]: https://github.com/theskumar/python-dotenv
[19]: https://www.hashicorp.com/blog/why-we-need-dynamic-secrets "Why we need dynamic secrets"
[20]: https://xi-editor.io/xi-editor/docs/config.html "Xi editor"
[21]: https://www.python.org/dev/peps/pep-0518/
