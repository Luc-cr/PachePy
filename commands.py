class commands():
  
    def __init__(self):
        self.events = {}

    def addCommand(self, name, help, arg):
        def inner(*args, **kwargs):
            self.events[name] = (args[0]," - {} {}:{}\n".format(name, arg, help))
        return inner

