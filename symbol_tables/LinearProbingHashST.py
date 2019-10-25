"""Symbol Table: Linear Probing Hash"""


class LinearProbingHashST:
    """A symbol table with key:value pairs implemented using a hash function on
    the keys to store items, maintaining fast lookup times. Two regular lists
    are used internally for storage - one for keys and one for values - with
    matching indexes. The keys list maintains a key -> (int) hash:key mapping,
    while the values list maintains a key -> (int) hash:value mapping. Hash
    collisions are handled by incrementing the hash index by one until an empty
    slot is found."""

    def __init__(self, cap=16):
        """LinearProbingHashST constructor

        :param cap: Size of internal list
        :type cap: int
        """

        self._m = cap
        self._keys = [None for _ in range(self._m)]
        self._values = [None for _ in range(self._m)]
        self._n = 0

    def __len__(self):
        """Reports number of elements in the symbol table

        :return: Length of symbol table
        :rtype: int
        """
        
        return self._n

    def __bool__(self):
        """Reports if symbol table contains any elements

        :return: False if empty, True otherwise
        :rtype: bool
        """

        return self._n > 0

    def _hash(self, key):
        """Hash function to turn a key into a (int) list index

        :param key: Lookup key
        :param key: str
        :return: They key's hash value used as the list index
        :rtype: int
        """

        return hash(key) % self._m

    def _resize(self, cap):
        """Resizes the internal storage list

        :param cap: New size for the internal lists
        :type cap: int
        """

        t = LinearProbingHashST(cap)
        for i in range(self._m):
            if self._keys[i] is not None:
                t[self._keys[i]] = self._values[i]
        self._m = t._m
        self._keys = t._keys
        self._values = t._values

    def __setitem__(self, key, value):
        """Sets the element with given key to given value, adds element if
        does not exist

        :param key: Lookup key
        :type key: str
        :param value: Any data value
        """

        if self._n >= self._m / 2:
            self._resize(self._m * 2)

        i = self._hash(key)
        while self._keys[i] is not None:
            if key == self._keys[i]:
                self._values[i] = value
                return
            i = (i + 1) % self._m

        self._keys[i] = key
        self._values[i] = value
        self._n += 1

    def __getitem__(self, key):
        """Retrieves the value of the element with a given key if it exists

        :param key: Lookup key
        :type key: str
        :return: Value of element found at the lookup key
        :raises: KeyError
        """

        i = self._hash(key)
        while self._keys[i] is not None:
            if key == self._keys[i]:
                return self._values[i]
            i = (i + 1) % self._m
        raise KeyError("Key `{}` not found.".format(key))

    def __delitem__(self, key):
        """Removes the element with the given key if it exists

        :param key: Lookup key
        :type key: str
        :raises: KeyError
        """

        if key not in self:
            raise KeyError("Key `{}` not found.".format(key))

        i = self._hash(key)
        while key != self._keys[i]:
            i = (i + 1) % self._m
        self._keys[i] = None
        self._values[i] = None

        i = (i + 1) % self._m
        while self._keys[i] is not None:
            key_to_redo = self._keys[i]
            value_to_redo = self._values[i]
            self._keys[i] = None
            self._values[i] = None
            self._n -= 1
            self[key_to_redo] = value_to_redo
            i = (i + 1) % self._m

        self._n -= 1
        if self._n > 3 and self._n <= self._m / 8:
            self._resize(self._m // 2)

    def __contains__(self, key):
        """Checks if lookup key is in symbol table

        :param key: Lookup key
        :type key: str
        :return: True if key exists, otherwise False
        :rtype: bool
        """

        i = self._hash(key)
        while self._keys[i] is not None:
            if key == self._keys[i]:
                return True
            i = (i + 1) % self._m
        return False

    def __iter__(self):
        """Iterates over the symbol table, order is not preserved. Generates
        a sequence of keys."""

        for i in range(self._m):
            if self._keys[i] is not None:
                yield self._keys[i]

    def keys(self):
        """Alias for __iter__()"""

        return iter(self)

    def values(self):
        """Iterates over the symbol table, order is not preserved. Generates
        a sequence of values."""

        for i in range(self._m):
            if self._keys[i] is not None:
                yield self._values[i]

    def items(self):
        """Iterates over the symbol table, order is not preserved. Generates
        a sequence of (key, value) pairs."""

        for i in range(self._m):
            if self._keys[i] is not None:
                yield self._keys[i], self._values[i]


if __name__ == "__main__":

    import unittest


    class TestLinearProbingHashST(unittest.TestCase):

        st = None

        def setUp(self):
            self.st = LinearProbingHashST()
            self.st['m'] = "Letter M"
            self.st['c'] = "Letter C"
            self.st['s'] = "Letter S"
            self.st['t'] = "Letter T"
            self.st['y'] = "Letter Y"
            self.st['b'] = "Letter B"

        def test_len(self):
            self.assertEqual(6, len(self.st))
            self.assertEqual(0, len(LinearProbingHashST()))

        def test_bool(self):
            self.assertTrue(bool(self.st))
            self.assertFalse(bool(LinearProbingHashST()))

        def test_setitem(self):
            self.st['a'] = "Letter A"
            self.assertEqual(7, len(self.st))
            self.assertEqual("Letter A", self.st['a'])

            self.st['s'] = "Character S"
            self.assertEqual(7, len(self.st))
            self.assertEqual("Character S", self.st['s'])

        def test_getitem(self):
            self.assertEqual("Letter M", self.st['m'])
            self.assertEqual("Letter C", self.st['c'])
            self.assertEqual("Letter S", self.st['s'])
            self.assertEqual("Letter T", self.st['t'])
            self.assertEqual("Letter Y", self.st['y'])
            self.assertEqual("Letter B", self.st['b'])
            self.assertRaises(KeyError, self.st.__getitem__, 'a')

            self.assertRaises(KeyError, LinearProbingHashST().__getitem__, 'a')

        def test_delitem(self):
            del self.st['m']
            self.assertEqual(5, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 'm')

            del self.st['c']
            self.assertEqual(4, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 'c')

            del self.st['s']
            self.assertEqual(3, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 's')

            del self.st['t']
            self.assertEqual(2, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 't')

            del self.st['y']
            self.assertEqual(1, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 'y')

            del self.st['b']
            self.assertEqual(0, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 'b')

            self.assertRaises(KeyError, self.st.__delitem__, 'a')

        def test_contains(self):
            self.assertTrue('m' in self.st)
            self.assertFalse('a' in self.st)

            self.assertFalse('a' in LinearProbingHashST())

        def test_iter(self):
            skeys = ['b', 'c', 'm', 's', 't', 'y']
            self.assertEqual(skeys, sorted(self.st))
            self.assertEqual(skeys, sorted([x for x in self.st]))
            self.assertEqual(skeys, sorted([*self.st]))

            self.assertEqual([], sorted(LinearProbingHashST()))

        def test_keys(self):
            skeys = ['b', 'c', 'm', 's', 't', 'y']
            self.assertEqual(skeys, sorted(self.st.keys()))
            self.assertEqual(skeys, sorted([x for x in self.st.keys()]))
            self.assertEqual(skeys, sorted([*self.st.keys()]))

            self.assertEqual([], sorted(LinearProbingHashST().keys()))

        def test_values(self):
            sletters = ["Letter B", "Letter C", "Letter M", "Letter S",
                        "Letter T", "Letter Y"]
            self.assertEqual(sletters, sorted(self.st.values()))
            self.assertEqual(sletters, sorted([x for x in self.st.values()]))
            self.assertEqual(sletters, sorted([*self.st.values()]))

            self.assertEqual([], sorted(LinearProbingHashST().values()))

        def test_items(self):
            sitems = [
                ('b', "Letter B"),
                ('c', "Letter C"),
                ('m', "Letter M"),
                ('s', "Letter S"),
                ('t', "Letter T"),
                ('y', "Letter Y")
            ]
            self.assertEqual(sitems, sorted(self.st.items()))
            self.assertEqual(sitems, sorted([x for x in self.st.items()]))
            self.assertEqual(sitems, sorted([*self.st.items()]))

            self.assertEqual([], sorted(LinearProbingHashST().items()))

        def test_resize(self):
            self.assertEqual(16, self.st._m)
            self.st["a"] = "Letter A"
            self.st["d"] = "Letter D"
            self.st["e"] = "Letter E"
            self.st["f"] = "Letter F"
            self.assertEqual(32, self.st._m)
            del self.st["a"]
            del self.st["b"]
            del self.st["c"]
            del self.st["d"]
            del self.st["e"]
            del self.st["f"]
            self.assertEqual(16, self.st._m)


    unittest.main()
