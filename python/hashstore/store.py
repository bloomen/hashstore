import pickle
import os


class Store:

    def __init__(self):
        thisdir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(thisdir, 'hashstore.db')
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.s = pickle.load(f)
        else:
            self.s = {}

    def clear(self):
        self.s.clear()
        self._save()

    def size(self):
        return len(self.s)

    def put(self, key, value):
        self.s[key] = value
        self._save()

    def get(self, key):
        return self.s.get(key)

    def key(self, index):
        for i, k in enumerate(self.s.keys()):
            if i == index:
                return k

    def remove(self, key):
        del self.s[key]
        self._save()

    def _save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.s, f)
