import inspect

class commands():

    def __init__(self):
        self.events = {}

    def addCommand(self):
        def inner(func, *args, **kwargs):
            self.events[func.__name__] = (func," - {} {}:{}\n".format(func.__name__, str(inspect.getfullargspec(func).args).replace("[]", "")," " + func.__doc__))
        return inner

