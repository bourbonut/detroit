# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class timer:
    def __init__(self, content="timer"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def restart(self, callback=None, delay=None, time=None):
        """
        Source · Restart a timer with the specified callback and optional delay and time. This
        is equivalent to stopping this timer and creating a new timer with the specified
        arguments, although this timer retains the original invocation priority.

        See more informations `here <https://d3js.org/d3-timer#timer_restart>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (callback, delay, time))))
        return timer(content=f"{self.content}.restart({arguments})")


    def stop(self):
        """
        Source · Stops this timer, preventing subsequent callbacks. This method has no effect
        if the timer has already stopped.

        See more informations `here <https://d3js.org/d3-timer#timer_stop>`_.
        """
        return timer(content=f"{self.content}.stop()")
