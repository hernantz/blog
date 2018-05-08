Title: One config.py to config them all
Summary: How to do configuration management.
Date: 2018-05-05
Category: Programming
Tags: python, best-practices, configuration, architecture, django

![configuration management](/images/configuration.png "Configuration management")


Configuration allows us to modify the behavior of our software based on a
number of settings, with the goal of providing more flexibility to the users of
such software.

Configuration management is an important aspect of the architecture of any
system. But it is sometimes overlooked.

The purpose of this post is to explore a proposed solution for proper config
management in general, and for a python app in particular.


## Types of configuration

Hold on a moment. Configuration understood as a mechanism of altering the state
and behavior of a program can be very broad.

We are interested in the *deterministic configuration* that presets the state
of a program, without having to interact with it, like static config files or
envirionment variables.

On the other hand, there's the *runtime configuration*, which happens when the
user interacts with the system. User preferences are a typical example of this
kind.

It may not always apply, but a general rule of thumb is to separate config by
how it affects code: Code that varies depending on where it is run (static),
as oposed on how it is used (runtime).

We make the distiction because the later is not very general and is up to the
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

Imagine if `sqlalchemy` gathered it's engine configuation from an environment
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
is because config varies substantially across deploys and executions, code does
not. The same code can be run inside a container or in a regular machine, it
can be executed in production or in testing environments.


### Where to get configuration from

[Environment variables][0] are important. But we have to be careful on how we use
them. Why not use environment variables directly? There is a common pattern to
read configurations in environment variable that look similar to the code
below:

```python
if os.environ.get("DEBUG", False):
    print(True)
else:
    print(False)
```

But this code have some issues:

if env var `DEBUG=False` this code will print `True` because
`os.environ.get("DEBUG", False)` will return an string `‘False’` instead of a
boolean `False`. And a non-empty string has a `True` boolean value. We can’t
(dis|en)able debug with env var `DEBUG=yes|no`, `DEBUG=1|0`,
`DEBUG=True|False`. We need to start casting/parsing everywhere.

If we want to use this configuration during development we need to define this
env var all the time. We can’t define this setting in a configuration file that
will be used if `DEBUG` envvar is not defined.

We also face another issue. If we need to configure an application and also
some specific processes of that application, we don't have a hierarchical way
of defining system-wide vs process-specific settings. This would force us to
give every process a full copy of all global + overwritten settings.

Well designed applications allow different ways to be configured. A proper
settings-discoverability chain goes as follows:

1. cli args
2. environment variables
3. Config files in different directories
4. Hardcoded constants

The rises the need to consolidate configuration in a single source of truth to
avoid having config management scattered all over the codebase. 

All this configuration management should be handled before the program starts,
to avoid parsing files, or passing CLI args everywhere. So ideally we would
have a single settings.py file where configuration is
gathered/parsed/processed. The app imports that config module and distributes
it to all the different libraries it is using.

An example startup script for your app could be:

```python
import sys
import os
from settings import gather_settings

if __name__ == '__main__':
    conf = gather_settings(sys.argv, os.environ, open('config_file').read())
    main(conf)  # conf is a dict of settings
```


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
PLUGINS = BASE_PLUGINS + EXTRA_PLUGINS
```

which gets its config from a local ini file for example:

```ini
# config.ini for everyone
BASE_PLUGINS = ['foo', 'bar']
EXTRA_PLUGINS = []


