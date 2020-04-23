Title: Default is not set
Date: 2020-04-23
Category: Programming
Tags: python
Summary: How can you tell if an optional parameter was set or not?


Usually for optional params we use `None` as default in the function signature.
If it is `None` we assume the user did not specify one.

```python
def main(param=None, **kwargs):
    if param is None:
        param = get_system_default()
    # ...


main(param='foo')  # use 'foo'
main()             # dynamically set param
```

But what if `None` is a possible value too?

```python
main(param=None)   # OOPS, will calculate anther value for param
```

The parameter still needs to be optional, because we can calculate a good
default if it is not set, but how can we know if an optional parameter was
explicitely set by the caller?

One way would be make it a required parameter and expose the
`get_system_default()` function. We then change the signature of our `main()`
so that Python ensures param is always set.

```python
def main(param, **kwargs):
    # ...


main(param='foo')                      # use 'foo'
main(param=get_system_default())       # dynamically set param
```

With this approach we delegated that responsabilty to the user of our function,
this is style and is perfectly feasable. But if `main()` is called a lot, we
complicated things for our user.

Another trick is to use the `**kwargs` dict and check if a param is there or
not.

```python
def main(*args, **kwargs):
    if 'param' in kwargs:
        param = kwargs['param']
    else:
        param = get_system_default()
    # ...
```

This also works fine, but we kind of loose visibility on what parameters
`main()` accepts. This is a bummer if you are using autocomplete tools of other
helpers that analyse the code.

So my last trick kind of mitigates that by introducing a custom default value,
the `NotSet` type.

```python
class NotSet():
    pass


NOT_SET = NotSet()


def main(param=NOT_SET, **kwargs):
    if param is NOT_SET:
        param = get_system_default()
    # ...
```

This is a unique type that won't collide with any other possible value for
`param`. If it is `NOT_SET`, then it is not set :)

I kind of like the first solution, but if you think that you will end up with
lots of `get_system_default()` calls everywhere in your code, at some point
switching to this `NOT_SET` approach would make sense.
