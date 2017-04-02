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

Dates mean nothing without the proper context, and that context is provided by
what it is called a [timezone][2].

A timezone is attached to a geographical location, under a certain
jurisdiction. So it doesn't mean just the offset, because that offset can
change, that is why timezones have names. Unless we are speaking of the UTC
timezone, which is a very special one.

We should think UTC time as the entire world's current time you compare all
other dates with. It is meant to be objective in the sense that it never was
and won't ever be affected by local time changes.

https://lazystone.github.io/programming/time/2017/03/13/time-matters.html
LEER eppur si muove



Como hacer queries de datos de hoy, ayer, etc. Depende del timezone del usuario, no usar utc_now + 1 day o utc_now - 1 day,
ver django model utils (timeframed mixin)

Cuidado con cachear "proximos estrenos", eso depende del offset del cliente

No usar logs en localtime, con DST hay problemas

Hablar del ultimo PEP sobre diferenciar fechas locales DST "first"

pytz y la tabla orson 

Ver postgres y tz

De como se cambio un timezone (chile), y por que combiene tener una referencia al timezone que origino la fecha


## Mesuring duration
para eventos = calcular hora reloj y mostrar ese periodo en la tz del usuario.
para progreso = calcular tiempo transcurrido.


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

[^1]: Many countries have started and stopped using DST. Others have adjusted their offset for "" reasons. 
      PONER EJEMPLOS DE EPPUR SI MUOVE
[^2]: If you see a date formatted like `yyyy-mm-ddThh:mm:ss-03:00`, it means that it's offset is UTC-3
      but it also means that to convert it to UTC you have to make that `-03:00` part a `+00:00`, so in
      this case you have to add three hours to the date for it to be in UTC.

[1]: https://en.wikipedia.org/wiki/Daylight_saving_time "Daylight Saving Time"
[2]: https://en.wikipedia.org/wiki/Tz_database "Olson Database"
