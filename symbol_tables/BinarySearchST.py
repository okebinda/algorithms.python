"""Symbol Table: Binary Search"""


class BinarySearchST:
    """A symbol table with key:value pairs implemented in parallel lists.
    Performs key lookup using binary search."""

    def __init__(self):
        """BinarySearchST constructor"""

        self._keys = []
        self._values = []
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

    def rank(self, key):
        """Determines the zero-indexed position of the given key if it exists,
        or where it would be inserted if it doesn't exist

        :param key: Lookup key
        :type key: str
        :return: The zero-indexed position (rank) or insertion point of the key
        :rtype: int
        """

        lo = 0
        hi = len(self) - 1
        while lo <= hi:
            mid = (hi + lo) // 2
            if key < self._keys[mid]:
                hi = mid - 1
            elif key > self._keys[mid]:
                lo = mid + 1
            else:
                return mid
        return lo

    def __setitem__(self, key, value):
        """Sets the element with given key to given value, adds element if
        does not exist

        :param key: Lookup key
        :type key: str
        :param value: Any data value
        """

        i = self.rank(key)
        if i < len(self) and key == self._keys[i]:
            self._values[i] = value
            return
        self._keys.insert(i, key)
        self._values.insert(i, value)
        self._n += 1

    def __getitem__(self, key):
        """Retrieves the value of the element with a given key if it exists

        :param key: Lookup key
        :type key: str
        :return: Value of element found at the lookup key
        :raises: KeyError
        """

        i = self.rank(key)
        if i < len(self) and key == self._keys[i]:
            return self._values[i]
        raise KeyError("Key `{}` not found.".format(key))

    def __delitem__(self, key):
        """Removes the element with the given key if it exists

        :param key: Lookup key
        :type key: str
        :raises: KeyError
        """
        
        i = self.rank(key)
        if i < len(self) and key == self._keys[i]:
            self._keys.pop(i)
            self._values.pop(i)
            self._n -= 1
            return
        raise KeyError("Key `{}` not found.".format(key))

    def min(self):
        """Finds the key with the lowest rank

        :return: The lookup key with the lowest rank
        :rtype: str
        :raises: Exception
        """

        if not bool(self):
            raise Exception("BinarySearchST is empty.")
        return self._keys[0]

    def max(self):
        """Finds the key with the highest rank

        :return: The lookup key with the highest rank
        :rtype: str
        :raises: Exception
        """

        if not bool(self):
            raise Exception("BinarySearchST is empty.")
        return self._keys[-1]

    def select(self, k):
        """Finds the key at the given index

        :param k: Zero-based index for key's position
        :type k: int
        :return: Lookup key at index
        :rtype: str
        :raises: IndexError
        """

        return self._keys[k]

    def floor(self, key):
        """Finds the highest ranking key that is not higher than the given key

        :param key: Value to compare keys against
        :type key: str
        :return: The highest ranking key that is not higher than the given key
        :rtype: str
        :raises: Exception
        """

        i = self.rank(key)
        if i == 0 and key != self._keys[i]:
            raise Exception("Illegal argument.")
        return self._keys[i] if (i < len(self) and
                                 key == self._keys[i]) else self._keys[i-1]

    def ceiling(self, key):
        """Finds the lowest ranking key that is not lower than the given key

        :param key: Value to compare keys against
        :type key: str
        :return: The lowest ranking key that is not lower than the given key
        :rtype: str
        :raises: Exception
        """
        
        i = self.rank(key)
        if i >= len(self):
            raise Exception("Illegal argument.")
        return self._keys[i]

    def __iter__(self):
        """Iterates over the symbol table in order. Generates a sequence of
        keys"""

        return iter(self._keys)

    def __reversed__(self):
        """Iterates over the symbol table in reverse order. Generates a
        sequence of keys"""

        for i in range(self._n-1, -1, -1):
            yield self._keys[i]

    def __contains__(self, key):
        """Checks if lookup key is in symbol table

        :param key: Lookup key
        :type key: str
        :return: True if key exists, otherwise False
        :rtype: bool
        """

        i = self.rank(key)
        return True if i < len(self) and key == self._keys[i] else False

    def keys(self):
        """Alias for __iter__()"""
        
        return iter(self._keys)

    def values(self):
        """Iterates over the symbol table in order. Generates a sequence of
        values"""

        return iter(self._values)

    def items(self):
        """Iterates over the symbol table in order. Generates a sequence of
        (key, value) pairs"""

        for i in range(len(self)):
            yield self._keys[i], self._values[i]


