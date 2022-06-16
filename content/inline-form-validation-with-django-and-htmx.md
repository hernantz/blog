Title: Inline form validation with Django and Htmx
Date: 2022-06-13
Category: Programming
Tags: python, django, javascript, htmx
Summary: Partial and progressive form validation without any Javascript.


<video autoplay loop>
  <source src="/videos/htmx-inline-form-validation.mp4" type="video/mp4">
</video>

[Hypermedia][1] as the engine of application state puts strong emphasis on
giving control to the server to render the state of the data and what actions
can be done with it.

Although client side scripting is allowed, this should only be a sidecar for
simple state manipulations. Most UI interactions that affect the state of the
app would need a roundtrip to the server to get the new state of the data.


## Client side vs server side validation

Call me purist, but in a traditional MPA, frontend scripting should only help to
aid in non-stateful changes, like toggling a dropdown, clearing an input, hiding
an alert after X seconds, etc.

Progressive form validation is a gray area. HTML already provides some basic
attributes to control valid inputs like `required`, `maxlength`, `type`, etc:

```html
<label for="id_email">What's your e-mail address?</label>
<input type="email" id="id_email" name="email" required maxlength="140">
```

While valuable, this is no replacement for server side validation, since clients
should never be trusted. Other times we need to do some validation that really
depends on the values of other fields or lookups on a database (is this email
already used?).

What is really nice about client side validation is the short feedback cycle.
The user can see the errors as the input is being manipulated or as soon as
focus is set on the next form element. Otherwise the user would have to fill the
entire form, wait for the server to validate and then scroll to see what errors
where found.

**Server side validation is required** for security, but **client side
validation is desirable** for it has better UX. Can't we have both?


## Partial and progressive server side form validation

With the help of [htmx][2], we will submit the form for validation after the
user interacts with an input and we will partially update the field with the
result from the server.

![htmx inline form validation](/images/htmx-server-side-form-validation.png "Htmx inline form validation")

The idea is to wrap each form field with a `div` + some `hx-` directives. I'm using
`hx-select` & `hx-trigger=blur` directives to only replace current input element
with the validation for that field.

```html
  <div
      id="email_field"
      {% if form.email.errors %}class="error"{% endif %}
      hx-select="#email_field"
      hx-post="{% url 'form-demo' %}"
      hx-trigger="blur from:find input"
      hx-target="#email_field">
    {{ form.email.label_tag }}
    {{ form.email }}
    {{ form.email.errors }}
  </div>
```

![htmx inline form validation](/images/htmx-inline-form-validation.png "Htmx inline form validation")

The [django backend code][3] is still pretty agnostic. If the form is invalid,
django will re-render the page with the errors displayed. If the form is valid,
and it was submitted via htmx request, we re-render the page (without any
errors).

```python
class SignUpView(FormView):
    form_class: forms.Form = SignupForm
    template_name: str = 'form-demo.html'
    success_url = reverse_lazy('form-demo')

    def form_valid(self, form):
        if self.request.htmx:
            # The submitted form is valid, just render it `as is` for htmx.
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)
```

If the form is manually submitted through a regular http post request, we just
follow the normal `FormView` flow, and we can redirect or make some change in
the database.

With this simple solution, quick to implement and easy to maintain, we get the
best of both worlds.

 **Immediate feedback** to the user, **no client-side code logic repetition**
 for validating fields, progressive enhancement approach when JS is not
 available and it is **framework agnostic**, can be adapted with any CSS toolkit
 and any backend language.


[1]: https://intercoolerjs.org/2016/05/08/hatoeas-is-for-humans.html "HATEOAS is for Humans"
[2]: https://htmx.org/ "high power tools for HTML"
[3]: https://github.com/hernantz/django-htmx-demo/pull/1/files "Example implementation"
