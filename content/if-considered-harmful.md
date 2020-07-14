Title: If considered harmful
Date: 2013-10-24
Category: Programming 
Tags: python, ideas
Status: draft
Summary: Some practices and ideas for flow-control in Python.
 

![Tree branches](/images/tree-branches.jpg "Tree branches")

In Python we strongly emphasize that code must be elegant and easy to
interpret, but with PEP8 alone is not enough, many times our logic can be
nested in a cataract of `if`/`else` combinations, which is difficult to
maintain and reduces expresability of your program.

In this post we *incrementally* explore strategies that structure our code to
avoid that unnecessary complexity in readability in an attempt to write
branchless code.


## If you write else

As a programmer, most of your time you will be writing `if`s.  Not only becouse
this is the main flow control structure, in C like languages, but because
writing an `else` is (or shoud be) a code smell. It's a trap.

When reading code, we programmers keep a heap of variables and flow control in
our heads.

The problem with using `else` is that it implies a jump (or goto) to another
context, that is the contrary of what was previously stated.

Let's check some code that we all might have written at some point:

```python
def func():
    if foo or bar:
        ###
        ###

        if bar in baz:
            ###
            ###

        else:
            ###
            ###

            if foo not in qux:
                ###
                ###
                ###
    else:
        ###
        ###

###
###
```

This might be perfectly valid PEP8 Python code, but it has it's problems.  When
reading from top to bottom, the programmer has to keep track of each execution
path that could reach a certain piece of code, in the example above, this would
be:

```python
def func():
    if foo or bar:
        ### <------ foo or bar
        ###

        if bar in baz: 
            ### <------ for or bar & bar in baz
            ###

        else:
            ### <------ foo or bar & bar not in baz
            ###

            if foo not in qux:
                ### <------ foo or bar & bar not in baz
                ###              & foo not in qux
                ###
    else:
        ### <------ not foo & not bar
        ###

###
###
```

Probably by the time you reach an else statement, the context switch will cause
this code to be hard to reason about. Also you might check if every `if` is
connected to some `else`, which condition is it conected to, if that condition
is altered, is the `else` still valid?

A better approach to handle these cases while avoiding the context switch is to
do context increments.

```python
def func():
    if foo or bar:
        ### <------ TRUE
        ###

        if bar in baz: 
            ### <------ TRUE & TRUE
            ###

            if foo == quix: 
                ### <------ TRUE & TRUE & TRUE
                ###

    ###
    ###
```

See how on every branch we are only adding more information, not negating some
other statement.

We are, nonetheless still stacking the new context, so we need to keep in our 
heads everything that is going on from the begining. This is what I call the
stairway of doom (a.k.a pyramid of doom in languages with curly brances).

Nesting context is better that switcing and jumping around but a An alternative
to this is having the full context on every branch, to fully understand what's
happening.

```python
def func():
    if foo or bar:
        ### <------ TRUE
        ###

    if (foo or bar) and bar in baz:
        ### <------ TRUE & TRUE
        ###

    if (foo or bar) and bar in baz and foo == quix:
        ### <------ TRUE & TRUE & TRUE
        ###

    ###
    ###
```

You can stablish a parallelism between the full context and truth tables in
which you have all the variables and their combinations on a single place at
[simple glance][6].


## If you write if

In programming readability counts. When reading code we are mentally parsing a
program, every line of code has to be decoded in our heads.

```python
if user.is_active and user.has_permission('foo') and user.credit >= SOME_PRICE:
    ######
    ###
    ########
```

In the snippet above, we are checking if the user should access a certain
feature and if it has enough credit to do so. Then, why not simply write the
statement in clearer words? Naming the conditionals lowers our cognitive
overhead.

```python
can_access_foo = user.is_active and user.has_permission('foo')
has_credit = user.credit >= SOME_PRICE

if can_access_foo and has_credit:
    ######
    ###
    ########
```

Now say that we need to handle the cases where the user cannot access and
return an error:

```python
can_access_foo = user.is_active and user.has_permission('foo')
has_credit = user.credit >= SOME_PRICE

if can_access_foo and has_credit:
    ######
    ###               <--------- what matters
    ########

if not can_access_foo:
    return # or raise error

if not has_credit:
    return # or raise error

############
###                  <--------- what matters
#######
```