# config.ini for developers
EXTRA_PLUGINS = ['baz']
```

This way the only thing that changes is pure configuration variables, but the
same configuration code gets executed everywhere. We also were able to separate configuration from code:
which allows us to:

1. Ship configuration separately from code. There is no need to modify code in
   order to change it's behavior.
2. Plain text files are *universal*. Can be edited with any text editor, no
   need to mess with db connectors/sql/scripts to configure an app.
3. No need to know a programming language to configure the app. [Vagrant][3],
   for example, uses Ruby for it's `Vagrantfile`, it is a bummer to have to
   learn the syntax of a language just to use a tool.


### The `settings.template` trick

We still need a way to bundle settings for different environments: QA, stating,
production, test, Bill's dev machine, etc

Config files are very convenient since they can be version-controlled, can be
put into templates by Config Management/Orchestration tools and come handy when
developing. It is also possible to put ENV VARS into a file that gets loaded
before the program starts. The convention is to put configuration in `.env`
files. Many tools that manage processes/containers, like docker-compose and
systemd, have support for loading them.

A litmus test for whether an app has all config correctly factored out of the
code is whether the codebase could be made open source at any moment, without
compromising any credentials.


### Devops tools

Code needs to be [packaged, distributed, installed, executed][4].

These are all steps that make use of external tools that are not part of the
codebase and should be replaceable. An app could be packaged for Ubuntu or
Windows differently, can be installed manually or put in a container. For this
reason, code should be as agnostic of these steps as possible and delegate that
to another actor called: *Installer/Builder*.

This new actor can be one or many tools combined, for example docker-compose,
yum, gcc, ansible, etc.

The installer actor is the one that knows how to bind code with the right
configuration it needs and how to do it (through env vars or files or cli args
or all of them). Because it knows the configuration it needs to inject into the
project, it makes a good candidate to manage configuration.  It can do so by
having configuration templates for files or settings that will be injected into
the environment, it knows about keeping secret/sensistive information
protected, etc.

The dev(ops) flow has two clearly distinct realms:

```
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

If you use different tools when developing and when deploying, all these
scripts and templates will start to increse in number. When that moment comes,
there will be the temptation to delegate all this responsability to the app to
"autoconfigure and install itself".

Sometimes an app not only needs to be configured, but it might need [other
services to be running][1], so you'll have to replace an orchestration tool and
a supervisor. This basically means that you will be replacing specialiced tools
with battle-tested ready-made solutions with your own implementation. More
code, mode problems.

Ideally, a project should support [one build tool][2] and use it for
development and production. For example: docker everywhere.

The important thing to note here is that the application's code should not
install dependencies or start services or export variables to the environment
because an external service needs them.


### Managing config changes

consult template -> places template -> emits reload signal -> program picks up new config
reload config signal (reload(config))
Database based configuration can bring the chickend and egg problem, for a large system.
Sqlite can be usefull for some programs, to store configuration provided by a non technical user (like screen resolution for counter strike).
But for a program to scale in a cluster, it is better not to force any db/connector/table/etc, by just issuing a file and and accepting reload.

how to dynamically update settings (process signals?)
How to reload program when config changes with systemd?


## Proposed architechture

Always use a single config.py file and load it before starting the program. Use
prettyconf since it follows this architecture (or will soon:
https://github.com/osantana/prettyconf/issues/18).  Configuration for other
services should be handled separately.  Keep in mind what belongs to which
realm when writing code/scripts. Everything can live in the same repo, but at
least they will be in different folders (src and ops, for example).
Consolidate a very similar set of tools for dev and production envs. Containers
are gaining popularity everywhere, we can either use docker/ansible-container
for both realms.  Ansible container:
https://github.com/ansible/ansible-container Docker: https://www.docker.com/


------


Introducing prettyconf

https://en.wikipedia.org/wiki/Windows_Registry

<zoredache> hernantz: maybe make an example vars file or something that is in the vcs, then instruct the devs to copy+populate the template to a name that is excluded by a gitignore?
Problem with this is that from time to time settings names might change, and when switching to that branch you have to manually change settings file that is not versioned.
Si las configs son como una base de datos en un archivo, por ahi puede existir un modelo que las represente y tener un sistema de migraciones entre schemas.

How to manage secrets for tests (should not be secrets, because testing should not have any dangerous side effect) the same applies for continuous integration tools.


[0]: https://12factor.net/config "The twelve-factor app | config"
[1]: https://12factor.net/backing-services "The twelve-factor app | backing services"
[2]: https://12factor.net/dev-prod-parity "The twelve-factor app | dev/prod parity"
[3]: https://www.vagrantup.com/docs/vagrantfile/ "Vagrantfile"
[4]: https://12factor.net/build-release-run "The twelve-factor app | build, release, run"
