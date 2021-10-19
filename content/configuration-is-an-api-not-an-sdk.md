Title: Configuration is an API, not an SDK
Date: 2020-06-27
Category: Programming
Tags: python, best-practices, tools, configuration, architecture
Summary: A configuration architecture for the working dev.

![Control room | photo by @patrykgradyscom at Unsplash](/images/control-room.jpg "Control room | photo by @patrykgradyscom at Unsplash")

Configuration is every setting that needs to change based on the environment
where the app is executed. It helps you *preset* the state of your app, without
having to change the code. This is why it is important to provide a clear
separation of configuration and code.


## Why are executable config files a bad idea?

[Configuration is just another API][1] of your app.

It might be used by people with or without technical skills, that install or run
your app.

Executable files can be used as config sources like `.vimrc` for Vim,
`Vagrantfile` for Vagrant, etc, but that approach has some drawbacks.

First, your users now need to learn a new programming language, just to
configure your application. Some apps (like the [suckless][2] bundle) go as far
as requiring you to patch and compile your app to change it’s configuration.

And second, your configuration is no longer hierarchical. Your application
cannot extract configuration from different sources by executing different
files, because you cannot know in advance what is being executed. A programming
language has control structures, can make calls to the internet, etc, so you
can't known in advance the output you will get. Your configuration is no longer
deterministic.

If you need to let users alter the behavior of your program, that is not
strictly configuration, there is a better solution: a plugin system.

The best way to think of configuration is as a set of key/value dicts that need
to be merged into a single config dict. No need to get fancy with yet another
DSL.


## What configuration format/sources should I use?

The short answer is: it depends, but probably more than one.

For example command line args are great to explore an app from the shell, and
tinker around it's possibilities. Many apps allow for both `-s` short and long
`--more-verbose` arguments, for those who don't want to be guessing later.

When you already know what you want it would be great to set some defaults in a
configuration file somewhere. Yes, you can always set an alias, like many
distros do:

```sh
$ type ll
ll is aliased to `ls -alF`
```

Alternatively, config files are naturally better documenting and declarative.
Some file formats allow for comments and are great as starter templates to build
upon. With files it's easier to make diffs and track changes over time.

Environment variables are the simplest way to configure apps/scripts. You just
need to populate a global dictionary before executing it. There is no need to
parse files or command line arguments. This practice is very common in cloud
providers to inject credentials or connection strings for your app. Another
example is [qutebrowser][4]; it allows the user to write *userscripts* and
passes many environment variables to share the browser state before executing
them.

On the other hand, environment variables shouldn’t hold sensitive data, there
are potential security issues regarding accidental leaks via logging and error
reporting services or child process inheritance.

Well designed applications allow different ways to be configured. Each having
it's pros and cons.

If your app is a long running process, like a webserver, you can issue a
``SIGHUP`` signal so that it reloads it's config from files. Env vars and
command line arguments cannot be easily changed from the outside after the
program startup.

What matters here is that env vars, command line args and files (`.ini`, `.yml`
and `.toml`) are the most standard formats to configure apps. You should be able
to configure any app with standard unix tools and a text editor. Stick to these
formats when possible.


## Settings discoverability

But what happens if a setting is passed as command line argument but also exist
in a config file? Which source is more important?

A proper settings-discoverability chain goes as follows:

 1. First command line args are checked.
 2. Then environment variables.
 3. Third, config files in different directories, that also imply some hierarchy. For example: config files in `/etc/myapp/settings.ini` are applied system-wide, while `~/.config/myapp/settings.ini` take precedence and are user-specific.
 4. Finally you fallback to hardcoded constants as defaults.

Some of these sources may not be present or relevant to your app. But each one
of these sources of configuration needs to be properly collected and overwritten
with an explicit level of hierarchy. This gives more flexibility to your users,
so they can run your app/script in the cloud or in their multi-user computers,
using systemd or docker, etc.

## Using the right tool for the job

Your application will require other tools, like compilers, installers, package
managers, process supervisors, etc. These tools solve different problems of the
architecture of your software.

Configuration is also part of that architecture. Along with your program you
will have to ship the configuration artifact. But this is not an issue that only
comes up when you make a new release. When you are developing you are also
making tiny releases on your laptop.

So this raises the need for some tool to provide your code with the right
configuration, in all its stages. Some of these tools are only used when
developing or in production, ideally both envs match.

