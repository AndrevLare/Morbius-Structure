class Strip:
    def __init__(self):   
        self.gate = Universe()
        self.gate.next = self.gate

    def __iter__(self):
        return self.gate

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
        pass
    
    def find(self, universe):
        n = 0
        for i in self:
            if i == universe:
                return n
            n += 1

    def delete(self, index):
        pass

class Universe:
    def __init__(self, next = None,  heaven = None, hell = None):
        self.heaven = heaven
        self.hell = hell
        self.next = next

    def __next__(self):
        if self.next == self:
            raise StopIteration
        current = self.next
        return current

def main():
    strip = Strip()
    for i in range(1, 6): # Queremos números del 1 al 5
        strip.append(i, i+5)
    for i in strip:
        print(f"Cielo: {i.heaven}\tInfierno: {i.hell}")

if __name__ == "__main__":
    main()