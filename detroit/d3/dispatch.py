# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class dispatch:
    def __init__(self, content="dispatch"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def on(self, typenames=None, callback=None):
        """
        Source · Adds, removes or gets the callback for the specified typenames. If a callback
        function is specified, it is registered for the specified (fully-qualified) typenames.
        If a callback was already registered for the given typenames, the existing callback is
        removed before the new callback is added.
        The specified typenames is a string, such as start or end.foo. The type may be
        optionally followed by a period (.) and a name; the optional name allows multiple
        callbacks to be registered to receive events of the same type, such as start.foo and
        start.bar. To specify multiple typenames, separate typenames with spaces, such as start
        end or start.foo start.bar.
        To remove all callbacks for a given name foo, say dispatch.on(".foo", null).
        If callback is not specified, returns the current callback for the specified typenames,
        if any. If multiple typenames are specified, the first matching callback is returned.

        See more informations `here <https://d3js.org/d3-dispatch#dispatch_on>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (typenames, callback))))
        return dispatch(content=f"{self.content}.on({arguments})")


    def copy(self):
        """
        Source · Returns a copy of this dispatch object. Changes to this dispatch do not affect
        the returned copy and vice versa.

        See more informations `here <https://d3js.org/d3-dispatch#dispatch_copy>`_.
        """
        return dispatch(content=f"{self.content}.copy()")


    def call(self, type=None, that=None, *arguments):
        """
        Source · Like function.call, invokes each registered callback for the specified type,
        passing the callback the specified ...argument, with that as the this context. See
        dispatch.apply for more information.

        See more informations `here <https://d3js.org/d3-dispatch#dispatch_call>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (type, that, *arguments))))
        return dispatch(content=f"{self.content}.call({arguments})")


    def apply(self, type=None, that=None, arguments=None):
        """
        Source · Like function.apply, invokes each registered callback for the specified type,
        passing the callback the specified arguments, with that as the this context. For
        example, if you wanted to dispatch your custom callbacks after handling a native click
        event, while preserving the current this context and arguments, you could say:
        .. code:: javascript

            selection.on("click", function() {
              dispatch.apply("custom", this, arguments);
            });

        You can pass whatever arguments you want to callbacks; most commonly, you might create
        an object that represents an event, or pass the current datum (d) and index (i). See
        function.call and function.apply for further information.

        See more informations `here <https://d3js.org/d3-dispatch#dispatch_apply>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (type, that, arguments))))
        return dispatch(content=f"{self.content}.apply({arguments})")