if __name__ == "__main__":

    import unittest


    class TestBinarySearchST(unittest.TestCase):

        st = None

        def setUp(self):
            self.st = BinarySearchST()
            self.st["m"] = "Letter M"
            self.st["c"] = "Letter C"
            self.st["s"] = "Letter S"
            self.st["t"] = "Letter T"
            self.st["b"] = "Letter B"
            self.st["y"] = "Letter Y"

        def test_len(self):
            self.assertEqual(6, len(self.st))
            self.assertEqual(0, len(BinarySearchST()))

        def test_bool(self):
            self.assertTrue(bool(self.st))
            self.assertFalse(bool(BinarySearchST()))

        def test_rank(self):
            self.assertEqual(0, self.st.rank("b"))
            self.assertEqual(1, self.st.rank("c"))
            self.assertEqual(2, self.st.rank("m"))
            self.assertEqual(3, self.st.rank("s"))
            self.assertEqual(4, self.st.rank("t"))
            self.assertEqual(5, self.st.rank("y"))

        def test_setitem(self):
            self.st["a"] = "Letter A"
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

            self.assertRaises(KeyError, BinarySearchST().__getitem__, 'a')

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
            self.assertRaises(KeyError, BinarySearchST().__delitem__, 'a')

        def test_min(self):
            self.assertEqual('b', self.st.min())
            self.assertRaises(Exception, BinarySearchST().min)

        def test_max(self):
            self.assertEqual('y', self.st.max())
            self.assertRaises(Exception, BinarySearchST().max)

        def test_select(self):
            self.assertEqual('b', self.st.select(0))
            self.assertEqual('c', self.st.select(1))
            self.assertEqual('m', self.st.select(2))
            self.assertEqual('s', self.st.select(3))
            self.assertEqual('t', self.st.select(4))
            self.assertEqual('y', self.st.select(5))
            self.assertRaises(IndexError, self.st.select, 6)

            self.assertRaises(IndexError, BinarySearchST().select, 0)

        def test_floor(self):
            self.assertEqual("b", self.st.floor('b'))
            self.assertEqual("c", self.st.floor('c'))
            self.assertEqual("c", self.st.floor('d'))
            self.assertEqual("m", self.st.floor('m'))
            self.assertEqual("m", self.st.floor('n'))
            self.assertRaises(Exception, self.st.floor, 'a')

            self.assertRaises(Exception, BinarySearchST().floor, 'm')

        def test_ceiling(self):
            self.assertEqual("y", self.st.ceiling('y'))
            self.assertEqual("y", self.st.ceiling('x'))
            self.assertEqual("t", self.st.ceiling('t'))
            self.assertEqual("s", self.st.ceiling('s'))
            self.assertEqual("s", self.st.ceiling('r'))
            self.assertRaises(Exception, self.st.ceiling, 'z')

            self.assertRaises(Exception, BinarySearchST().ceiling, 'm')

        def test_iter(self):
            keys = ['b', 'c', 'm', 's', 't', 'y']
            self.assertEqual(keys, list(self.st))
            self.assertEqual(keys, [x for x in self.st])
            self.assertEqual(keys, [*self.st])

            self.assertEqual([], list(BinarySearchST()))

        def test_reversed(self):
            rkeys = ['y', 't', 's', 'm', 'c', 'b']
            self.assertEqual(rkeys, list(reversed(self.st)))
            self.assertEqual(rkeys, [x for x in reversed(self.st)])
            self.assertEqual(rkeys, [*reversed(self.st)])

            self.assertEqual([], list(reversed(BinarySearchST())))

        def test_contains(self):
            self.assertTrue('m' in self.st)
            self.assertFalse('a' in self.st)

            self.assertFalse('m' in BinarySearchST())

        def test_keys(self):
            keys = ['b', 'c', 'm', 's', 't', 'y']
            self.assertEqual(keys, list(self.st.keys()))
            self.assertEqual(keys, [x for x in self.st.keys()])
            self.assertEqual(keys, [*self.st.keys()])

            self.assertEqual([], list(BinarySearchST().keys()))

        def test_values(self):
            values = ["Letter B", "Letter C", "Letter M", "Letter S",
                      "Letter T", "Letter Y"]
            self.assertEqual(values, list(self.st.values()))
            self.assertEqual(values, [x for x in self.st.values()])
            self.assertEqual(values, [*self.st.values()])

            self.assertEqual([], list(BinarySearchST().values()))

        def test_items(self):
            items = [
                ('b', "Letter B"),
                ('c', "Letter C"),
                ('m', "Letter M"),
                ('s', "Letter S"),
                ('t', "Letter T"),
                ('y', "Letter Y")
            ]
            self.assertEqual(items, list(self.st.items()))
            self.assertEqual(items, [x for x in self.st.items()])
            self.assertEqual(items, [*self.st.items()])

            self.assertEqual([], list(BinarySearchST().items()))


    unittest.main()
