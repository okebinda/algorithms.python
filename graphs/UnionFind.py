"""Graphs: Union-Find"""


class UnionFind:
    """Finds pairs of connected components, such as for simple graphs."""

    def __init__(self, n):
        """UnionFind constructor.

        :param n: Number of initial components
        :typen: int
        """

        self._count = n
        self._id = list(range(n))

    def __len__(self):
        """Reports the number of connected components.

        :return: The number of connected components
        :rtype: int
        """

        return self._count

    def connected(self, p, q):
        """Reports if the two components are connected.

        :return: True if components are connected, False otherwise
        :rtype: bool
        """

        return self.find(p) == self.find(q)

    def find(self, p):
        """Reports the ID of the connected component the component belongs to.

        :param p: A component ID
        :type p: int
        :return: The ID of the connected component for the component
        :rtype: int
        """

        return self._id[p]

    def union(self, p, q):
        """Connects two components together.

        :param p: The first component
        :type p: int
        :param q: The first component
        :type q: int
        """

        p_id = self.find(p)
        q_id = self.find(q)

        if p_id == q_id:
            return

        for i in range(len(self._id)):
            if self._id[i] == p_id:
                self._id[i] = q_id

        self._count -= 1


if __name__ == "__main__":

    import unittest


    class TestUnionFind(unittest.TestCase):

        def setUp(self):
            components = [(4, 3), (3, 8), (6, 5), (9, 4), (2, 1), (8, 9),
                          (5, 0), (7, 2), (6, 1), (1, 0), (6, 7)]
            self.uf = UnionFind(10)
            for pair in components:
                self.uf.union(*pair)

        def test_count(self):
            self.assertEqual(2, len(self.uf))

        def test_connected(self):
            self.assertTrue(self.uf.connected(0, 1))
            self.assertTrue(self.uf.connected(7, 5))
            self.assertTrue(self.uf.connected(3, 9))
            self.assertFalse(self.uf.connected(2, 8))
            self.assertFalse(self.uf.connected(1, 9))

        def test_union(self):
            self.uf.union(7, 8)
            self.assertEqual(1, len(self.uf))
            self.assertTrue(self.uf.connected(1, 9))


    unittest.main()
