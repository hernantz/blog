Title: Functions all the way down
Date: 2020-06-20
Category: Programming
Tags: fp, ideas, javascript
Summary: The building blocks of a programming language.
Status: draft


![tutles all the way down](/images/turtles-all-the-way-down.jpg "Turtles all the way down")

https://www.youtube.com/watch?v=pUN3algpvMs

## Computations

The basic building block of a functional language is obviously a function. Functions represent computations that take inputs and return outputs as results.

```js
let add = (x, y) => x + y
```

Since functions are first class citizens, functions can be values too, so functions can return functions.

```js
let add = (x) => (y) => x + y
```

Here add is a function that takes an argument `x`, returns a function that takes and argument `y` and adds them together.
This is called curring. It helps you write functions that are more composable.

```js
add2 = add(2)
```

Now `add2` can be passed arround as a parameter to other functions.

```js
add2(4) // will output 6
```

Like we said, functions represent computations, but the results might not be always needed. So a way to defer computations until they are needed is to return expressions wrapped in functions.
```js
let lazyadd => (x) => (y) => () => x + y
```

This way we can represent the eventual result as:
```js
let sum = lazyadd(1)(2)
sum() // outputs 3
```


## Making decisions

At some point we will need control structures to make decisions.
Something like the if/then blocks in other languages. We don't have anything but functions here. So functions we use:

```js
let truthy = (x) => (y) => x
let falsy = (x) => (y) => y
```

Along with these boolean representations we would need some form of primitive that returns them.

```js
let eq = (x) => (y) => x == y ? truthy : falsy;
```

Now that we can compare, we can make decisions.

```js
let ifthen = (bool) => (then) => (otherwise) => bool(then)(otherwise)
```

Or build more complex boolean logic.

```js
let negate = (bool) => ifthen(eq(bool)(truthy))(falsy)(truthy)
```

## Data containers

As we can see, functions can hold data as parameters and as return values. But how do we represent a container of x number of values?

We could create a function that take n arguments.

```js
let container = (fst) => (snd) => (n) => { /* do something */ }
```


but we would need to create multiple functions, so there is a better abstraction we can get inspired by: a linked list. A linked list is basically a tuple of a value an a pointer to another tuple. So we need a function that accepts only two arguments.

```js
let list = (fst) => (snd) => { /* do something */  };
```

Now I can create a list of any size, it is lists all the way down!

```js
numbers = list(1)(list(2)(3))
```

How to we get data back? After all this list should just be a container, and perform no calculations. We will return a getter function! 

```js
let list = (fst) => (snd) => (getter) => getter(fst)(snd)
```

This function `list` takes only two arguments. And returns a generic getter, to extract any of these values back.

Since we are working with just two values and we already know how to  make binary decisions, let's write alias those getters.

```js
let head = (xs) => xs(truthy)
let tail = (xs) => xs(falsy)
```

This way we can access all the items inside the list.

```js
head(numbers) // 1
head(tail(numbers) // 2
tail(tail(numbers) // 3
```

## Iterating over lists

```js
isempty = (xs) => eq(tail(xs), null)

range = (low) => (max) => ifthen(eq(low, max))(null)(pair(low, range(low+1, max)))
```
idx, length, map, reduce, filter
```js
map = (fn) => (xs) => { ifthen(isempty(head(xs)), null, pair(fn(head(xs)), map(fn)(tail(xs)) }
```


What about loops, just use recursion
map = (fn) => (xs) => pair(fn(head(x)))(map(fn)(tail(xs))))

reduce is just map with a different collector

reduce = (collector) => (fn) => (xs) => ifthen(isempty(head(xs)), null, collector(fn(head(xs)), map(fn)(tail(xs))

map = reduce(pair)

Null = []
Maybe x = [x]

Exceptions? => lists

Dicts are lists of tuples and an index (of getters and setters)
users = [['foo', 'bar'], ['baz', 'zaz']]

firstname user = user[0] 
lastname user = user[1]

So really firstname and lastname are aliases for get, we could just write
get i obj = obj[i]

fistname = get 0
lastname = get 1

## Object oriented programming
Objects hold data as state and methods to manipulate it. 
Methods are functions bound to objects:
circle.draw() == draw(circle)
Python went further in it's zen of explicit vs implicit
and passes an explicit reference of the object (self)

By composing functions and piping data through we don't need inheritance.

## Infinite sequences
Now that we have curring, loops and data, we realize that lists can be consumed and are no longer useful, what if we need streams?
Streams = callbag

Futures and async ?

## Types
Types are needed to manage memory and to express entities of your program. Types are like bags of data that is labeled. This labels imply some meaning of data it carries and what operations are permitted.
We could implement type checking by using validations all over our code, to make sure that we are working with the right kind of data type.

To not loose our sanity we will say that it's up to the compiler to not only manage memory for us, but to also perform type checking analysis.  

## High level programming

It seems that the building blocks of a programming language are pure functions to work over values and lists (which are functions too). Functions represent computations, an lists carry data and results around our codebase.

You can see how we can start implementing lots improvements to reduce validation (types system and compile time checking). Add syntactic sugar to write less parentheses. Auto curring of functions. Auto lazyness of results. And many more that languages have already implemented.

The more expresive a program is, the less work you have to do. You tell the compiler what you need instead of how to do it.

This process has been taking place since programmers switched from binary to assembler. Assembler is a high level programming.