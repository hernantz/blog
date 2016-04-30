Title: Django's signal to noise ratio
Date: 2016-04-29
Category: Programming
Tags: django, python
Summary: Keeping a balance between decoupled and maintenable code.

![Contact (1997) scene](/images/signal-to-noise-ratio.png "Contact (1997)")

## Noise

Signals allow decoupled applications get notified when actions occur elsewhere
in the project. This decoupling can become unmaintainable if not enough care
is taken.

Most of the time signals are used for doing some action when a model is
saved/deleted.

For the sake of [introducing the topic][2], let's consider that our Q&A
application needs to store each user's resume (with experience, studies, etc).
Whenever a new user is created, we'll ensure that it gets it's own `Resume`
instance.

```python
# somewhere inside cv/models.py

from django.dispatch import receiver
from django.core.signals import post_save
from users.models import User

@receiver(post_save, sender=User)
def create_user_cv(sender, **kwargs):
    if kwargs.get('created', False):
        Resume.objects.get_or_create(user=kwargs.get('instance'))
```

If another piece of code is also interest in perfoming some action everytime a
user is saved, like syncing user info with a 3rd party jobs board site for
example, we could acomplish that with another handler:

```python
# somewhere inside users/models.py

from django.dispatch import receiver
from django.core.signals import post_save
from django.forms import model_to_dict
from users.models import User

@receiver(post_save, sender=User)
def sync_jobsboard_with_users(sender, **kwargs):
    user = kwargs.get('instance')
    resume_data = model_to_dict(user.resume)
    sync_with_jobsboard(user_data, resume_data)
```

Now this code expects a curriculum to be associated to this user and that won't
be true for new members.

Whilst this special case could be catched by proper testing, as code grows
**you'll have a hard time traking moving pieces**, scattered throughout
different handlers. Specially because **the order in which they get executed is
not inmediatelly clear**.


## Silence

The following snippet shows how to put everything in one place, gaining us some
maintainability, but still allowing us differentiate recently created instances,
`pre_save` and `post_save` code:

```python
class User(models.Model):
    # ...

    def save(self, *args, **kwargs):
        # pre save code
        
        created = not self.pk
        
        if created:
            # this model does not exist in our db yet
 
        # persist the model to the db and also ensures
        # that pre/post save signals get emitted
        super(MyModel, self).save(*args, **kwargs)

        # post save code, now we have self.pk

        resume, _ = Resume.objects.get_or_create(user=self)

        user_data = model_to_dict(self)
        resume_data = model_to_dict(resume)
        sync_with_jobsboard(user_data, resume_data)
```

Model's `save()` method is also a pretty standard method to be overrided since
it is called by other frameworks like DRF or the admin so it makes a good place
to hook in there our custom code.


## Signal

Truth be told, signals have broader applications that cannot be replaced by
extending a single method.

For example, when you have to track changes in `ManyToManyField` fields

```python
class Question(models.Model):
    favorited = ManyToManyField(User)
```
Here we cannot use the `save()` because m2m instances are added or deleted
through intermediate tables which are managed by Django. But we can make use of
the `m2m_changed` signals for that: 

```python
def handle_fav_notifications(sender, instance, action, **kwargs):
    """Send an email to the author of a question whenever it gets fav'ed"""
    if action == 'post_add':
        instance.notify_new_favorite()

m2m_changed.connect(
    handle_fav_notifications, sender=Question.favorited.through)
```

In case we needed to track multiple m2m relations, we can do all that in a
single handler:

```python
class FavableMixin(models.Model):
    favorited = M2MField(User, related_name='favorite_%(class)s')

    class Meta:
        abstract = True

    def notify_new_favorite(self):
        pass


class Question(FavableMixin):
    pass


class Answer(FavableMixin):
    pass


class Comment(FavableMixin):
    pass


@receiver(m2m_changed, dispatch_uid='m2m_fav_notifications')
def handle_fav_notifications(sender, instance, action, **kwargs):
    if issubclass(instance._meta.model, FavableMixin) and action == 'post_add':
        instance.notify_new_favorite()
```

Signals can also become handy when trying to **react to code you do not own**.
This other example shows how we can hook some custom code into the `auth` third
party app, without having to create a new login view:

```python
from django.contrib.auth.signals import user_login_failed


def help_user_with_login_link(sender, credentials, **kwargs):
    """Let's help our forgetful users login, and email them a login link."""
   if update_and_get_failure_logins(credentials) > MAX_LOGIN_ATTEMPTS:
        send_login_link(credentials.email)

# Sent when the user failed to login successfully
user_login_failed.connect(help_user_with_login_link)
```

Django puts emphasis on **following conventions**, and signals shouldn't be the
exception. You have to place signals and handlers somewhere the framework can
pick them up automatically, and that is usually the `models.py` or `urls.py` of
each app. Something tidier would be to place them in a `signals.py` file or
module and import it explicitly in the app's config file, as suggested by
[the docs][1].

There is nothing wrong with signals *per se*, so long as there's a good balance
between decoupled and maintenable code. As a general rule I would suggest to
**avoid using signals for code you own**. Instead put everything inside a method
or view, and *try to avoid them* for code you don't own, **except when it sounds
like a good idea**.


[1]: https://docs.djangoproject.com/en/1.9/topics/signals/ "Django documentation"
[2]: https://twitter.com/hernantz/status/623293934857535488
