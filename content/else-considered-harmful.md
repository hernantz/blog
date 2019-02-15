Title: Else considered harmful
Date: 2013-10-24
Category: Programming 
Tags: python, ideas, best-practices
Status: draft
Summary: Some practices and ideas for flow-control in Python.
 

![Tree branches](/images/tree-branches.jpg "Tree branches")

In Python we strongly emphasize that code must be elegant and easy to
interpret, but with PEP8 alone is not enough, many times our logic can be
nested in a cataract of if(s) and else(s) difficult to maintain. In this
talk we explored some strategies to avoid that unnecessary complexity.

I'm writing this article to encourage some code structure techniques and never
again have to discuss this in the future.

As a programmer, most of your time you will be writing ifs.
Not only becouse this is the main flow control structure, in c like languages,
but because writing an else is (or shoud be at least) a code smell. It's a trap.

The if/else couple reduces expresability of your program.

https://news.ycombinator.com/item?id=16678209

## If you write ifs

Cut the flow ifs

    ::python
    for item in items:
        if item is None:
            continue

    for item in items:
        if item is None:
            log('None found')
            break

rather than

    ::python
    for item in items:
        if item is not None:
            blah
            blah 
            blah
            blah 
            if is_nested_if:
                blah
                blah 
                try:
                    blah
                except:
                    blah 
    else:
        log('None found')
        

If your programming language has curly braces, nesting ifs leads you to
the pyramid of doom.
Pyramid of doom picture here.
While in Python it looks more like a stairs of doom.
stair of doom in python picture
In functional languages, it pretty much always looks ugly.

## Single check ifs 
    ::python
    if (this and not that) or there and (here or nearby):
        blah

if your are asking too many contions and of different kind, you are doing it 
wrong


NOMBRAR LAS CONDICIONES EN VARIABLES
USAR NOMBRES POSITIVOS no (not is_admin)


def min(x, y):
    if x < y:
        return x
    else:
        return y

should be written as

def min(x, y):
    if x < y:
        return x
    return y


USAR LAZYNESS

>>> from toolz import map  # toolz' map is lazy by default
>>> loud_book = map(str.upper, book)

HABLAR DE por que no usar el inline if/else 

>>> a = 'hola' if False else True if False else None
>>> a
>>> a = 'hola' if False else True if False else 'chau'
>>> a
'chau'

http://www.idiotinside.com/2015/10/18/5-methods-to-use-else-block-in-python/

Al no anidar if/else estamos leyendo una tabla de la verdad y compuertas logicas


PARA GUARDAR VALORES BOOLEANOS USAR
x = this or that
x = is not None 
x = something 

instead of 

if this or that:
   x = true

if something:
    x = True
else:
    x = False

POST SOBRE COUNTING THINGS IN PYTHON
escribir sobre cadena de responsabilidad?
escribir sobre actions: {} y despues actions[var]() como reemplazo al switch

Usar all([condicion==condicion2, condicion3==condicion4, etc])

VER GENERATORS WILL FREE YOUR MIND
para usar generadores y asi evirtar for loops y while loops?

https://speakerdeck.com/nb/else-considered-harmful


http://code.activestate.com/recipes/577786-smarter-default-arguments/
Currently if you want to avoid any confusion with mutable defaults, you set the default argument to some (immutable) sentinel that indicates the real default argument should be used:

def f(x=None):
    if x is None:
        x = []
There are downsides though:

The default argument no longer reflects the expectation for the argument type.
You can no longer introspect the default argument.
If you want to have the default actually be None, you will have to use some other value for the sentinel. At that point you'll probably then have two different sentinels in use: None and and its surrogate.
The real default must be re-evaluated during each call it is used.
There are two more [seemingly superfluous] lines cluttering up your function body.


La monada de usear [] o [User]
La idea de monadas es tener dos flujos separados para tratar cosas distintas
y si usamos excepciones como una forma de crear un canal alternativo para lo que
pasa en nuestro programa? Las excepciones no son necesariamente algo malo, en python
se pueden usar para crear un canal nuevo de comunicacion.
http://www.holger-peters.de/exceptions-the-dark-side-of-the-force.html
ifs for error handling ^

https://coreos.com/blog/eliminating-journald-delays-part-1.html  -> journald NO usa ifs anidados

A Python Æsthetic
https://www.youtube.com/watch?v=x-kB2o8sd5c
http://rhodesmill.org/brandon/slides/2012-11-pyconca/

https://twitter.com/raymondh/status/856663816981041152
http://stackoverflow.com/questions/865741/else-considered-harmful-in-python
http://degoes.net/articles/destroy-all-ifs

Agrupar variables al pricipio de las funciones porque siempre agrupamos cosas que son lo mismo 
variables en un lado, clases en otro archivo, etc. Mezclar todo no es la forma ideal de organizarse.

http://jrsinclair.com/articles/2017/javascript-without-loops/
http://pozorvlak.livejournal.com/94558.html
https://blog.feabhas.com/2017/02/abusing-c-switch-statement-beauty-eye-beholder/
https://youtu.be/D_6ybDcU5gc?t=8m43s
https://www.youtube.com/watch?v=rrBJVMyD-Gs
https://fsharpforfunandprofit.com/rop/

Django PermissionDenied para custom authentication backend



    def extract_timestamp(self):
        record = self.get_parsed_record()
        timestamp = record.get('timestamp')
        if timestamp is None:
            return None
        if isinstance(timestamp, datetime):
            return timestamp
        return dateutil.parser.parse(record['timestamp'])



    def get_parsed_record(self):
        record = self.record
        event_name = self.event_name
        if event_name in (SasEvents.KNOWLEDGE_COMPONENT_MODEL,
                          SasEvents.KCM_UPDATE):
            parsed_record = record
        elif event_name == CeEvents.QUESTION_PART_ATTEMPT:
            require_kcm = 'knowledge_component_model' in record
            parsed_record = qpa.parse_question_part_attempt(
                record, require_kcm=require_kcm)
        elif event_name == SasEvents.TUNING_STATUS_CHANGED:
            parsed_record = record
        else:
            parsed_record = record

        return parsed_record