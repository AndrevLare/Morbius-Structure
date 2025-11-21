class Strip:
    def __init__(self):   
        self.gate = Gate()
        self.gate.next = self.gate

    def __iter__(self):
        i = self.gate
        list = []
        while i.next != self.gate:
            i = i.next
            list.append(i)
        return iter(list)

    def append(self, heaven =  None, hell = None):
        if self.gate.next == self.gate:
            universe = Universe(self.gate, heaven, hell)
            self.gate.next = universe
            return
        for i in self:
            if i.next == self.gate:
                universe = Universe(self.gate, heaven, hell)
                i.next = universe
                return

    def add(self, index, universe):
        n = 0
        for i in self:
            if n == (index-1):
                universe.next = i.next
                i.next = universe
            n += 1
    
    def index(self, universe):
        n = 0
        for i in self:
            if i == universe:
                return n
            n += 1

    def find(self, index):
        i = 0
        for u in self:
            if i == index:
                return u
            i += 1

    def delete(self, index):
        u = self.find(index-1)
        u.next = u.next.next

    def __str__(self):
        n = 0
        print("Index\t|Heaven\t|Hell")
        for i in self:
            print(f"{n}\t|{i.heaven}\t|{i.hell}")
            n += 1
        return ""

class Universe:
    def __init__(self, next = None,  heaven = None, hell = None):
        self.heaven = heaven
        self.hell = hell
        self.next = next

class Gate(Universe):
    def __init__(self):
        super().__init__()
        self.next_gate = None


def main():
    strip = Strip()
    for i in range(1, 6):
        strip.append(i, i+5)
    print (strip)
if __name__ == "__main__":
    main()