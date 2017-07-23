#!/usr/bin/env python3

class Signal:
    __serial__ = 0

    def __init__(self, scheduler, value = 0, name = None):
        self.scheduler  = scheduler
        self.components = []
        self.pending    = None

        if name is None:
            Signal.__serial__ += 1
            name = "Signal%d" % Signal.__serial__
        self.name = name

        self.value      = None
        self.set(value)
        self.value = value

    def bind(self, component):
        self.components.append(component)
        return self

    def get(self):
        return self.value

    def __set__(self, value):
        #print('setting %s to %d' % (self.name, value))
        self.pending = None
        if value == self.value:
            return
        self.value = value
        for comp in self.components:
            comp.update()

    def set(self, value, delay = 0):
        if value == self.value:
            return
        if self.pending is not None:
            #print('removing previously scheduled change')
            self.scheduler.remove(self.pending)
        #print('scheduling change of %s to %d with delay %d' % (self.name, value, delay))
        self.pending = self.scheduler.schedule(self.__set__, (value,), delay = delay)

