#!/usr/bin/env python3

from queue import PriorityQueue
from collections import namedtuple

SimTime = namedtuple('SimTime', ['time', 'delta'])


class Item(namedtuple('Item', ['sim_time', 'callable', 'args'])):
    # We have to override __lt__ because PriorityQueue will try to compare
    # the entire tuple, but ordering is not defined on functions (callable).
    # We don't actually care about ordering on any field other than sim_time.
    def __lt__(self, other):
        return self.sim_time.time < other.sim_time.time

class Scheduler:
    def __init__(self):
        self.sim_time = SimTime(time = 0, delta = 0)
        self.queue = PriorityQueue()

    def reset(self):
        self.queue = PriorityQueue()

    def schedule(self, callable, args, delay = 0):
        if delay == 0:
            sim_time = SimTime(time = self.sim_time.time,
                               delta = self.sim_time.delta + 1)
        else:
            sim_time = SimTime(time = self.sim_time.time + delay,
                               delta = 0)
        item = Item(sim_time = sim_time,
                    callable = callable,
                    args = args)
        self.queue.put(item)
        return item

    def remove(self, item):
        self.queue.queue.remove(item)

    def run(self, max_events = 0):
        count = 0
        while (not self.queue.empty()) and (max_events == 0 or count < max_events):
            item = self.queue.get()
            if item.sim_time != self.sim_time:
                self.sim_time = item.sim_time
            item.callable(*item.args)
            count += 1
        return count

if __name__ == "__main__":
    def fna(a):
        print("at ", scheduler.sim_time.time, ":" , scheduler.sim_time.delta, " fna(", a, ")")

    def fnb(a, b):
        print("at ", scheduler.sim_time.time, ":", scheduler.sim_time.delta, " fnb(", a, b, ")")

    scheduler = Scheduler()

    scheduler.schedule(fna, (37,), 12)
    scheduler.schedule(fnb, (3, 5))
    scheduler.schedule(fna, (1,), 3)

    scheduler.run()
