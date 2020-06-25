Title: Configuration is an API, not an SDK
Date: 2020-06-24
Category: Programming
Tags: python, best-practices
Summary: A config management architecture for the working dev.
Status: draft

![Soviet control room](/images/soviet-control-room.jpg "Soviet nuclear plan control room")

Configuration is every setting that needs to change based on the environment where the app is executed. It helps you *preset* the state of your app, without having to change the code. This is why it is important to provide a clear separation of configuration and code.


## Why are executable config files a bad idea?

[Configuration is just another API][1] of your app.

It might be used by people with or without technical skills, that install or run your app.

Executable files can be used as config sources like `.vimrc`, `Vagrantfile`, etc. This approach has some drawbacks.

First, your users now need to learn a new programming language, just to configure your application. Some apps (like the [suckless][2] bundle) go as far as requiring you to patch and compile your app to change it’s configuration.

And second, your configuration is no longer hierarchical, your application cannot extract configuration from different sources by executing different files, because you cannot know in advance what is being executed. So you typically end up with one single executable file as config that takes care of everything.

The best way to think of configuration is as a set of key/value dicts that need to be merged into a single config dict. No need to get fancy.

If you need to let users alter the behaviour of your program, that is not strictly configuration, but there is a better solution for this: a plugin system.

## Settings discoverability

Well designed applications allow different ways to be configured. Each having it's pros and cons.

For example command line args are great to explore an app from the shell, and tinker around it's possibilities.

When you already know what you want it would be great to set some defaults in a configuration file somewhere. Yes, you can always set an alias, like many distros do:

```sh
$ type ll
ll is aliased to `ls -alF`
```

And yes, many apps allow for both `-s` short and `--long-descriptive` arguments.

Config files are naturally better documenting and declarative. It's easier to make a diff and inspect.

On the other hand, environment variables are the simplest way to configure apps/scripts. You just need to populate a global dictionary before executing it. There is no need to parse files or command line arguments. An example of this is [qutebrowser][4] were it allows the user to write userscripts, but it's up to the user to look into the environment dict for what it needs. This practice is also common in cloud providers to inject credentials or connection strings for your app.

But what happens if a setting is passed as command line argument but also exist in the config file? Which one is more important?

A proper settings-discoverability chain goes as follows:

 1. First command line args are checked.
 2. Then environment variables.
 3. Config files in different directories, that also imply some hierarchy. For example: config files in `/etc/myapp/settings.ini` are applied system-wide, while `~/.config/myapp/settings.ini` take precedence and are user-specific.
 4. Hardcoded constants as defaults.

Some of these sources may not be present or relevant to your app. Ideally each one of this sources of configuration need to be properly collected and overwritten with an explicit level of hierarchy. This gives more flexibility to your users, so they can run your app/script in the cloud or in their multiuser computers, using systemd or docker, etc.

## Using the right tool for the job

There are many tools for managing configuration. [Direnv][6] and [envdir][7] load environment variables from directories and files. [Systemd units][5] have a section to list them or point to an environment file populating the environment. [Ansible][8] includes a templating language to generate configuration files and placing them anywhere in the system.
[Ansible Vault][9] can be used to provide the app with encrypted secrets.

No matter which tool you choose to manage, generate and populate the configuration, your app should only care about reading files/env vars/cli args.


## Naming conventions and namespaces for settings

There happen to be some formatting conventions for configuration parameters based on where they are set. For example, it is common to declare environment variables in uppercase:

```sh
$ DEBUG=yes OTHER_CONFIG=10 myapp
```

Since the environment is a global and shared dictionary, it is a good practice to also apply some prefix to each setting to avoid collisions with other known settings, like `LOCALE`, `TZ`, etc. This prefix works as a namespace for your app.

```sh
$ MY_APP_DEBUG=yes MY_APP_OTHER_CONFIG=10 myapp
```

but if you were to set this config in an .ini file, each setting should probably be in lower case, the namespace is implicit in the file path, i.e: `/etc/myapp/config.ini`.

```ini
[settings]
debug=yes
other_config=10
```

Command line arguments have yet another conventions:

```sh
$ myapp --debug=yes --another-config=10
```

## A solution for the working dev

If your app is written in Python, it's your lucky day.

[Classyconf][3] is a library that provides the configuration management solution for perfectionists with deadlines, or for the working dev if it sits you better.

The good practices that it suggests have an agnostic approach to configure applications, no matter if they are web, CLI or GUI apps, hosted on the cloud or running in your desktop.

You can find out more documentation at [Read the
Docs](https://classyconf.readthedocs.io/en/latest/index.html) website, but
here is a preview of how to use it.

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

As you can see is very declarative. It uses the concept of loaders, which collect settings from different sources and merges them in the right order.

Later this object can be used to print settings

```python
>>> config = AppConfig()
>>> print(config)
DEBUG=True - Toggle debugging mode.
DATABASE='postgres://localhost:5432/mydb' - Database connection.
```

extended according to different environments or needs

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

The idea of this blog post was to highlight the importance of a nice configuration API for any program, no matter what kind of program it is. 

I've shamelessly introduced classyconf, but I'm sure that similar libraries can be found for other languages as well.


[1]: {filename}/configuration-friendly-apps.md "Configuration-friendly apps"
[2]: http://suckless.org/ "Software that sucks less"
[3]: https://github.com/hernantz/classyconf "Classyconf: configuration management for perfectionists with deadlines"
[4]: http://qutebrowser.org/doc/userscripts.html
[5]: https://serverfault.com/a/438945
[6]: https://direnv.net/
[7]: http://cr.yp.to/daemontools/envdir.html
[8]: https://docs.ansible.com/ansible/latest/
[9]: https://docs.ansible.com/ansible/latest/user_guide/vault.html