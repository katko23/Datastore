class CounterS:
    def __init__(self, i, j, k):
        self.i1 = i
        self.i2 = j
        self.i3 = k

    def Pass(self):
        self.i1 = ( self.i1 + 1 ) % 3 + 1
        self.i2 = (self.i2 + 1) % 3 + 1
        self.i3 = (self.i3 + 1) % 3 + 1