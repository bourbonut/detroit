# Generated by detroit
# See https://github.com/bourbonut/detroit/tree/main/api_maker

from functools import partial
from operator import is_not

class event:
    def __init__(self, content="event"):
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

    def __call__(self, *args):
        arguments = ", ".join(map(repr, args))
        return f"{self}({arguments})"

    def on(self, typenames=None, listener=None):
        """
        Source · Equivalent to drag.on, but only applies to the current drag gesture. Before
        the drag gesture starts, a copy of the current drag event listeners is made. This copy
        is bound to the current drag gesture and modified by event.on. This is useful for
        temporary listeners that only receive events for the current drag gesture. For example,
        this start event listener registers temporary drag and end event listeners as closures:
        .. code:: javascript

            function started(event) {
              const circle = d3.select(this).classed("dragging", true);
              const dragged = (event, d) => circle.raise().attr("cx", d.x = event.x).attr("cy", d.y = event.y);
              const ended = () => circle.classed("dragging", false);
              event.on("drag", dragged).on("end", ended);
            }


        See more informations `here <https://d3js.org/d3-drag#event_on>`_.
        """
        arguments = ", ".join(map(repr, filter(partial(is_not, None), (typenames, listener))))
        return event(content=f"{self.content}.on({arguments})")

