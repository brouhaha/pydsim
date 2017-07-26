#!/usr/bin/env python3

from scheduler import Scheduler
from signal import Signal
from component import Component

class NAND(Component):
    __serial__ = 0
    __sc_debug__ = False

    @classmethod
    def set_global_debug(cls, value):
        cls.__sc_debug__ = value

    @classmethod
    def get_global_debug(cls):
        return cls.__sc_debug__

    def __init__(self, scheduler,
                 inputs,
                 output,
                 name = None,
                 prop_delay = 0):
        super().__init__(scheduler)
        self.debug = False
        self.inputs = [i.bind(self) for i in inputs]
        if output is None:
            output = Signal(scheduler)
        self.output = output
        if name is None:
            NAND.__serial__ += 1
            name = "NAND%d" % NAND.__serial__
        self.name = name
        self.prop_delay = prop_delay

    def set_debug(self, value):
        self.debug = value

    def get_debug(self):
        return self.debug

    def update(self):
        if any (input.get() == 0 for input in self.inputs):
            new_val = 1
        else:
            new_val = 0
        if NAND.__sc_debug__ or self.debug:
            print("%s: updating %s to %d" %(self.name, self.output.name, new_val))
            print("listeners:")
            for l in self.output.components:
                print(" %s" % l.name, end = '')
            print()
        self.output.set(new_val,
                        delay = self.prop_delay)

if __name__ == '__main__':
    scheduler = Scheduler()
    a = Signal(scheduler, name = 'a')
    b = Signal(scheduler, name = 'b')
    c = Signal(scheduler, name = 'c')
    n1 = NAND(scheduler, inputs = [a, b], output = c)

    n2 = NAND(scheduler, inputs = [a, b], output = c)

    scheduler.run()

    
