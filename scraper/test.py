import functools
class reprwrapper(object):
    def __init__(self, repr, func):
        self._repr = repr
        self._func = func
        functools.update_wrapper(self, func)
    def __call__(self, *args, **kw):
        return self._func(*args, **kw)
    def __repr__(self):
        return self._repr(self._func)

def wrapper(func):
    return reprwrapper(lambda x: f"d3.{x.__name__}", func)

class A:

    @wrapper
    @staticmethod
    def mymethod():
        return 2

print(A.mymethod)
