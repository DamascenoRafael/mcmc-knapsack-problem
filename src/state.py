class State():

    items = None    # list indicating the presence of items in the state
    v = 0           # total value of state - sum of item values
    w = 0           # total weight of state - sum of item weights

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