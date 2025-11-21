from Data.MoebiusStrip import (Strip, Universe, Gate)

class MorbiusFlower:
    def __init__(self, strip):
        self.first = strip.gate
        strip.gate.next_gate = strip.gate

    def __iter__(self):
        i = self.first
        list = [i]
        while i.next_gate != self.first:
            i = i.next_gate
            list.append(i)
        return iter(list)

    def append(self, strip):

        # if self.first.next_gate == self.first:
        #     self.first.next_gate = strip
        #     strip.gate.next_gate = self.first
        #     return

        for i in self:
            if i.next_gate == self.first:
                i.next_gate = strip.gate
                strip.gate.next_gate = self.first
                return

    def add(self, index, strip):
        n = 0
        for i in self:
            if n == (index-1):
                strip.gate.next_gate = i.next_gate
                i.next_gate = strip
            n += 1

    def index(self, strip):
        n = 0
        for i in self:
            if i == strip.gate:
                return n
            n += 1

    def find(self, index):
        i = 0
        for s in self:
            if i == index:
                return s
            i += 1

    def delete(self, index):
        strip = self.find(index-1)
        strip.next_gate = strip.next_gate.next_gate

    def __str__(self):
        for strip in self:
            print("First strip:")
            print(strip)