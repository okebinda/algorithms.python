"""Tree: Binary Search Tree"""


class BinarySearchTree:
    """A symbol table with key:value pairs implemented as a binary tree."""

    class _Node:
        """A data node in the tree"""

        __slots__ = 'key', 'value', 'n', 'left', 'right'

        def __init__(self, key, value, n):
            """Node constructor

            :param key: Lookup key
            :type key: str
            :param value: Any data value
            :param n: Initial length of subtree
            :type n: int
            """

            self.key = key
            self.value = value
            self.n = n
            self.left = None
            self.right = None

    def __init__(self):
        """BinarySearchTree constructor"""

        self._root = None

    def __len__(self):
        """Reports number of elements in the entire tree

        :return: Length of tree
        :rtype: int
        """

        return self._len(self._root)

    def _len(self, node):
        """Reports number of elements in the subtree

        :param node: The node at the root of the subtree
        :type node: _Node
        :return: Length of subtree
        :rtype: int
        """

        return 0 if node is None else node.n

    def __bool__(self):
        """Reports if tree contains any elements

        :return: False if empty, True otherwise
        :rtype: bool
        """

        return False if self._root is None else True

    def __setitem__(self, key, value):
        """Sets the element with given key to given value, adds element if
        does not exist

        :param key: Lookup key
        :type key: str
        :param value: Any data value
        """

        self._root = self._setitem(key, value, self._root)

    def _setitem(self, key, value, node):
        """Sets the element with given key to given value for a subtree, adds
        element if does not exist

        :param key: Lookup key
        :type key: str
        :param value: Any data value
        :param node: The node at the root of the subtree
        :type node: _Node
        :return: The node at the root of the subtree
        :rtype: _Node
        """

        if node is None:
            return self._Node(key, value, 1)
        if key < node.key:
            node.left = self._setitem(key, value, node.left)
        elif key > node.key:
            node.right = self._setitem(key, value, node.right)
        else:
            node.value = value
        node.n = self._len(node.left) + self._len(node.right) + 1
        return node

    def __getitem__(self, key):
        """Retrieves the value of the element with a given key if it exists

        :param key: Lookup key
        :type key: str
        :return: Value of element found at the lookup key
        :raises: KeyError
        """

        return self._getitem(key, self._root)

    def _getitem(self, key, node):
        """Retrieves the value of the element with a given key if it exists for
        a subtree

        :param key: Lookup key
        :type key: str
        :param node: The node at the root of the subtree
        :type node: _Node
        :return: Value of element found at the lookup key
        :raises: KeyError
        """

        if node is None:
            raise KeyError("Key `{}` not found.".format(key))
        if key < node.key:
            return self._getitem(key, node.left)
        elif key > node.key:
            return self._getitem(key, node.right)
        else:
            return node.value

    def __delitem__(self, key):
        """Removes the element with the given key if it exists

        :param key: Lookup key
        :type key: str
        :raises: KeyError
        """

        self._root = self._delitem(key, self._root)

    def _delitem(self, key, node):
        """Removes the element with the given key if it exists for a subtree

        :param key: Lookup key
        :type key: str
        :param node: The node at the root of the subtree
        :type node: _Node
        :raises: KeyError
        """

        if node is None:
            raise KeyError("Key `{}` not found.".format(key))
        if key < node.key:
            node.left = self._delitem(key, node.left)
        elif key > node.key:
            node.right = self._delitem(key, node.right)
        else:
            if node.right is None:
                return node.left
            if node.left is None:
                return node.right
            t = node
            node = self._min(node.right)
            node.right = self._delete_min(t.right)
            node.left = t.left
        node.n = self._len(node.left) + self._len(node.right) + 1
        return node

    def min(self):
        """Finds the key with the lowest rank

        :return: The lookup key with the lowest rank
        :rtype: str
        :raises: Exception
        """

        if not bool(self):
            raise Exception("BinarySearchTree is empty.")
        return self._min(self._root).key

    def _min(self, node):
        """Finds the key with the lowest rank for a subtree

        :param node: The node at the root of the subtree
        :type node: _Node
        :return: The node with the lookup key with the lowest rank
        :rtype: _Node
        """

        return node if node.left is None else self._min(node.left)

    def max(self):
        """Finds the key with the highest rank

        :return: The lookup key with the highest rank
        :rtype: str
        :raises: Exception
        """

        if self._root is None:
            raise Exception("BinarySearchTree is empty.")
        return self._max(self._root).key

    def _max(self, node):
        """Finds the key with the highest rank for a subtree

        :param node: The node at the root of the subtree
        :type node: _Node
        :return: The lookup key with the highest rank
        :rtype: str
        :raises: Exception
        """

        return node if node.right is None else self._max(node.right)

    def delete_min(self):
        """Removes the element with the key with the lowest rank

        :raises: Exception
        """

        if self._root is None:
            raise Exception("BinarySearchTree is empty.")
        self._root = self._delete_min(self._root)

    def _delete_min(self, node):
        """Removes the element with the key with the lowest rank for a subtree

        :param node: The node at the root of the subtree
        :type node: _Node
        :raises: Exception
        """

        if node.left is None:
            return node.right
        node.left = self._delete_min(node.left)
        node.n = self._len(node.left) + self._len(node.right) + 1
        return node

    def floor(self, key):
        """Finds the highest ranking key that is not higher than the given key

        :param key: Value to compare keys against
        :type key: str
        :return: The highest ranking key that is not higher than the given key
        :rtype: str
        :raises: Exception
        """

        node = self._floor(key, self._root)
        if node is None:
            raise Exception("Illegal argument.")
        return node.key

    def _floor(self, key, node):
        """Finds the node with the highest ranking key that is not higher than
        the given key for a subtree

        :param key: Value to compare keys against
        :type key: str
        :param node: The node at the root of the subtree
        :type node: _Node
        :return: The node with the highest ranking key that is not higher than
                 the given key
        :rtype: _Node
        """

        if node is None:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self._floor(key, node.left)
        t = self._floor(key, node.right)
        return node if t is None else t

    def ceiling(self, key):
        """Finds the lowest ranking key that is not lower than the given key

        :param key: Value to compare keys against
        :type key: str
        :return: The lowest ranking key that is not lower than the given key
        :rtype: str
        :raises: Exception
        """

        node = self._ceiling(key, self._root)
        if node is None:
            raise Exception("Illegal argument.")
        return node.key

    def _ceiling(self, key, node):
        """Finds the node with the lowest ranking key that is not lower than
        the given key for a subtree

        :param key: Value to compare keys against
        :type key: str
        :param node: The node at the root of the subtree
        :type node: _Node
        :return: The node with the lowest ranking key that is not lower than
                 the given key
        :rtype: _Node
        """

        if node is None:
            return None
        if key == node.key:
            return node
        if key > node.key:
            return self._ceiling(key, node.right)
        t = self._ceiling(key, node.left)
        return node if t is None else t

    def select(self, k):
        """Finds the key at the given index

        :param k: Zero-based index for key's position
        :type k: int
        :return: Lookup key at index
        :rtype: str
        :raises: IndexError
        """

        if k < 0 or k >= len(self):
            raise IndexError("Index `{}` out of bounds.".format(k))
        return self._select(k, self._root).key

    def _select(self, k, node):
        """Finds the node at the given index for a subtree

        :param k: Zero-based index for key's position
        :type k: int
        :param node: The node at the root of the subtree
        :type node: _Node
        :return: The node at the index
        :rtype: _Node
        """

        if node is None:
            return None
        t = self._len(node.left)
        if t > k:
            return self._select(k, node.left)
        elif t < k:
            return self._select(k-t-1, node.right)
        else:
            return node

    def rank(self, key):
        """Determines the zero-indexed position of the given key if it exists

        :param key: Lookup key
        :type key: str
        :return: The zero-indexed position (rank) of the key
        :rtype: int
        :raises: KeyError
        """

        r = self._rank(key, self._root)
        if r is None:
            raise KeyError("Key `{}` not found.".format(key))
        return r

    def _rank(self, key, node):
        """Determines the zero-indexed position of the given key if it exists
        for a subtree

        :param key: Lookup key
        :type key: str
        :param node: The node at the root of the subtree
        :type node: _Node
        :return: The zero-indexed position (rank) of the key
        :rtype: int
        """

        if node is None:
            return None
        if key < node.key:
            return self._rank(key, node.left)
        elif key > node.key:
            return 1 + self._len(node.left) + self._rank(key, node.right)
        else:
            return self._len(node.left)

    def __iter__(self):
        """Iterates over the tree in order. Generates a sequence of keys"""

        return self._iter(self._root)

    def _iter(self, node):
        """Iterates over a subtree in order. Generates a sequence of keys

        :param node: The node at the root of the subtree
        :type node: _Node
        """

        if node is not None:
            for l_child in self._iter(node.left):
                yield l_child
            yield node.key
            for r_child in self._iter(node.right):
                yield r_child

    def __reversed__(self):
        """Iterates over the tree in reverse order. Generates a sequence of
        keys"""

        return self._reversed(self._root)

    def _reversed(self, node):
        """Iterates over a subtree in reverse order. Generates a sequence of
        keys

        :param node: The node at the root of the subtree
        :type node: _Node
        """

        if node is not None:
            for r_child in self._reversed(node.right):
                yield r_child
            yield node.key
            for l_child in self._reversed(node.left):
                yield l_child

    def __contains__(self, key):
        """Checks if lookup key is in the tree

        :param key: Lookup key
        :type key: str
        :return: True if key exists, otherwise False
        :rtype: bool
        """

        try:
            self[key]
            return True
        except KeyError:
            return False

    def keys(self):
        """Iterates over the tree in order. Generates a sequence of keys"""

        return iter(self)

    def values(self):
        """Iterates over the tree in order. Generates a sequence of values"""

        return self._values(self._root)

    def _values(self, node):
        """Iterates over a subtree in order. Generates a sequence of values

        :param node: The node at the root of the subtree
        :type node: _Node
        """

        if node is not None:
            for l_child in self._values(node.left):
                yield l_child
            yield node.value
            for r_child in self._values(node.right):
                yield r_child

    def items(self):
        """Iterates over the tree in order. Generates a sequence of
        (key, value) pairs"""

        return self._items(self._root)

    def _items(self, node):
        """Iterates over a subtree in order. Generates a sequence of
        (key, value) pairs

        :param node: The node at the root of the subtree
        :type node: _Node
        """

        if node is not None:
            for l_child in self._items(node.left):
                yield l_child
            yield node.key, node.value
            for r_child in self._items(node.right):
                yield r_child


