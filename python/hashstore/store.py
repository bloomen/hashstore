

class Store:

    def __init__(self):
        self.s = {}

    def clear(self):
        self.s.clear()

    def size(self):
        return len(self.s)

    def put(self, key, value):
        self.s[key] = value

    def get(self, key):
        return self.s.get(key)

    def key(self, index):
        for i, k in enumerate(self.s.keys()):
            if i == index:
                return k

    def remove(self, key):
        del self.s[key]
