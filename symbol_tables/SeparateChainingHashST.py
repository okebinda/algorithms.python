"""Symbol Table: Separate Chaining Hash"""

from .SequentialSearchST import SequentialSearchST


class SeparateChainingHashST:
    """A symbol table with key:value pairs implemented using a hash function on
    the keys to store items, maintaining fast lookup times. A regular list is
    used to maintain key -> hash (int) mappings, with each list item being a
    sequential search symbol table to handle hash collisions."""

    def __init__(self, m=997):
        """SeparateChainingHashST constructor

        :param m: Size of internal list
        :type m: int
        """

        self._m = m
        self._st = [None] * self._m
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

    def __setitem__(self, key, value):
        """Sets the element with given key to given value, adds element if
        does not exist

        :param key: Lookup key
        :type key: str
        :param value: Any data value
        """

        h = self._hash(key)
        if self._st[h] is None:
            self._st[h] = SequentialSearchST()
        if key not in self:
            self._n += 1
        self._st[h][key] = value

    def __getitem__(self, key):
        """Retrieves the value of the element with a given key if it exists

        :param key: Lookup key
        :type key: str
        :return: Value of element found at the lookup key
        :raises: KeyError
        """

        h = self._hash(key)
        if self._st[h] is None:
            raise KeyError("Key `{}` not found.".format(key))
        return self._st[h][key]

    def __delitem__(self, key):
        """Removes the element with the given key if it exists

        :param key: Lookup key
        :type key: str
        :raises: KeyError
        """

        h = self._hash(key)
        if self._st[h] is None:
            raise KeyError("Key `{}` not found".format(key))
        del self._st[h][key]
        self._n -= 1

    def __contains__(self, key):
        """Checks if lookup key is in symbol table

        :param key: Lookup key
        :type key: str
        :return: True if key exists, otherwise False
        :rtype: bool
        """

        h = self._hash(key)
        if self._st[h] is None:
            return False
        return True if self._st[h] else False

    def __iter__(self):
        """Iterates over the symbol table, order is not preserved. Generates
        a sequence of keys."""

        for chain in self._st:
            if chain:
                for key in chain:
                    yield key

    def keys(self):
        """Alias for __iter__()"""

        return iter(self)

    def values(self):
        """Iterates over the symbol table, order is not preserved. Generates
        a sequence of values."""

        for chain in self._st:
            if chain:
                for key in chain:
                    yield chain[key]

    def items(self):
        """Iterates over the symbol table, order is not preserved. Generates
        a sequence of (key, value) pairs."""

        for chain in self._st:
            if chain:
                for key in chain:
                    yield key, chain[key]


if __name__ == "__main__":

    import unittest


    class TestSeparateChainingHashST(unittest.TestCase):

        st = None

        def setUp(self):
            self.st = SeparateChainingHashST()
            self.st['m'] = "Letter M"
            self.st['c'] = "Letter C"
            self.st['s'] = "Letter S"
            self.st['t'] = "Letter T"
            self.st['b'] = "Letter B"
            self.st['y'] = "Letter Y"

        def test_len(self):
            self.assertEqual(6, len(self.st))
            self.assertEqual(0, len(SeparateChainingHashST()))

        def test_bool(self):
            self.assertTrue(bool(self.st))
            self.assertFalse(bool(SeparateChainingHashST()))

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
            self.assertEqual("Letter B", self.st['b'])
            self.assertEqual("Letter Y", self.st['y'])
            self.assertRaises(KeyError, self.st.__getitem__, 'a')

            self.assertRaises(KeyError,
                              SeparateChainingHashST().__getitem__, 'a')

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

            del self.st['b']
            self.assertEqual(1, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 'b')

            del self.st['y']
            self.assertEqual(0, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 'y')

            self.assertRaises(KeyError, self.st.__delitem__, 'a')

            self.assertRaises(KeyError,
                              SeparateChainingHashST().__delitem__, 'a')

        def test_contains(self):
            self.assertTrue('m' in self.st)
            self.assertFalse('a' in self.st)

            self.assertFalse('a' in SeparateChainingHashST())

        def test_iter(self):
            sorted_keys = ['b', 'c', 'm', 's', 't', 'y']
            self.assertEqual(sorted_keys, sorted(self.st))
            self.assertEqual(sorted_keys, sorted([x for x in self.st]))
            self.assertEqual(sorted_keys, sorted([*self.st]))

            self.assertEqual([], sorted(SeparateChainingHashST()))

        def test_keys(self):
            skeys = ['b', 'c', 'm', 's', 't', 'y']
            self.assertEqual(skeys, sorted(self.st.keys()))
            self.assertEqual(skeys, sorted([x for x in self.st.keys()]))
            self.assertEqual(skeys, sorted([*self.st.keys()]))

            self.assertEqual([], sorted(SeparateChainingHashST().keys()))

        def test_values(self):
            svalues = ["Letter B", "Letter C", "Letter M", "Letter S",
                       "Letter T", "Letter Y"]
            self.assertEqual(svalues, sorted(self.st.values()))
            self.assertEqual(svalues, sorted([x for x in self.st.values()]))
            self.assertEqual(svalues, sorted([*self.st.values()]))

            self.assertEqual([], sorted(SeparateChainingHashST().values()))

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

            self.assertEqual([], sorted(SeparateChainingHashST().items()))


    unittest.main()
