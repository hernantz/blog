Title: If (you write ifs)
Date: 2013-10-24 22:56
Category: Programming 
Tags: python, ideas
Status: draft
Summary: As a programmer, most of your time you will be writing ifs.
 

![Tree branches](/images/tree-branches.jpg "Tree branches")

As a programmer, most of your time you will be writing ifs.
Not only becouse this is the main flow control structure, in c like languages,
but becouse writing an else is (or shoud be at least) a code smell. It's a trap. 

## Cut the flow ifs

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

////////////
   
Titulo charla: Tenemos que dejar de escribir else por dos anos

En Python hacemos fuerte incapie en que el codigo sea elegante y facil de interpretar,
pero con PEP8 solo no alcanza, muchas veces nuestra logica puede quedar anidada en 
una catarata de if(s) y else(s) dificil de mantener.
En esta charla exploraremos algunas estrategias para evitar esa complejidad inecesaria.

Se llama Hernan Lozano, pero se pone hernantz de nickname,
le gusta la musica en general y el metal en particular, pero no tiene una banda,
es hincha de Talleres, pero nunca va a la cancha,
es avido lector, pero casi siempre termina leyendo el mismo autor,
y por sobre todo, le gusta aprender cosas nuevas, pero despues nunca hace nada con lo que aprendio.


###################
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
###################


La monada de usear [] o [User]
La idea de monadas es tener dos flujos separados para tratar cosas distintas
y si usamos excepciones como una forma de crear un canal alternativo para lo que
pasa en nuestro programa? Las excepciones no son necesariamente algo malo, en python
se pueden usar para crear un canal nuevo de comunicacion.
http://www.holger-peters.de/exceptions-the-dark-side-of-the-force.html

https://coreos.com/blog/eliminating-journald-delays-part-1.html  -> journald NO usa ifs anidados

A Python Æsthetic
https://www.youtube.com/watch?v=x-kB2o8sd5c
http://rhodesmill.org/brandon/slides/2012-11-pyconca/


http://www.nationalaffairs.com/publications/detail/cultural-intelligence
