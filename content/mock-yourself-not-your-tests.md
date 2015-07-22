Title: Mock yourself, not your tests
Date: 2015-04-19 19:56
Category: Programming 
Tags: testing, python, mocks, rants
Summary: Every mock is a smell, avoid them as much as you can.
Status: draft


*tl;dr*: While sometimes mocks are needed, they should not be the first tool 
you use to write tests. It is a shame to be mocking your code when you could 
be writing meaningful tests at almost the same cost.

![Enable virtualization in BIOS](/images/bridge-fail.jpg)

In this post I try to discourage the use of mocks when writing tests.
I'm not completely against them (I see their value) but it's that sometimes 
I feel like we abuse of them, just to make tests pass, feel comfortable of
seeing another green dot in your test suite and to release yourself from the
burden of having to test your code.


## Why do we use mocks anyway? 

Well, I'll name a few reasons that seem legit to me.

One reason to use mocks is to **force a desired state** for your test
and easily trigger side effects. Mocks facilitate a lot the testing of
corner cases.
Another reason is **to gain speed** by staying away of slow code, like 
system calls, db, network calls, costly calculations, etc. Also it could be 
a short path to increase code coverage. But probably the primary reason for 
using mocks is to **make a unit test more specific**. Just testing exactly 
one piece of code, and thus, avoiding having to test things that (hopefully)
are already tested.


### Testing with mocks

Let's see some example code:

```python
class Payment():
    def __init__(self, invoice_id, credit_card):
        # more code here
    
    def process(self):
        amount = self.calculate_amount()
        if self.credit_card.has_credit():
            self.credit_card.withdraw(amount)
            self.status = 'processed'
```

As we can see, the `process()` method uses other objects (credit_card), called 
collaborators. If we were to write a **unit test** for this method, we would 
mock all its collaborators, so that we test the codepaths involved, and 
only caring that the function calls the collaborators, nothing more. We do this, 
because we are assuming that all the collaborators work and have their own unit 
tests.

```python
from mymodule import Payment
from mock import Mock
import unittest


class PaymentTestCase(unittest.TestCase):

    @mock.patch.object(Payment, 'calculate_amount')
    def test_process_cc_with_credit(self, calculate_amount_mock):
        cc = Mock()
        calculate_amount_mock.return_value = 'foo'
        cc.has_credit.return_value = True
        payment = Payment(1, cc)
        payment.process()
        cc.withdraw.assert_called_with('foo')

    @mock.patch.object(Payment, 'calculate_amount')
    def test_process_cc_without_credit(self, calculate_amount_mock):
        cc = Mock()
        cc.has_credit.return_value = False
        payment = Payment(1, cc)
        payment.process()
        self.assertFalse(cc.withdraw.called)
```

Now let's think for a moment if these tests we just wrote tell us, with a good
level of confidence, whether `process()` works or not. Or are we just asserting
that some methods are called in specific order with specific parameters. This 
feels almost like testing that the compiler/interpreter works!

> *"We've fallen into a trap of testing that the code does what the code says 
> it does, rather than testing functional behaviour we care about."*
>
> Every mock.patch() is a little smell. <cite>[Daniel Pope][1]</cite>

This kind of unit testing makes too many assumptions on how `process()` is
implemented. Tightly coupling your tests with mocks, make refactors to be
painfull.  As soon as you change a detail of the implementation your tests will
*break* (which is not the same as to *fail*), with helpless tracebacks about
functions that were not called, or mocks that fail to be applied because some
method doesn't exist anymore, like:

```python
Traceback (most recent call last):
  File "test.py", line 9, in <module>
    m.process_with_currency()
  File "/usr/local/lib/python2.7/site-packages/mock.py", line 65, in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
AttributeError: Mock object has no attribute 'some_old_method'
```
 
Another drawback I wanted to point out is that mocks tend to be too permissive, in 
the sense that they swallow errors that should occur because of a change in the 
API of the mocked object.

```python
class CreditCard():
    # ...

    # the old signature was: withdraw(self, amount)
    def withdraw(self, amount, currency):
        # ...
```

If suddendly I decided to change the signature of the `withdraw()` method, to
charge the credit card with a specific currency, the mocked tests above would
still pass successfully, so they will not tell you anymore whether you have
introduced a regression bug or not. 
Yes, I'm aware of the `autospec=True` param, that would restrict the mock to
just follow the object's api, making our tests a little bit less permissive.