if __name__ == "__main__":

    import unittest


    class TestBinarySearchTree(unittest.TestCase):

        def setUp(self):
            self.tree = BinarySearchTree()
            self.tree['m'] = "Letter M"
            self.tree['c'] = "Letter C"
            self.tree['s'] = "Letter S"
            self.tree['t'] = "Letter T"
            self.tree['b'] = "Letter B"
            self.tree['y'] = "Letter Y"

        def test_len(self):
            self.assertEqual(6, len(self.tree))
            self.assertEqual(0, len(BinarySearchTree()))

        def test_bool(self):
            self.assertTrue(bool(self.tree))
            self.assertFalse(bool(BinarySearchTree()))

        def test_setitem(self):
            self.tree['a'] = "Letter A"
            self.assertEqual(7, len(self.tree))

        def test_getitem(self):
            self.assertEqual("Letter M", self.tree['m'])
            self.assertEqual("Letter C", self.tree['c'])
            self.assertEqual("Letter S", self.tree['s'])
            self.assertEqual("Letter T", self.tree['t'])
            self.assertEqual("Letter B", self.tree['b'])
            self.assertEqual("Letter Y", self.tree['y'])
            self.assertRaises(KeyError, self.tree.__getitem__, 'a')
            self.assertRaises(KeyError, BinarySearchTree().__getitem__, 'a')

        def test_delitem(self):
            del self.tree['m']
            self.assertEqual(5, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 'm')

            del self.tree['c']
            self.assertEqual(4, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 'c')

            del self.tree['s']
            self.assertEqual(3, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 's')

            del self.tree['t']
            self.assertEqual(2, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 't')

            del self.tree['y']
            self.assertEqual(1, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 'y')

            del self.tree['b']
            self.assertEqual(0, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 'b')

            self.assertRaises(KeyError, self.tree.__delitem__, 'a')
            self.assertRaises(KeyError, BinarySearchTree().__delitem__, 'a')

        def test_min(self):
            self.assertEqual('b', self.tree.min())
            self.assertRaises(Exception, BinarySearchTree().min)

        def test_max(self):
            self.assertEqual('y', self.tree.max())
            self.assertRaises(Exception, BinarySearchTree().max)

        def test_delete_min(self):
            self.tree.delete_min()
            self.assertEqual(5, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 'b')

            self.tree.delete_min()
            self.assertEqual(4, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 'c')

            self.tree.delete_min()
            self.assertEqual(3, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 'm')

            self.tree.delete_min()
            self.assertEqual(2, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 's')

            self.tree.delete_min()
            self.assertEqual(1, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 't')

            self.tree.delete_min()
            self.assertEqual(0, len(self.tree))
            self.assertRaises(KeyError, self.tree.__getitem__, 'y')

            self.assertRaises(Exception, self.tree.delete_min)
            self.assertRaises(Exception, BinarySearchTree().delete_min)

        def test_floor(self):
            self.assertEqual('b', self.tree.floor('b'))
            self.assertEqual('c', self.tree.floor('c'))
            self.assertEqual('c', self.tree.floor('d'))
            self.assertEqual('m', self.tree.floor('m'))
            self.assertEqual('m', self.tree.floor('n'))
            self.assertRaises(Exception, self.tree.floor, 'a')
            self.assertRaises(Exception, BinarySearchTree().floor, 'z')

        def test_ceiling(self):
            self.assertEqual('y', self.tree.ceiling('y'))
            self.assertEqual('y', self.tree.ceiling('x'))
            self.assertEqual('t', self.tree.ceiling('t'))
            self.assertEqual('s', self.tree.ceiling('s'))
            self.assertEqual('s', self.tree.ceiling('r'))
            self.assertRaises(Exception, self.tree.ceiling, 'z')
            self.assertRaises(Exception, BinarySearchTree().ceiling, 'a')

        def test_select(self):
            self.assertEqual('b', self.tree.select(0))
            self.assertEqual('c', self.tree.select(1))
            self.assertEqual('m', self.tree.select(2))
            self.assertEqual('s', self.tree.select(3))
            self.assertEqual('t', self.tree.select(4))
            self.assertEqual('y', self.tree.select(5))
            self.assertRaises(IndexError, self.tree.select, 6)
            self.assertRaises(IndexError, BinarySearchTree().select, 0)

        def test_rank(self):
            self.assertEqual(0, self.tree.rank('b'))
            self.assertEqual(1, self.tree.rank('c'))
            self.assertEqual(2, self.tree.rank('m'))
            self.assertEqual(3, self.tree.rank('s'))
            self.assertEqual(4, self.tree.rank('t'))
            self.assertEqual(5, self.tree.rank('y'))
            self.assertRaises(KeyError, self.tree.rank, 'a')
            self.assertRaises(KeyError, BinarySearchTree().rank, 'a')

        def test_iter(self):
            keys = ['b', 'c', 'm', 's', 't', 'y']
            self.assertEqual(keys, list(self.tree))
            self.assertEqual(keys, [x for x in self.tree])
            self.assertEqual(keys, [*self.tree])
            self.assertEqual([], list(BinarySearchTree()))

        def test_reversed(self):
            rkeys = ['y', 't', 's', 'm', 'c', 'b']
            self.assertEqual(rkeys, list(reversed(self.tree)))
            self.assertEqual(rkeys, [x for x in reversed(self.tree)])
            self.assertEqual(rkeys, [*reversed(self.tree)])
            self.assertEqual([], list(reversed(BinarySearchTree())))

        def test_contains(self):
            self.assertTrue('m' in self.tree)
            self.assertTrue('c' in self.tree)
            self.assertTrue('s' in self.tree)
            self.assertTrue('t' in self.tree)
            self.assertTrue('b' in self.tree)
            self.assertTrue('y' in self.tree)
            self.assertFalse('a' in self.tree)
            self.assertFalse('a' in BinarySearchTree())

        def test_keys(self):
            keys = ['b', 'c', 'm', 's', 't', 'y']
            self.assertEqual(keys, list(self.tree.keys()))
            self.assertEqual(keys, [x for x in self.tree.keys()])
            self.assertEqual(keys, [*self.tree.keys()])
            self.assertEqual([], list(BinarySearchTree().keys()))

        def test_values(self):
            values = ["Letter B", "Letter C", "Letter M", "Letter S",
                      "Letter T", "Letter Y"]
            self.assertEqual(values, list(self.tree.values()))
            self.assertEqual(values, [x for x in self.tree.values()])
            self.assertEqual(values, [*self.tree.values()])
            self.assertEqual([], list(BinarySearchTree().values()))

        def test_items(self):
            items = [
                ('b', "Letter B"),
                ('c', "Letter C"),
                ('m', "Letter M"),
                ('s', "Letter S"),
                ('t', "Letter T"),
                ('y', "Letter Y")
            ]
            self.assertEqual(items, list(self.tree.items()))
            self.assertEqual(items, [x for x in self.tree.items()])
            self.assertEqual(items, [*self.tree.items()])
            self.assertEqual([], list(BinarySearchTree().items()))


    unittest.main()
