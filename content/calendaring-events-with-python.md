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
the browser or postgres contain their own copies [^4].  For example, `pytz` is
a [library][5] that *"brings the Olson tz database into Python"* providing
timezone classes to use with `datetime` objects.

Any how, it is a good idea to store the user's timezone, so that you are able
to format dates in case you don't trust the clients ability to display them
correctly (due to an outdated db most likely).

It might also be important to store the original timezone of a date somewhere, so
that if that timezone gets it's offset updated, you can notify the user about a
possible change that date that requires his attention. Pretty much like when a
flight's schedule gets updated, and the airline emails you.

Como hacer queries de datos de hoy, ayer, etc. Depende del timezone del usuario, no usar utc_now + 1 day o utc_now - 1 day,
ver django model utils (timeframed mixin)


De como se cambio un timezone (chile), y por que combiene tener una referencia al timezone que origino la fecha


https://lazystone.github.io/programming/time/2017/03/13/time-matters.html

Despite [PEP495][6]'s attempt at providing some extra help to desambiguate
naive dates, it is [highly recomended][7] that you **convert dates to UTC as
soon as they enter the system** and work with them that way for calculations
and queries, so that all dates are naive but implicitly UTC.

When retriving today's movie releases, it is important to request those dates
in the UTC version of the user's 00:00 to 23:59 time lapse, since *today* is
relative to the timezone you are currently at, and using *UTC's today* is not
an option. Be extra carefull if you are caching these results, and make sure
that the timezone is part of the cache's
key.

When calculating the duration of an event, it is important to do it converting
both dates (start and end) to UTC, so that the time jumps inbetween get
ignored.

When logging events, you can see logs that have the same date, that would seem
to be duplicated because of DST.


## Recurring events
Script para calcular fechas de una serie y evitar problemas con DST 
https://coderwall.com/p/7t3qdq/datetimes-and-timezones-and-dst-oh-my

## Alarm events
When it comes to events that should happen of a given day and time, regardless
of the timezone, the approach has to be a bit different.

usar la libreria de prox notificacion en local time del usuario


VIDEO pycon india avoiding common pitfalls of datetime

https://julien.danjou.info/blog/2015/python-and-timezones

http://tommikaikkonen.github.io/timezones/?utm_source=Python+Weekly+Newsletter&utm_campaign=90b2ae57fb-Python_Weekly_Issue_221_December_10_2015&utm_medium=email&utm_term=0_9e26887fc5-90b2ae57fb-299842937

http://delorean.readthedocs.org/en/latest/quickstart.html#with-power-comes

http://www.creativedeletion.com/2015/12/03/timezone-updates-need-fixing.html and it's related links

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

[1]: https://en.wikipedia.org/wiki/Daylight_saving_time "Daylight Saving Time"
[2]: https://en.wikipedia.org/wiki/Tz_database "Olson Database"
[3]: https://mm.icann.org/mailman/listinfo/tz-announce "tz announce maling list"
[4]: https://www.iana.org/time-zones/repository/tz-link.html "Sources for time zone and daylight saving time data"
[5]: http://pytz.sourceforge.net/ "pytz - World Timezone Definitions for Python"
[6]: https://www.python.org/dev/peps/pep-0495/ "PEP 495 -- Local Time Disambiguation"
[7]: http://lucumr.pocoo.org/2011/7/15/eppur-si-muove/ "“Eppur si muove!”* – Dealing with Timezones in Python"
[8]: http://infiniteundo.com/post/25509354022/more-falsehoods-programmers-believe-about-time "More falsehoods programmers believe about time"
[9]: http://www.creativedeletion.com/2015/12/03/timezone-updates-need-fixing.html "Timezone updates need to be fixed"
