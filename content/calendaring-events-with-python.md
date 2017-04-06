Title: Calendaring events with python 
Date: 04-07-2017
Category: Programming
Tags: python
Status: draft
Summary: Some gotchas to keep in mind when scheduling your next doomsday


![Aztec sun stone](/images/aztec-calendar.png "Aztec sun stone")


## One time events

Because of the way we track time, a single moment can happen at different times
of the day for different people around the globe and a single date and time can
never happen or happen twice thanks to [DST][1] or government regulations [^1].
Yes, working with dates is [hard][8]. 

**Dates mean nothing without the proper context**, and that context is provided
by what it is called a [timezone][2].

**A timezone it doesn't mean just the offset**, because that offset can change,
that is they have names, and are attached to a geographical location, under a
certain jurisdiction. Unless we are speaking of the UTC timezone, which is a
very special one.

We should think UTC time as the entire world's current time you compare all
other dates with. It is meant to be objective in the sense that it never was
and won't ever be affected by local time changes.

Timezone information is available in the [Olson database][2]. Since timezones
change every now and then, it is vital to keep your software up to date [^3].
If that is something you cannot control, be advised that the dates your system
is dealing with might not be correct (i.e. in an embedded device).

Updates can be handled differently depending on the OS, program or language you
use. For example, in linux there is a package `tzdata`, but some programs like
the browser or postgres contain their own copies [^4].

Python provides naive dates by default through it's `datetime` module, and it
is someone else's responsability to provide tz information, for example, `pytz`
is a [library][5] that *"brings the Olson tz database into Python"* providing
timezone classes to use with `datetime` objects.

```python
>>> datetime.datetime.now()
datetime.datetime(2017, 4, 4, 10, 36, 57, 800151)
>>> datetime.datetime.utcnow()
datetime.datetime(2017, 4, 4, 13, 37, 1, 833276)
>>> pytz.utc.localize(datetime.datetime.utcnow())
datetime.datetime(2017, 4, 4, 13, 37, 44, 500463, tzinfo=<UTC>)
```

Despite [PEP495][6]'s attempt at providing some extra help to desambiguate
naive dates, it is highly recomended that you **convert dates to UTC as soon as
they enter the system** and work with them that way for calculations and
queries. Despite the fact that you can take naive dates as being [UTC
implicitly][7], I would suggest to still [attach the UTC tz][10] to them [^6].
This way, all the information is there, and it becomes easier to reason about date
calculations:

When logging events, you can see logs that have the same date, that would seem
to be duplicated because of DST. Instead if you have them in UTC and in the
[ISO format][12], there is no place left for confusion.

```python
'2002-10-27T01:30:00'  # no timezone attached
'2002-10-27T01:30:00'

'2002-10-27T01:30:00-04:00'  # with timezone attached
'2002-10-27T01:30:00-05:00'

'2002-10-27T05:30:00+00:00'  # in UTC 
'2002-10-27T06:30:00+00:00'
```

Even more, a sever could fire repeated crons or skip them if not configured to
[use UTC][15] due to a DST switch.

When retriving today's entries from a database, it is important to request
those dates in the UTC version of the user's 00:00 to 23:59 time lapse, since
*today* is relative to the timezone you are currently at, and using *UTC's
today* is not an option. *Note*: Be extra carefull if you are caching these
results, and make sure that the timezone is part of the cache's key.

```python
# Assuming event dates are stored in UTC (like postgres does).
# These convertions might not be needed depending on the storage engine
# or frameworks you are using.

def active(self):
    now = datetime.utcnow().replace(tzinfo=utc)
    return events.filter(start<=now, end>=now)

def future(self):
    now = datetime.utcnow().replace(tzinfo=utc)
    return events.filter(start>=now)

def today_only(self):
    # UTC's current date might be different from user's date
    # datetime.datetime.combine returns naive dates :(
    local_now = user_tz.normalize(datetime.utcnow().replace(tzinfo=utc))
    local_today_min = user_tz.localize(datetime.combine(local_now, time.min))
    local_today_max = user_tz.localize(datetime.combine(local_now, time.max))
    today_min = utc.normalize(local_today_min)
    today_max = utc.normalize(local_today_max)
    return events.filter(start>=today_min, end<=today_max)
```

When doing calculations, despite the fact that you can manipulate aware dates
transparently [^7] the math is evident for the programmer if those dates are in
UTC:

```python
>>> buenos_aires
datetime.datetime(2017, 4, 5, 2, 0,
    tzinfo=<DstTzInfo 'America/Buenos_Aires' -03-1 day, 21:00:00 STD>)
>>> madrid
datetime.datetime(2017, 4, 5, 6, 0, 
    tzinfo=<DstTzInfo 'Europe/Madrid' CEST+2:00:00 DST>)
>>> buenos_aires - madrid
datetime.timedelta(0, 3600)  # mmm... hard to tell...
>>> pytz.utc.normalize(buenos_aires)
datetime.datetime(2017, 4, 5, 5, 0, tzinfo=<UTC>)
>>> pytz.utc.normalize(madrid)  # there is obviously a one hour diff
datetime.datetime(2017, 4, 5, 4, 0, tzinfo=<UTC>)
>>> pytz.utc.normalize(buenos_aires) - pytz.utc.normalize(madrid)
datetime.timedelta(0, 3600)  # yeah! same results
```

Event durations can be conterintuitive ir you don't keep in mind the inbetween
jumps of DST. And when building this dates, the user needs to desambiguate them 
explicitly, provide the `is_dst` flag that is.
```python
>>> eastern = pytz.timezone('US/Eastern')
>>> loc_dt = datetime.datetime(2002, 10, 27, 1, 30, 00)  # date occured twice
>>> edt_dt = eastern.localize(loc_dt, is_dst=False)  # notice the is_dst flag
>>> edt_dt.isoformat()
'2002-10-27T01:30:00-05:00'
>>> est_dt = eastern.localize(loc_dt, is_dst=True)
>>> est_dt.isoformat()
'2002-10-27T01:30:00-04:00'
>>> edt_dt - est_dt
datetime.timedelta(0, 3600)
```
If your are rendering these kind of events in some sort of calendar, you'll
have to decide if dates or duration is what determines how to represent this
event in a slot.

Now that we know that UTC aware dates everywhere [is the way to go][16],
there are some extra details to pay attention to:

1. It is a good idea to store the user's timezone, so that you are able
   to format dates in case you don't trust the clients ability to display them
   correctly (due to an outdated db on their side, most likely).
2. If events are attached to a certain location, like a flight for instance, and
   that location changes it's timezone, then we need to recalculate all scheduled
   dates for that location and notify users about it.

So storing the original timezone as way to get back to and from UTC is
important.


## Recurring events

For generating a series of events you should use the `dateutils.rrule` package
[^8], which allows a great deal of configuration and manages corner cases like:
*every last day of the month*.

But when it comes to creating recurring events, say every Monday at 11:00 am,
the user wants those dates to always stay at 11:00 am even if there is a DST
switch at some point.

The procedure is perfectly explained [here][14] and involves naive dates on
purpose!

We first have to generate the ocurrences regardless or the timezone settings.

```python
>>> start = datetime.datetime(2014, 2, 22, 11, 0)  # Feb 22
>>> end = datetime.datetime(2014, 3, 24, 0, 0)  # March 24
>>> list(rrule(WEEKLY, dtstart=start, until=end, byweekday=(MO,)))
[datetime.datetime(2014, 2, 24, 11, 0), 
 datetime.datetime(2014, 3, 3, 11, 0), 
 datetime.datetime(2014, 3, 10, 11, 0), 
 datetime.datetime(2014, 3, 17, 11, 0)]  # all at the same time
```

Now we will attach the user's timezone to these dates and normalize them to
UTC, so that the change happens on the stored dates, but the time the user will
see in their local timezone stays intact.

```python
>>> tz = pytz.timezone('America/Chicago')  # observes DST switch on March 9
>>> localized = [tz.localize(dt) for dt in dates]
>>> for dt in localized:
        print 'Central: {}; UTC: {}'.format(dt, dt.astimezone(pytz.utc))
'Central: 2014-02-24 11:00:00-06:00; UTC: 2014-02-24 17:00:00+00:00'
'Central: 2014-03-03 11:00:00-06:00; UTC: 2014-03-03 17:00:00+00:00'
'Central: 2014-03-10 11:00:00-05:00; UTC: 2014-03-10 16:00:00+00:00'
'Central: 2014-03-17 11:00:00-05:00; UTC: 2014-03-17 16:00:00+00:00'
```
You should also set the `is_dst` flag when needed.

## Reminder events
When it comes to events that should happen of a given day and time, regardless
of the timezone, the approach has to be a bit different.

usar la libreria de prox notificacion en local time del usuario

```python
tz = user.time_zone
now = utc.now().astimezone(tz)
rule = rrule.rrule(rrule.WEEKLY, dtstart=now, byweekday=days,
                   byhour=self.reminder_time.hour,
                   byminute=self.reminder_time.minute)

# Get the fist recurrence after after "now"
next_reminder = rule.after(now)
```


# Conclusions

Always use tz aware dates and specifically UTC aware dates inside your program,
but keep a reference to a local timezone that makes sense in case you need to
retrace changes. For all this, is vital to stay up to date with tz updates.