```python
from mymodule import Payment, CreditCard
from mock import Mock, create_autospec
import unittest


# create a mock that mimics the real CreditCard object
CreditCardMock = create_autospec(CreditCard, spec_set=True)


class PaymentTestCase(unittest.TestCase):

    @mock.patch.object(Payment, 'calculate_amount', autospec=True)
    def test_process_cc_with_credit(self, calculate_amount_mock):
        cc = CreditCardMock()
        calculate_amount_mock.return_value = 'foo'
        cc.has_credit.return_value = True
        payment = Payment(1, cc)
        payment.process()
        cc.withdraw.assert_called_with('foo')

    @mock.patch.object(Payment, 'calculate_amount', autospec=True)
    def test_process_cc_without_credit(self, calculate_amount_mock):
        cc = CreditCardMock()
        cc.has_credit.return_value = False
        payment = Payment(1, cc)
        payment.process()
        self.assertFalse(cc.withdraw.called)
```

Or we could have gone a little bit further, and inject a double to our
`process()` function, for example:

```python
class StubCreditCard:
    """
    Replace our CreditCard with a double to avoid hitting the db or
    3rd party services (if any).
    """
    def __init__(self, amount=100):
        self.amount = amount

    def has_credit(self):
        return self.amount > 0

    def withdraw(self, amount):
        self.amount = self.amount - amount
```

This is also an interesting strategy, but, now you'll have to be maintaining
this double by hand, every time you real object is updated. A double is a double
edged sword.

Let's try a completely different approach and see if we can do any better.


### Testing without mocks

Now, how would I test this, without mocks?

```python
from mymodule import Payment 
from myfactories import CreditCardFactory, InvoiceFactory
import unittest


class PaymentTestCase(unittest.TestCase):

    def test_process_cc_with_credit(self):
        InvoiceFactory.create(id=1, cost=5)
        cc = CreditCardFactory(balance=10)
        payment = Payment(1, cc)
        payment.process()
        self.assertEqual(cc.balance, 5)

    def test_process_cc_without_credit(self):
        InvoiceFactory.create(id=1, cost=5)
        cc = CreditCardFactory(balance=0)
        payment = Payment(1, cc)
        payment.process()
        self.assertEqual(cc.balance, 0)
```

Comparing the test above, with the one that uses mocks, we can see that it has 
almost the same amount of code, but this test is not bound to the implementation, 
it is still deterministic, plus it tests goals in an automated way, similar to 
the manual check I would do to trust that the `process()` method works.

We have used two techniques here that helped us get way from mocks.

The first technique was to start testing how collaborators interact between
each other inside `process()`. These type of tests are called **integration
tests**, that test larger units of your code, with real components. This also 
helped reducing the chance of bugs that sneak away when you test units in 
isolation.

*Side note*: Keep a reasonable amount of code under your tests. While writing
tests for very small units of code might be adding noise to your test suite,
there won't be too much value in testing a huge portion of your code either.

The second technique consisted on using factories. Whats important is that
factories **build real objects** for you in a declarative and straighforward
way, which let's you focus on the bits of data you need to setup your test and
leave the rest for the factory to implement.

Alright! This is looking better, but does this mean that we can get rid of
mocks once for all? Nope.

## In the quest for *real mocks*

There are cases where it really makes sense to use mocks. I'll show you a couple
of examples that, in my opinion, could serve as inspiration to use them
successfully and write better tests. These mocks are: 

* Agnostic: the details of your code change, but your mocks continue to work.
* Swappable: you can easily turn them on/off or switch to them on the fly.
* Precise: they stub only the sensible parts of the real object.
* Verified: the interfaces of such mock are carefully maintained and mimic the 
  real object.


### Example 1: Did you receive my email?

Django gives us an in-memory mailbox that captures all outgoing emails. What's 
interesting is that it sets up this dummy double  **by default** when you 
inherit from `TestCase`, so writing these kind of tests becomes really easy.

```python
from mymodule import Payment
# ...
from django.core import mail
from django.test import TestCase


class PaymentTestCase(TestCase):

    def test_process_cc_with_credit(self):
        # this factory will create an Invoice and a User associated to 
        # it, with the specified email
        InvoiceFactory.create(id=1, cost=5, user__email='foo@bar.com')
        # ... more code 

        # Test that payment receipt email has been sent.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['foo@bar.com'])
```

### Example 2: This call is being recorded

