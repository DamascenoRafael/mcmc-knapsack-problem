class State():

    items = None
    v = 0
    w = 0

    def __init__(self):
        self.items = []
        self.v = 0
        self.w = 0

    def setIn(self, index, v, w):
        if self.items[index] != 1:
            self.items[index] = 1
            self.w += w
            self.v += v
        return self

    def setOut(self, index, v, w):
        if self.items[index] != 0:
            self.items[index] = 0
            self.w -= w
            self.v -= v
        return self

    def copy(self):
        obj_copy = State()
        obj_copy.items = self.items[:]
        obj_copy.v += self.v
        obj_copy.w += self.w
        return obj_copy

    def __repr__(self):
        return str(self.items) + ',' + str(self.v) + ',' + str(self.w)

    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self, other):
        return self.items == other.items
    
    def __gt__(self, other):
        return self.v > other.v