Part of the idea of this post was make it a compendium of all things related to
dates I have read about, and had to use for work. So I suggest you to read all
linked pages, they are worth reading.

I hope you found this useful.


[^1]: Many countries have started and stopped using DST and different times.
      > For example, 1:30am on 27th Oct 2002 happened twice in the US/Eastern timezone when the
      > clocks where put back at the end of Daylight Saving Time.
      > Similarly, 2:30am on 7th April 2002 never happened at all in the US/Eastern timezone, as
      > the clocks where put forward at 2:00am skipping the entire hour.
      >
      > Extracts from *the pytz [documentation][5]*

      Moreover, timezones can change for other reasons that just DST. 
      > In 1915 Warsaw switched from Warsaw time to Central European time with no daylight savings
      > transition. So at the stroke of midnight on August 5th 1915 the clocks were wound back 24
      > minutes creating an ambiguous time period that cannot be specified without referring to the
      > timezone abbreviation or the actual UTC offset. In this case midnight happened twice, neither
      > time during a daylight saving time period. pytz handles this transition by treating the
      > ambiguous period before the switch as daylight savings time, and the ambiguous period after
      > as standard time.
      >
      > Extracts from *the pytz [documentation][5]*

[^2]: If you see a date formatted like `yyyy-mm-ddThh:mm:ss-03:00`, it means that it's offset is UTC-3
      but it also means that to convert it to UTC you have to make that `-03:00` part a `+00:00`, so in
      this case you have to add three hours to the date for it to be in UTC.
[^3]: The ICANN organization, which is in charge of hosting the Olson Database, publishes updates through
      a [mailing list][3]. Some languages like Elixir, have [automatic builds][9] for their date packages
      when the db gets updated.
[^4]: More information about programs, libraries and systems can be found [here][4].
[^5]: [PEP495][6] suggests adding an attribute called `fold` to instances of the `datetime` classes. For
      example, on a system set to US/Eastern timezone:

          >>> dt = datetime(2014, 11, 2, 1, 30)
          >>> dt.astimezone().strftime('%D %T %Z%z')
          '11/02/14 01:30:00 EDT-0400'
          >>> dt.replace(fold=1).astimezone().strftime('%D %T %Z%z')
          '11/02/14 01:30:00 EST-0500'
      This way we can represent just one moment in time in an ambiguous case.
[^6]: This is a peak at some of the terminology involved when dealing with dates:

      * naive datetime – a datetime object without a timezone.
      * localized datetime – a datetime object with a timezone.
      * localizing – associating a naive datetime object with a timezone.
      * normalizing – shifting a localized datetime object from one timezone to another, this changes
        both tzinfo and datetime object.

      As the Delorean docs [explain it][11].

      *Attaching* a timezone should never be done using `.replace()` as you
      might carelessly end up creating an invalid date.

[^7]: Python cannot mix aware and naive dates or you will get a `TypeError:
      can't compare offset-naive and offset-aware datetimes` exception.

[^8]: [dateutils][13] is a must if your app makes intensive use of dates. It
      also provides some other niceties like `relativedelta` and `parser.parse`.

[1]: https://en.wikipedia.org/wiki/Daylight_saving_time "Daylight Saving Time"
[2]: https://en.wikipedia.org/wiki/Tz_database "Olson Database"
[3]: https://mm.icann.org/mailman/listinfo/tz-announce "tz announce maling list"
[4]: https://www.iana.org/time-zones/repository/tz-link.html "Sources for time zone and daylight saving time data"
[5]: http://pytz.sourceforge.net/ "pytz - World Timezone Definitions for Python"
[6]: https://www.python.org/dev/peps/pep-0495/ "PEP 495 -- Local Time Disambiguation"
[7]: http://lucumr.pocoo.org/2011/7/15/eppur-si-muove/ "“Eppur si muove!”* – Dealing with Timezones in Python"
[8]: http://infiniteundo.com/post/25509354022/more-falsehoods-programmers-believe-about-time "More falsehoods programmers believe about time"
[9]: http://www.creativedeletion.com/2015/12/03/timezone-updates-need-fixing.html "Timezone updates need to be fixed"
[10]: https://julien.danjou.info/blog/2015/python-and-timezones "Timezones and Python"
[11]: http://delorean.readthedocs.io/en/latest/quickstart.html "Delorean docs"
[12]: https://en.wikipedia.org/wiki/ISO_8601 "ISO 8601"
[13]: https://labix.org/python-dateutil "python-dateutil"
[14]: https://coderwall.com/p/7t3qdq/datetimes-and-timezones-and-dst-oh-my
[15]: http://www.creativedeletion.com/2015/08/07/why-not-to-use-server-local-time.html "Why not to ask the server for its "local time"
[16]: http://tommikaikkonen.github.io/timezones/ "timezones"
