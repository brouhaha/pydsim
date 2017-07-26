#!/usr/bin/env python3

class Signal:
    __serial__ = 0
    __sc_debug__ = False

    @classmethod
    def set_global_debug(cls, value):
        cls.__sc_debug__ = value

    @classmethod
    def get_global_debug(cls):
        return cls.__sc_debug__

    def __init__(self, scheduler, value = 0, name = None):
        self.scheduler  = scheduler
        self.components = []
        self.pending    = None
        self.debug      = False

        if name is None:
            Signal.__serial__ += 1
            name = "Signal%d" % Signal.__serial__
        self.name = name

        self.value      = None
        self.set(value)
        self.value = value

    def reinit(self, value):
        self.value = None
        self.set(value)
        self.value = value

    def set_debug(self, value):
        self.debug = value

    def get_debug(self):
        return self.debug

    def bind(self, component):
        self.components.append(component)
        return self

    def get(self):
        return self.value

    def __set__(self, value):
        if Signal.__sc_debug__ or self.debug:
            print('setting %s to %d' % (self.name, value))
        self.pending = None
        #if value == self.value:
        #    return
        self.value = value
        for comp in self.components:
            if Signal.__sc_debug__ or self.debug:
                print("scheduling update of %s" % comp.name)
            self.scheduler.schedule(comp.update, (), delay = 0)

    def set(self, value, delay = 0):
        if value == self.value:
            return
        if self.pending is not None:
            if Signal.__sc_debug__ or self.debug:
                print('removing previously scheduled change')
            self.scheduler.remove(self.pending)
        if Signal.__sc_debug__ or self.debug:
            print('scheduling change of %s to %d with delay %d' % (self.name, value, delay))
        self.pending = self.scheduler.schedule(self.__set__, (value,), delay = delay)