Say for example that you need to hit a 3rd party API that you don't own, that
probably has throttle limitations, no sandbox/testing ground, you cannot setup
and run it locally, or all these together. Doing live testing is not really an
option. But if you use something like [vrc.py][8], then you profit from testing
against real requests/responses that are recorded, so that next time you run the
test suite it runs under safe and repeatable conditions, without hitting the net.

```python
from mymodule import Payment 
# ...
import vcr


class PaymentTestCase(unittest.TestCase):

    @vcr.use_cassette('stripe_responses/cc_with_credit.yaml')
    def test_process_cc_with_credit(self):
        # ... more code

    @vcr.use_cassette('stripe_responses/cc_without_credit.yaml')
    def test_process_cc_without_credit(self):
        # ... more code 
```

If the 3rd party API changes, you don't have to do anything but delete the
recorded responses, and your test will do all the work for you, updating the
test cases with the new responses.
Should you need more control over a certain response that is not easy to 
reproduce, (like a 500 error response), you can achieve that with [httpretty][11].

```python
import httpretty

class PaymentTestCase(unittest.TestCase):
    @httpretty.activate
    def test_process_handles_failure_from_stripe():
        httpretty.register_uri(httpretty.GET, 'https://api.stripe.com',
                               body='{"success": false}', status=500,
                               content_type='text/json')
        # ... more code
        payment.process()
        self.assertEqual(payment.status, 'failed')
```

### Example 3: The philosophy of time <s>travel</s> freezing

When you need to test code that deals with dates, mocks will be very handy
too. Let's see an example.

```python
from datetime import (datetime, timedelta)

def tomorrow():
    return datetime.now() + timedelta(days=1)
```

To test this, you would have to write tests that have almost the same code 
you are trying to test, and the bugs in your code will also pass unnoticed 
into your tests.

```python
assert tomorrow() == today() + timedelta(days=1)  # silly test
```

Now, when we test using the [freezegun][9] module

```python
from freezegun import freeze_time

with freeze_time('2012-01-01'):
    assert tomorrow().strftime('%Y-%m-%d') == '2012-01-02'
```

You can see how we avoided mocking `datetime()` and `timedelta()` and we can
even use `strftime()` in our tests. We made time behave deterministically
using a nice declarative API, that doesn't get in our way. We can even make
`tomorrow()` to be calculated using other libraries.

```python
import arrow

def tomorrow():
    return arrow.now() + timedelta(days=1)  # Our test still passes :)
```


## Need for speed

I mentioned that using mocks was a legit excuse for speeding your tests, and
staying away of slow parts like the database. Well if you used an ORM and your
data structures are pretty standard, then you may be able to [switch to an
in-memory sqlite database][4] just to run your tests.

Another possibility that's worth exploring, but I haven't tried myself though,
is to [mount the database][5] in a `tmpfs` filesystem, or combine that with a
[custom docker build][6] to gain speed, but at the same time, run the tests
against the db engine you use in production, and thus, gain also reliability.

In case you don't want to mess with custom setups for testing, there are some
easy tricks to speed your tests like running them in parallel:

```bash
$ nosetests --processes=NUM
```
provided that your tests [can run concurrently][7] and are IO bound, or simply
[throw hardware at the problem][10] with more RAM, a more powerful CPU or an
SSD.


## In conclusion 

* Integration tests are one honking great idea, let's do more of those. Don't 
  relay exclusively in unit tests, test goals.
* Use factories to reduce boilerplate of tests setup and asserting a known state
  before they run.
* Avoid using mocks as much as you can. There's a good chance you'll be testing 
  what the code does, not what it should do.
* In times of need, apply well maintained global mocks, the closest possible to 
  the danger zone.

Mock yourself not your tests :P


[1]: http://mauveweb.co.uk/posts/2014/09/every-mock-patch-is-a-little-smell.html
[2]: http://www.toptal.com/python/an-introduction-to-mocking-in-python
[3]: https://docs.python.org/3/library/unittest.mock.html#autospeccing
[4]: http://www.machinalis.com/blog/optimizing-your-tests-in-django/
[5]: https://gist.github.com/zekefast/07fa5434afcd0ba77f9b "Run postgresql in a ram disk"
[6]: https://github.com/gentics/docker-tmpfs-mysql "Docker tmpfs mysql"
[7]: http://nose.readthedocs.org/en/latest/plugins/multiprocess.html#beware
[8]: https://github.com/kevin1024/vcrpy
[9]: https://github.com/spulec/freezegun
[10]: https://twitter.com/df07/status/607562584401821696
[11]: https://github.com/gabrielfalcao/HTTPretty
