Title: Functions all the way down
Date: 2020-06-20
Category: Programming
Tags: fp, ideas, javascript
Summary: A thought experiment on using functions everywhere
Status: draft

![tutles all the way down](/images/turtles-all-the-way-down.jpg "Turtles all the way down")


## Computations

The basic building block of a functional language is obviously a function. Functions represent computations that take inputs and return outputs as results.

```js
let add = (x, y) => x + y
```

Since functions are first class citizens, functions can be values too, so functions can return functions.

```js
let add = (x) => (y) => x + y
```

Here `add` is a function that takes an argument `x`, returns a function that takes and argument `y` and adds them together.
This is called curring. It helps you write functions that are more composable.

```js
let incr = add(1)
```

Now `incr` is a new function that has been loaded with one param and can be passed around as a parameter to other functions or called later with the remaining param.

```js
incr(4) // will output 5
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


## Branches

At some point we will need control structures to make decisions.
Something like the if/then blocks in other languages. We don't have anything but functions here. So functions we use:

```js
let truthy = (x) => (y) => x
let falsy = (x) => (y) => y
```

Along with these boolean representations we would need some form of primitive that returns them. We could assume in this case that `==` is baked into the language.

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

We still have one problem, `x` and `y` are values already evaluated, we should only execute them if and only if they need to. For this we re-define our booleans as:

```js
let truthy = (x) => (y) => x()
let falsy = (x) => (y) => y()
```
Booleans now represent branches in computation by functions that are executed lazily.

## Containers

As we can see, functions can hold data as parameters and as return values. But how do we represent a container of x number of values?

We could create a function that take n arguments.

```js
let container = (fst) => (snd) => (n) => { /* do something */ }
```

But we would need to create multiple functions for each size of containers we have to work with. It would be great to have just one function that represented all data containers, no matter their size.

That abstraction we are looking for is the linked list.

A linked list is basically a tuple of a value an a pointer to another tuple. So we need a function that accepts only two arguments.

```js
let list = (fst) => (snd) => { /* do something */  };
```

Now I can create a list of any size, it is lists all the way down!

```js
let numbers = list(1)(list(2)(3))
```

It would be very convenient to be able to tell when the list finishes, so lets establish the convention that the last element of any list is always the null value.

```js
let numbers = list(1)(list(2)(list(3)(null)))
```

This way we can create lists that hold just one element.

```js
let one = list(1)(null)
```

How to we get data back? After all this list should just be a container, and perform no calculations. We will return a getter function!

```js
let list = (fst) => (snd) => (getter) => getter(fst)(snd)
```

This function `list` takes only two arguments. And returns a generic getter, to extract any of these values back.

Since we are working with just two values and we already know how to  make binary decisions, let's write aliases for those getters.

```js
let head = (xs) => xs(truthy)
let tail = (xs) => xs(falsy)
```

This way we can access all the items inside the list.

```js
head(numbers) // 1
head(tail(numbers)) // 2
tail(tail(numbers)) // 3
```

Now, this won't work unless we re-define our contract with lists.

```js
let numbers = list(()=>1)(()=>list(()=>2)(()=>null))
```

Lists now contain functions that return values, only when inspected.


## Generators

Not only our lists are immutable, but also lazy. This has a nice side effect. We have accidentally created lazy generators.

This means we can represent infinite lists, like all the natural numbers that are computed only when accessed/evaluated:

```js
let numbers = (n) => list(()=>n)(()=>numbers(n+1))
```

If we start generalizing again, the signature of every generator would look like this: 

```js
let gen = (fn) => (v) => list(()=>v)(()=>gen(fn)(fn(v)))
```

And now we can rewrite our natural numbers generator reusing the `incr` function.

```js
let numbers = gen(incr)(0)
```

## Loops

Instead of *for loops*, we use recursion to iterate and manipulate values one by one.

The layout of map looks like this:

```js
let map = (fn) => (xs) => list(()=>fn(head(xs)))(()=>map(fn)(tail(xs)))
```

It takes a `fn` to apply to each element of `xs`, so we build a new `list` with the using `head` and recursively mapping the `tail`.

We face our first problem with recursion. We need a base case:

```js
let map = (fn) => (xs) => list(()=>fn(head(xs)))
                              (ifthen(islast(xs))
                                     (()=>()=>null)
                                     (()=>()=>map(fn)(tail(xs))))
```

The base case is a helper function that tells us when to stop the recursion, in this case, when we reached the end of the list.

```js
let islast = (xs) => eq(tail(xs))(null)
islast(one) // truthy
```

A more general implementation is to accept other function as the accumulator.

```js
let fold = (acc) => (fn) => (xs) => acc(()=>fn(head(xs)))
                                       (ifthen(islast(xs))
                                              (()=>()=>null)
                                              (()=>()=>fold(acc)(fn)(tail(xs))))
```

With this abstraction we can not only compose `map`, but some functions like `sum` and `length`.

```js
let id = (x) => x
let add = (x) => (y) => x() + y()
let ones = (x) => ifthen(eq(x)(null))(()=>0)(()=>1)

let map = fold(list)
let sum = fold(add)(id)
let length = fold(add)(ones)
```

## Streams


If we start generalizing again, a way to iterate 

```js
let cons = (xs) => list(()=>head(xs))(()=>cons(tail(xs))
```

```js
let cons = (next) => gen
```

```js
let range = i => n => gen numbers (i)
```

Map is a list creator so we can join maps.


```js
let ends = (next) => (xs) => ifthen(islast(xs))
                                   (()=>()=>null)
                                   (()=>()=>next(xs))
```


```js
let check = (condition) = (next) => (xs) => ifthen(condition(xs))
                                                  (()=>()=>null)
                                                  (()=>()=>next(tail(xs)))
```

```js
let ends = check (islast)
```


```js
let gen = (check) => (acc) => (fn) => (v) => acc(()=>v)
                                                (check(gen(check)(acc)(fn))(fn(v)))
```

```js
let fold = gen(ends)(list)
```

## More

There are many other functions that we should explore, like filter, reverse, index, etc.

But I think by now we can appreciate that [functions are really powerful][1] bulding blocks.

Of course this syntax is very ilegible and cumbersome, and writing `map(fn, [1, 2, 3])` is way more expresive.

This was just a [thought experiment][2], an academic one. So don't try this at home.


[1]: https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf
[2]: https://www.youtube.com/watch?v=pUN3algpvMs
