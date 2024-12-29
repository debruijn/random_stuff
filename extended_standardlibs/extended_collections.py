# Some ideas:
# - Two-way DictList ( "x['a'] += 'b'" and "x['b'] += 'a'" do the same thing, so Dict in usage, but more like a graph in working)
# - NoHashDict (using lists to store a dict if you can't hash) -> can be used as if it is a dict but it's not
#       Go through to see what to reimplement https://docs.python.org/3/library/stdtypes.html#typesmapping
from itertools import chain


class NoHashDict:

    def __init__(self, list_tuple=None):
        if list_tuple is None:
            self._keys, self._values = tuple(), tuple()
        else:
            self._keys, self._values = list(zip(*list_tuple))

    def __str__(self):
        return "{" + ", ".join([f"{k}: {v}" for k,v in self.items()]) + "}"

    def __repr__(self):
        return self.__str__()

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
            return self[key]
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
            return self[key]
        else:
            self[key] = default
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
        return self.keys()

    def __reversed__(self):
        return reversed(self._keys)


class MaybeHashDict(NoHashDict):

    def __init__(self, list_tuple=None):
        super().__init__()
        self._dict = {}
        self._nodict = NoHashDict()
        if list_tuple is not None:
            for k, v in list_tuple:
                if self.hashash(k):
                    self._dict[k] = v
                else:
                    self._nodict[k] = v

    @staticmethod
    def hashash(obj):
        return hasattr(obj, '__hash__') and getattr(obj, '__hash__') is not None

    def __len__(self):
        return len(self._dict) + len(self._nodict)

    def clear(self):
        self._dict.clear()
        self._nodict.clear()

    def copy(self):
        new = MaybeHashDict()
        new._dict = self._dict.copy()
        new._nodict = self._nodict.copy()
        return new

    @staticmethod
    def fromkeys(iterable, value):
        return MaybeHashDict(zip(iterable, iter(lambda: value, None)))

    def items(self):
        return chain(self._dict.items(), self._nodict.items())

    def keys(self):
        yield from self._dict.keys()
        yield from self._nodict.keys()

    def values(self):
        yield from self._dict.values()
        yield from self._nodict.values()

    def pop(self, __key):
        if self.hashash(__key):
            return self._dict.pop(__key)
        else:
            return self._nodict.pop(__key)

    def popitem(self):
        if len(self._nodict) > 0:
            return self._nodict.popitem()
        else:
            return self._dict.popitem()

    def __setitem__(self, key, value):
        if self.hashash(key):
            self._dict[key] = value
        else:
            self._nodict[key] = value

    def __getitem__(self, item):
        return self._dict[item] if self.hashash(item) else self._nodict[item]

    def __contains__(self, item):
        return item in (self._dict if self.hashash(item) else self._nodict)

    def __reversed__(self):
        yield from reversed(self._nodict)
        yield from reversed(self._dict)


test1 = NoHashDict([(3, 2), (4, 1), (['koi'], 'koi')])
print(test1)

test3 = MaybeHashDict([(3, 2), (4, 1), (['koi'], 'koi')])
print(test3)

for k,v in test3.items():
    print(k, v)

for k in reversed(test3):
    print(k, test3[k])