There are many tools for managing configuration. For example, [direnv][6] and
[envdir][7] load environment variables from directories and files. [Systemd
units][5] have a section to list them or point to an environment file populating
the environment. [Ansible][8] includes a templating language to generate
configuration files and place them anywhere in the system. [Ansible Vault][9]
can be used to provide the app with encrypted secrets.

Some tools like [consul-template][11] or [envconsul][10] can also listen to
changes in the configuration and issue a `SIGTERM` or (even better) a `SIGHUP`
signal to your long running process, so that it can pick up new config values
without downtime.

No matter which tool you choose to manage, generate and populate the
configuration artifact, the code of your app should only care about reading
files, env vars and/or cli args.


## Naming conventions and namespaces for settings

There happen to be some formatting conventions for configuration parameters
based on where they are set. For example, it is common to declare environment
variables in uppercase:

```sh
$ DEBUG=yes OTHER_CONFIG=10 myapp
```

Since the environment is a global and shared dictionary, it is a good practice
to also apply some prefix to each setting to avoid collisions with other known
settings, like `LOCALE`, `TZ`, etc. This prefix works as a namespace for your
app.

```sh
$ MY_APP_DEBUG=yes MY_APP_OTHER_CONFIG=10 myapp
```

but if you were to set this config in an .ini file, each setting should probably
be in lower case, the namespace is implicit in the file path, i.e:
`/etc/myapp/config.ini`.

```ini
[settings]
debug=yes
other_config=10
```

Command line arguments have yet another conventions:

```sh
$ myapp --debug=yes --another-config=10
```

You probably noticed that the debug setting is a boolean value. These flags
should accept different inputs like `yes|no`, `1|0`, `true|false` or `t|f`.

It is important to be consistent in naming these variables, but to respect the
conventions too.


## A solution for the working dev

If your app is written in Python, it's your lucky day.

[Classyconf][3] is a library that helps you with a configuration architecture
for perfectionists with deadlines™, or for the working dev if it sits you
better.

The good practices that it suggests have an agnostic approach to configure
applications, no matter if they are web, CLI or GUI apps, hosted on the cloud or
running in your desktop.

You can find out more documentation at [Read the
Docs](https://classyconf.readthedocs.io/en/latest/index.html) website, but here
is a preview of how to use it.

```python
from classyconf import Configuration, Value, Environment, IniFile, as_boolean, EnvPrefix


class AppConfig(Configuration):

    class Meta:
        loaders = [
            Environment(keyfmt=EnvPrefix("MY_APP_")),
            IniFile("config.ini", section="myapp")
        ]

    DEBUG = Value(default=False, cast=as_boolean, help="Toggle debugging mode.")
    DATABASE = Value(default="postgres://localhost:5432/mydb", help="Database connection.")
```

As you can see is very declarative. It uses the concept of loaders, which
collect settings from different sources and merges them in the right order.

This class can be extended according to different environments or needs.

```python
class TestConfig(AppConfig):
    class Meta:
        loaders = [IniFile("test_settings.ini"), IniFile("config.ini")]
```

overridden at runtime

```python
>>> dev_config = AppConfig(loaders=[IniFile("dev_settings.ini")])
>>> dev_config.DEBUG
True
```

accessed (and lazily evaluated) as dict or object

```python
>>> config.DEBUG
False
>>> config["DEBUG"]
False
```

introspected and iterated

```python
 >>> for setting in config:
...     print(setting)
...
('DEBUG', Value(key="DEBUG", help="Toggle debugging on/off."))
('DATABASE', Value(key="DATABASE", help="Database connection."))
```

## Conclusion

The idea of this blog post was to highlight the importance of thinking
configuration as an API, to follow best practices and conventions and the need
to be flexible for different sources of configuration.

I've shamelessly introduced [classyconf][3] as a way to address all this topics,
but I'm sure that similar libraries can be found for other languages as well.


[1]: {filename}/configuration-friendly-apps.md "Configuration-friendly apps"
[2]: http://suckless.org/ "Software that sucks less"
[3]: https://github.com/hernantz/classyconf "Classyconf: configuration management for perfectionists with deadlines"
[4]: http://qutebrowser.org/doc/userscripts.html
[5]: https://serverfault.com/a/438945
[6]: https://direnv.net/
[7]: http://cr.yp.to/daemontools/envdir.html
[8]: https://docs.ansible.com/ansible/latest/
[9]: https://docs.ansible.com/ansible/latest/user_guide/vault.html
[10]: https://github.com/hashicorp/envconsul
[11]: https://github.com/hashicorp/consul-template
