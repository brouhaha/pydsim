#!/usr/bin/env python3

from scheduler import Scheduler
from signal import Signal
from component import Component
from nand import NAND
from state_watcher import StateWatcher

class DFF(Component):
    def __init__(self, scheduler,
                 clk, d, not_pre, not_clr,
                 q, not_q):
        super().__init__(scheduler)

        # We don't need to bind the inputs, because they are all going to
        # subcomponents which will bind them.
        self.clk       = clk
        self.d         = d
        self.not_pre   = not_pre
        self.not_clr   = not_clr

        if q is None:
            q = Signal(scheduler)
        self.q         = q
        if not_q is None:
            not_q = Signal(scheduler)
        self.not_q     = not_q

        self.sr1_q     = Signal(scheduler)
        self.sr1_not_q = Signal(scheduler)
        self.sr2_q     = Signal(scheduler)
        self.sr2_not_q = Signal(scheduler)

        self.n1 = NAND(scheduler,
                       inputs = (self.not_pre, self.sr2_not_q, self.sr1_not_q),
                       output = self.sr1_q)
        self.n2 = NAND(scheduler,
                       inputs = (self.not_clr, self.clk,       self.sr1_q),
                       output = self.sr1_not_q)

        self.n3 = NAND(scheduler,
                       inputs = (self.clk,     self.sr1_not_q, self.sr2_not_q),
                       output = self.sr2_q)
        self.n4 = NAND(scheduler,
                       inputs = (self.d,       self.not_clr,   self.sr2_q),
                       output = self.sr2_not_q)

        self.n5 = NAND(scheduler,
                       inputs = (self.not_pre, self.sr1_not_q, self.not_q),
                       output = self.q)
        self.n6 = NAND(scheduler,
                       inputs = (self.not_clr, self.sr2_q,     self.q),
                       output = self.not_q)

if __name__ == '__main__':
    scheduler = Scheduler()
    clk     = Signal(scheduler, value = 0, name = 'clk')
    d       = Signal(scheduler, value = 0, name = 'd')
    not_pre = Signal(scheduler, value = 1, name = 'not_pre')
    not_clr = Signal(scheduler, value = 1, name = 'not_clr')
    q       = Signal(scheduler,            name = 'q')
    not_q   = Signal(scheduler,            name = 'not_q')

    dff = DFF(scheduler, clk, d, not_pre, not_clr, q, not_q)

    q_watcher     = StateWatcher(scheduler, q,     name = 'q')
    not_q_watcher = StateWatcher(scheduler, not_q, name = 'not_q')

    scheduler.run()

    print('setting not_clr to 0')
    not_clr.set(0)
    scheduler.run()

    print('setting not_clr to 1')
    not_clr.set(1)
    scheduler.run()

    print('setting d to 1')
    d.set(1)
    scheduler.run()

    print('setting clk to 1')
    clk.set(1)
    scheduler.run()
    
    print('setting clk to 0')
    clk.set(0)
    scheduler.run()

    print('setting d to 0')
    d.set(0)
    scheduler.run()

    print('setting clk to 1')
    clk.set(1)
    scheduler.run()
    
    print('setting clk to 0')
    clk.set(0)
    scheduler.run()
    
