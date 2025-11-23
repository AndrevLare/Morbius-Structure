class Strip:
    def __init__(self):   
        self.gate = Gate(self)
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

    def add(self, index, heaven, hell):
        n = 0
        for i in self:
            if n == (index-1):
                universe = Universe(None, heaven, hell)
                universe.next = i.next
                i.next = universe
                return
            n += 1
        self.append(heaven, hell)
    
    def index(self, heaven, hell):
        n = 0
        for i in self:
            if i.heaven == heaven and i.hell == hell:
                return n
            n += 1
        raise KeyError ("Universe not found in strip")

    def find(self, index):
        i = 0
        for u in self:
            if i == index:
                return u
            i += 1
        raise IndexError (f"Not enough universes to reach index {index}")
    
    def delete(self, index):
        u = self.find(index-1)
        u.next = u.next.next

    def __str__(self):
        n = 0
        print("Index\t|Heaven\t|Hell")
        for i in self:
            print(f"{n}\t|{i}")
            n += 1
        return ""

class Universe:
    def __init__(self, next = None,  heaven = None, hell = None):
        self.heaven = heaven
        self.hell = hell
        self.next = next

    def __str__(self):
        return f"{self.heaven}\t|{self.hell}"

class Gate(Universe):
    def __init__(self, strip):
        super().__init__()
        self.next_gate = None
        self.strip = strip

    def __str__(self):
        return f"{self.strip}"

def main():
    strip = Strip()
    for i in range(1, 6):
        strip.append(i, i+5)
    print (strip)

if __name__ == "__main__":
    main()