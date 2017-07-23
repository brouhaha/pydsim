#!/usr/bin/env python3

from scheduler import Scheduler
from signal import Signal
from component import Component

class StateWatcher(Component):
    __serial__ = 0
    
    def __init__(self, scheduler,
                 input,
                 name = None):
        super().__init__(scheduler)
        self.input = input.bind(self)
        if name is None:
            StateWatcher.__serial__ += 1
            name = "StateWatcher%d" % StateWatcher.__serial__
        self.name = name
        self.prev_value = None

    def update(self):
        value = self.input.get()
        if value != self.prev_value:
            print("%s update to %d" % (self.name, value))
            self.prev_value = value
