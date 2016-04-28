Title: Django's signal to noise ratio
Date: 2016-04-22
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

For the sake of [introducing the topic][2], let's consider that our e-commerce
application needs to store each user's billing information (like billing
address, phone, etc). Whenever a new user is created, we'll ensure that it gets
it's own `BillingDetails` instance. 

```python
# somewhere inside billing/models.py

from django.dispatch import receiver
from django.core.signals import post_save
from users.models import User

@receiver(post_save, sender=User)
def create_user_billing_details(sender, **kwargs):
    if kwargs.get('created', False):
        BillingDetails.objects.get_or_create(user=kwargs.get('instance'))
```

If another piece of code is also interest in perfoming some action everytime a
user is saved, like syncing user info with a 3rd party CRM service for example,
we could acomplish that with another handler:

```python
# somewhere inside users/models.py

from django.dispatch import receiver
from django.core.signals import post_save
from django.forms import model_to_dict
from users.models import User

@receiver(post_save, sender=User)
def sync_crm_with_users(sender, **kwargs):
    user = kwargs.get('instance')
    user_data = model_to_dict(user)
    billing_data = model_to_dict(user.billing_details)
    sync_with_crm(user_data, billing_data)
```

Now this code expects an instance of preferences to exist and that won't be true
for new members.

Whilst this special case could be catched by proper testing, as code grows
**you'll have a hard time traking moving pieces**, scattered throughout
different handlers. Specially because **the order in which they get executed is
not inmediatelly clear**.


## Silence

The following snippet shows how to put everything in one place, gaining us some
maintenability, but still enabling us differentiate recently created instance,
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

        billing, _ = BillingDetails.objects.get_or_create(user=self)

        user_data = model_to_dict(self)
        billing_data = model_to_dict(billing)
        sync_with_crm(user_data, billing_data)
```

Model's `save()` method is pretty standard method to overrided since it is
called by other frameworks like DRF or the admin so it makes a good place to
hook in there our custom code.


## Signal

Truth be told, signals have broather applications that cannot be replaced by
extending a single method.

For example, when you have to track changes in `M2MField` fields

```python
@receiver(m2m_changed, dispatch_uid='calendar_entry_generator_m2m_sync')
def handle_m2m_sync_for_calendar_entries(sender, instance, **kwargs):
    """
    We need to track m2m relations too, since they might not be available
    when the generator was saved.
    IMPORTANT: If the model tracked by CalendarEntryGeneratorMixin, has a
    m2m field that uses a through model needed for sync'ing calendar entries
    update that manually.
    """
    if issubclass(instance._meta.model, CalendarEntryGeneratorMixin):
        instance.sync_calendar_entries()
```

Signals can also become handy when trying to **react to code you do not own**.
This other example shows how we can hook some custom code into the `auth` third
party app, without having to create a new login view, just to extend it:

```python
from django.contrib.auth.signals import user_logged_in


def check_suspicious_login(sender, user, request, **kwargs):
   if is_unusual_login(user, request):
        user.notify_by_email('suspicious_login', request)

user_logged_in.connect(check_suspicious_login)
```

Django puts emphasis on **following conventions**, and signals shouldn't be the
exception. You have to place signals and handlers some place the framework can 
pick them up automatically. That is usually either `models.py` or `urls.py` of
each app. Something tidier would be to place them in a `signals.py` file or
module and import it explicitly in the app's config file, as suggested by
[the docs][1].

There is nothing wrong with signals *per se*, so long as there's a good balance
between decoupled and maintenable code. As a general rule I would suggest to
**avoid using signals for code you own**, i.e. put everything inside a method or
view, and *try to avoid them* for code you don't own, **except when it sounds
like a good idea**.


[1]: https://docs.djangoproject.com/en/1.9/topics/signals/ "Django documentation"
[2]: https://twitter.com/hernantz/status/623293934857535488
[3]: http://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project
[4]: https://docs.djangoproject.com/en/1.9/ref/contrib/auth/#django.contrib.auth.signals.user_login_failed "user_login_failed signal"
