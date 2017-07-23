#!/usr/bin/env python3

from scheduler import Scheduler
from signal import Signal
from component import Component

class NAND(Component):
    __serial__ = 0
    
    def __init__(self, scheduler,
                 inputs,
                 output,
                 name = None,
                 prop_delay = 0):
        super().__init__(scheduler)
        self.inputs = [i.bind(self) for i in inputs]
        if output is None:
            output = Signal(scheduler)
        self.output = output
        if name is None:
            NAND.__serial__ += 1
            name = "NAND%d" % NAND.__serial__
        self.name = name
        self.prop_delay = prop_delay

    def update(self):
        #print(self.name, " update")
        self.output.set(any (input.get() == 0 for input in self.inputs),
                        delay = self.prop_delay)

if __name__ == '__main__':
    scheduler = Scheduler()
    a = Signal(scheduler, name = 'a')
    b = Signal(scheduler, name = 'b')
    c = Signal(scheduler, name = 'c')
    n1 = NAND(scheduler, inputs = [a, b], output = c)

    n2 = NAND(scheduler, inputs = [a, b], output = c)

    scheduler.run()

    