It is easy to get distracted by validations and checks, from what is important.
Instead we should cut the flow of the program with guards and [return early][0], so
we don't have to worry about certain checks later in the code.

```python
can_access_foo = user.is_active and user.has_permission('foo')
has_credit = user.credit >= SOME_PRICE

if not can_access_foo:
    return # or raise error

if not has_credit:
    return # or raise error

######
########            <--------- what matters
############
###
#######
```

If this code was inside a function, we could move these checks outside of it to
some decorators.

```python
@requires_access('foo')
@requires_credit(SOME_PRICE)
def foo(user):
    ######
    ########        <--------- what matters
    ############
    ###
    #######
```

This patern greatly improves the maintenability and expresability of the
program. Not only we have less (seemingly superfluous) lines cluttering up your
function body, but these decorators are reusable/composable functions.


## If you write elif

Most of the time we are writing `if`s for type-checking and error-handling.
There are some ways of not writting `if`s altogether. 

In the case of `elif`s, it's easy to observe the paterns that emerge from the
code, and patterns are easy to refactor. Consider this checks on the type of
user to determine the right permissions:

```python
def get_permissions(self):
    #####
    ########

    if user == 'admin':
        perms = self.get_admin_permissions()
    elif var == 'editor':
        perms = self.get_editor_permissions()
    elif var == 'authenticated'
        perms = self.get_authenticated_permissions()
```

Although I'm not a big fan of OOP, I should point out that polymorphism can
also replace conditionals.

```python
class Admin(User):
    def get_permissions(self):
        return ['read', 'write', 'delete']


class Editor(User):
    def get_permissions(self):
        return ['read', 'write']
```

So you would simply write `user.get_permissions()` and let the type
of the class determine the right method to be executed.

But I suppose that at some point we will need to have the `if` logic
to determine which instance of User to create.

So a more pythonic way of doing this form of pattern matching is to use
dictionary lookups:

```python
def get_admin_permissions():
    #####
    ########

def get_editor_permissions():
    #####
    ########
    
def get_permissions(user):
    perms = {
        'admin': get_admin_permissions,
        'editor': get_editor_permissions
    }

    return perms[user]()
```

This way if we need to extend the code with more permissions
functions, we get this branching logic for free.

Another example is turning flags on/off, with code like this:

```python
var = False

if foo:
    var = True
elif bar:
    var = True
elif baz:
    var = True
```

Can be simply put like:

```python
var = foo or bar or baz
```

I guess the point here is to use the right pattern that replaces the
switch/elif structure with more readable/maintainable code.


## If you write flags

Flags or sentinels are checks we do to avoid executing pieces of code that are
optional or blocks that are computationally expensive.

```python
def f(filter=False):
    ###
    #####

    if filter:
        ###
        #####  <---- optinal piece of code that gets activated
```

Would be better off if we let the user of our function execute any pluggable code
to filter:

```python
def noop(*args, **kws):
    return None

def f(filter=noop):
    ###
    #####

    filter(some, args)  # <-- look ma, no ifs!
```

We know that function arguments hide `if`s behind the interpreter to initialize
variables, by allowing you to set some defaults that can be overriwritten at
runtime. But currently if you want to avoid any confusion with mutable
defaults, you set the default argument to some (immutable) sentinel that
indicates the real default argument should be used.

```python
def f(x=None):
    if x is None:
        x = [1, 2, 3]

    ###
    #####
```

Should be ideally written with some immutable data structure:

```python
def f(x=(1, 2, 3)):
    ###
    #####
```

Many times we are working with collections of data that need to be filtered,
re-grouped, sliced, etc. These checks are also flags!

The `itertools` module offers some functions that allow us to hide our `if`s
(along with our [loops][5]) by simply passing *predicates* to these functions:

```python
>>> import itertools
>>>
>>> less_than_one = lambda x: x < 1
>>> numbers = [1, 2, 3, 0]
>>>
>>> list(filter(less_than_one, numbers))
[0]
>>> list(itertools.filterfalse(less_than_one, numbers))
[1, 2, 3]
>>>
>>> for key, group in itertools.groupby(numbers, less_than_one):
...     print(f'{key}: {list(group)}')
... 
False: [1, 2, 3]
True: [0]
```


Computationally intensive jobs => lazyness => ej del orm django

