"""Symbol Table: Sequential Search"""

from collections.abc import MutableMapping


class SequentialSearchST(MutableMapping):
    """A symbol table with key:value pairs implemented as a singly linked
    list. Performs key lookup sequentially starting with most recently added
    element."""

    class _Node:
        """A data node in the symbol table"""

        __slots__ = 'key', 'value', 'next'

        def __init__(self, key, value, next):
            """Node constructor

            :param key: Lookup key
            :type key: str
            :param value: Any data value
            :param next: The next node in the symbol table
            :type next: _Node
            """

            self.key = key
            self.value = value
            self.next = next

    def __init__(self):
        """SequentialSearchST constructor"""

        self._head = None
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

    def __setitem__(self, key, value):
        """Sets the element with given key to given value, adds element if
        does not exist

        :param key: Lookup key
        :type key: str
        :param value: Any data value
        """

        node = self._head
        while node is not None:
            if key == node.key:
                node.value = value
                return
            node = node.next
        self._head = self._Node(key, value, self._head)
        self._n += 1

    def __getitem__(self, key):
        """Retrieves the value of the element with a given key if it exists

        :param key: Lookup key
        :type key: str
        :return: Value of element found at the lookup key
        :raises: KeyError
        """

        node = self._head
        while node is not None:
            if key == node.key:
                return node.value
            node = node.next
        raise KeyError("Key `{}` not found.".format(key))

    def __delitem__(self, key):
        """Removes the element with the given key if it exists

        :param key: Lookup key
        :type key: str
        :raises: KeyError
        """

        node = self._head
        prev_node = None
        while node is not None:
            if key == node.key:
                if prev_node is None:
                    self._head = node.next
                else:
                    prev_node.next = node.next
                self._n -= 1
                return
            prev_node = node
            node = node.next
        raise KeyError("Key `{}` not found.".format(key))

    def __iter__(self):
        """Iterates over the symbol table, most recently added to last.
        Generates a sequence of keys"""

        node = self._head
        while node is not None:
            yield node.key
            node = node.next
        return self

    def __reversed__(self):
        """Iterates over the symbol table, last added element to the first.
        Generates a sequence of keys."""

        return self._prev(self._head)

    def _prev(self, node):
        """Helps __reversed__() recursively iterate over symbol table

        :param node: The next node to iterate over
        :type node: _Node
        """

        if node is not None:
            yield from self._prev(node.next)
            yield node.key

    def __contains__(self, key):
        """Checks if lookup key is in symbol table

        :param key: Lookup key
        :type key: str
        :return: True if key exists, otherwise False
        :rtype: bool
        """

        node = self._head
        while node is not None:
            if key == node.key:
                return True
            node = node.next
        return False

    def keys(self):
        """Alias for __iter__()"""

        return iter(self)

    def values(self):
        """Iterates over the symbol table, most recently added to last.
        Generates a sequence of values."""

        node = self._head
        while node is not None:
            yield node.value
            node = node.next

    def items(self):
        """Iterates over the symbol table, most recently added to last.
        Generates a sequence of (key, value) pairs."""

        node = self._head
        while node is not None:
            yield node.key, node.value
            node = node.next


if __name__ == "__main__":

    import unittest


    class TestSequentialSearchST(unittest.TestCase):

        def setUp(self):
            self.st = SequentialSearchST()
            self.st["m"] = "Letter M"
            self.st["c"] = "Letter C"
            self.st["s"] = "Letter S"
            self.st["t"] = "Letter T"
            self.st["b"] = "Letter B"
            self.st["y"] = "Letter Y"

        def test_len(self):
            self.assertEqual(6, len(self.st))
            self.assertEqual(0, len(SequentialSearchST()))

        def test_bool(self):
            self.assertTrue(bool(self.st))
            self.assertFalse(bool(SequentialSearchST()))

        def test_setitem(self):
            self.st["a"] = "Letter A"
            self.assertEqual(7, len(self.st))
            self.assertEqual("Letter A", self.st['a'])

            self.st['s'] = "Character S"
            self.assertEqual(7, len(self.st))
            self.assertEqual("Character S", self.st['s'])

        def test_getitem(self):
            self.assertEqual("Letter S", self.st['s'])
            self.assertEqual("Letter M", self.st['m'])
            self.assertEqual("Letter Y", self.st['y'])
            self.assertEqual("Letter B", self.st['b'])
            self.assertEqual("Letter C", self.st['c'])
            self.assertEqual("Letter T", self.st['t'])
            self.assertRaises(KeyError, self.st.__getitem__, 'a')

            self.assertRaises(KeyError, SequentialSearchST().__getitem__, 'a')

        def test_delitem(self):
            del self.st['s']
            self.assertEqual(5, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 's')

            del self.st['m']
            self.assertEqual(4, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 'm')

            del self.st['y']
            self.assertEqual(3, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 'y')

            del self.st['b']
            self.assertEqual(2, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 'b')

            del self.st['c']
            self.assertEqual(1, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 'c')

            del self.st['t']
            self.assertEqual(0, len(self.st))
            self.assertRaises(KeyError, self.st.__getitem__, 't')

        def test_iter(self):
            keys = ['y', 'b', 't', 's', 'c', 'm']
            self.assertEqual(keys, list(self.st))
            self.assertEqual(keys, [x for x in self.st])
            self.assertEqual(keys, [*self.st])

        def test_reversed(self):
            rkeys = ['m', 'c', 's', 't', 'b', 'y']
            self.assertEqual(rkeys, list(reversed(self.st)))
            self.assertEqual(rkeys, [x for x in reversed(self.st)])
            self.assertEqual(rkeys, [*reversed(self.st)])
        
        def test_contains(self):
            self.assertTrue('m' in self.st)

        def test_keys(self):
            keys = ['y', 'b', 't', 's', 'c', 'm']
            self.assertEqual(keys, list(self.st.keys()))
            self.assertEqual(keys, [x for x in self.st.keys()])
            self.assertEqual(keys, [*self.st.keys()])
        
        def test_values(self):
            values = ['Letter Y', 'Letter B', 'Letter T', 'Letter S',
                      'Letter C', 'Letter M']
            self.assertEqual(values, list(self.st.values()))
            self.assertEqual(values, [x for x in self.st.values()])
            self.assertEqual(values, [*self.st.values()])

        def test_items(self):
            items = [
                ('y', 'Letter Y'),
                ('b', 'Letter B'),
                ('t', 'Letter T'),
                ('s', 'Letter S'),
                ('c', 'Letter C'),
                ('m', 'Letter M')
            ]
            self.assertEqual(items, list(self.st.items()))
            self.assertEqual(items, [x for x in self.st.items()])
            self.assertEqual(items, [*self.st.items()])


    unittest.main()
