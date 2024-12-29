# Some ideas:
# - Two-way DictList ( "x['a'] += 'b'" and "x['b'] += 'a'" do the same thing, so Dict in usage, but more like a graph in working)
# - NoHashDict (using lists to store a dict if you can't hash) -> can be used as if it is a dict but it's not
#       Go through to see what to reimplement https://docs.python.org/3/library/stdtypes.html#typesmapping

class NoHashDict:

    def __init__(self, list_tuple):
        self._keys, self._values = list(zip(*list_tuple))

    def __str__(self):
        return "{" + ", ".join([f"{k}: {v}" for k,v in zip(self._keys, self._values)]) + "}"

    def __repr__(self):
        return "{" + ", ".join([f"{k}: {v}" for k,v in zip(self._keys, self._values)]) + "}"

    def __len__(self):
        return len(self._keys)

    def clear(self):
        self._keys, self._values = tuple(), tuple()

    def copy(self):
        return NoHashDict(zip(self._keys, self._values))

    @staticmethod
    def fromkeys(iterable, value):
        return NoHashDict(zip(iterable, iter(lambda: value, None)))

    def get(self, key, default=None):
        try:
            return self._values[self._keys.index(key)]
        except ValueError:
            return default

    def items(self):
        return iter(zip(self._keys, self._values))

    def keys(self):
        return iter(self._keys)

    def values(self):
        return iter(self._values)

    def pop(self, __key):
        try:
            index = self._keys.index(__key)
        except ValueError:
            raise KeyError(__key)
        self._keys = self._keys[:index] + self._keys[index+1:]
        val = self._values[index]
        self._values = self._values[:index] + self._values[index+1:]
        return val

    def popitem(self):
        item, self._keys, self._values = (self._keys[-1], self._values[-1]), self._keys[:-1], self._values[:-1]
        return item

    def setdefault(self, key, default=None):
        if key in self._keys:
            return self._values[self._keys.index(key)]
        else:
            self._keys += (key, )
            self._values += (default, )
            return default

    def update(self, m, **kwargs):
        if hasattr(m, 'keys'):
            for k in m.keys():
                self[k] = m[k]
        else:
            for k, v in m.items():
                self[k] = v
        for k in kwargs:
            self[k] = kwargs[k]

    def __setitem__(self, key, value):
        if key in self._keys:
            index = self._keys.index(key)
            self._values = self._values[:index] + (value,) + self._values[index+1:]
        else:
            self._keys += (key,)
            self._values += (value,)

    def __getitem__(self, item):
        return self._values[self._keys.index(item)]

    def __contains__(self, item):
        return item in self._keys

    def __iter__(self):
        return iter(self._keys)

    def __reversed__(self):
        return reversed(self._keys)