allows you to express pieces of computation, without having to pay the costs
until you really need them.
```python
>>> from toolz import map  # toolz' map is lazy by default
>>> loud_book = map(str.upper, book)
```

## if you handle errors
Errors => exceptions => monads

VER GENERATORS WILL FREE YOUR MIND
para usar generadores y asi evirtar for loops y while loops?




La monada de usear [] o [User]
La idea de monadas es tener dos flujos separados para tratar cosas distintas
y si usamos excepciones como una forma de crear un canal alternativo para lo que
pasa en nuestro programa? Las excepciones no son necesariamente algo malo, en python
se pueden usar para crear un canal nuevo de comunicacion.
http://www.holger-peters.de/exceptions-the-dark-side-of-the-force.html
ifs for error handling ^

"You either will end up with if something is not None: on almost every line and global pollution of your logic by type-checking conditionals, or will suffer from TypeError every day. Not a pleasant choice."

A Python Æsthetic
https://www.youtube.com/watch?v=x-kB2o8sd5c

https://twitter.com/raymondh/status/856663816981041152
http://stackoverflow.com/questions/865741/else-considered-harmful-in-python
http://degoes.net/articles/destroy-all-ifs
https://returns.readthedocs.io/en/latest/index.html

Agrupar variables al pricipio de las funciones porque siempre agrupamos cosas que son lo mismo 
variables en un lado, clases en otro archivo, etc. Mezclar todo no es la forma ideal de organizarse.

https://blog.feabhas.com/2017/02/abusing-c-switch-statement-beauty-eye-beholder/
https://youtu.be/D_6ybDcU5gc?t=8m43s
https://www.youtube.com/watch?v=rrBJVMyD-Gs
https://fsharpforfunandprofit.com/rop/

3 formas de manejar errores:
1- excepciones (is a form of pattern matching by type of error), instead of if/elif/else, you just except multiple times.
2- result value (int or boolean), multiple return values (like go), a structured object that represents a result: un objecto en js -> monada (maybe) -> response message like a json api => the problem is that the signature of every function will now become a maybe x?
3- callbacks -> Promises
http://stupidpythonideas.blogspot.com/2015/05/if-you-dont-like-exceptions-you-dont.html
https://bytes.yingw787.com/posts/2019/12/06/monads/

Django PermissionDenied para custom authentication backend

Compiler-driven development: the need for runtime-checking is reduced when using the compiler to do this for us with Typechecking automatically https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html#standard-duck-types

flag argument: https://www.martinfowler.com/bliki/FlagArgument.html

Talk about cyclomatic complexity
https://www.youtube.com/watch?v=dqdsNoApJ80
https://sobolevn.me/2019/02/python-exceptions-considered-an-antipattern


if's are flow control structures used for:
- validation (parse, don't validate post?)
- error handling https://mijailovic.net/2017/05/09/error-handling-patterns-in-go/


## Endif

There are many *considered harmful* essays out there. One of those is even
called: *["Considered Harmful" Essays Considered Harmful][3]*.

[Else considered harmful][4] is a talk that inspired this post.  It explains
why writing `else` can be problematic and how to get rid of it, and I thought,
can we go further and make the same attempt with `if`?

The result is supposed to be a guideline on how to express programs with less
logic branches. That being said, I'm not against writing `if`, `else` or `elif`
per se, life is more complex with lots of gray areas. The examples here are
[not real world snippets][1], but simply put to make a point.

Interestingly enough, all the expermients lead to functional programmig
principles, like composing functions, passing functions as parameters,
processing iterables, lazyness and immutability, etc.

Maybe this implies that functional languages are superior in terms of
expresability.


[0]: https://blog.timoxley.com/post/47041269194/avoid-else-return-early "Avoid else, return early"
[1]: https://gist.github.com/hernantz/ca79890b9b212c6df45e615d94320f6e
[2]: https://stackoverflow.com/a/1554691/518918
[3]: https://meyerweb.com/eric/comment/chech.html "“Considered Harmful” Essays Considered Harmful"
[4]: https://speakerdeck.com/nb/else-considered-harmful
[5]: https://jrsinclair.com/articles/2017/javascript-without-loops/ "JavaScript Without Loops"
[6]: https://en.wikipedia.org/wiki/Truth_table "Truth table"
