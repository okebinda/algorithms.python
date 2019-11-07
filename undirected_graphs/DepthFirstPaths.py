"""Undirected Graph: Depth First Paths"""

from .Graph import Graph


class DepthFirstPaths:
    """A Graph client that uses depth-first search to find paths to all
    vertices connected to an initial vertex."""

    def __init__(self, G, s):
        """DepthFirstPaths constructor.

        :param G: The complete graph to search
        :type G: Graph
        :param s: The starting vertex for all path searches
        :type s: int
        """

        self._marked = [False] * G.V()
        self._edge_to = [None] * G.V()
        self._s = s
        self._dfs(G, s)

    def _dfs(self, G, v):
        """Finds all paths on the graph from the initial vertex using
        depth-first search.

        :param G: The complete graph to search
        :type G: Graph
        :param v: The vertex to start searching from
        :type v: int
        """

        self._marked[v] = True
        for w in G.adj(v):
            if self._marked[w] is False:
                self._edge_to[w] = v
                self._dfs(G, w)

    def has_path_to(self, v):
        """Determines if a path between the given vertex and the initial one
        exists.

        :param v: The vertex to search for a path to
        :type v: int
        :return: True if path exists, False otherwise
        :rtype: bool
        """

        return self._marked[v]

    def path_to(self, v):
        """Reports a path between the given vertex and the initial one.

        :param v: The vertex to find a path to
        :type v: int
        :return: A sequence of vertices forming the path or None
        :rtype: tuple | None
        """

        if self.has_path_to(v) is False:
            return None
        v_path = []
        x = v
        while x is not self._s:
            v_path.append(x)
            x = self._edge_to[x]
        v_path.append(self._s)
        return tuple(reversed(v_path))


if __name__ == "__main__":

    import unittest
    from os import path


    class TestDepthFirstPaths(unittest.TestCase):

        graph = None

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyG.txt')
            self.graph = Graph(filename=data_file)

        def test_has_path_to(self):
            dfp0 = DepthFirstPaths(self.graph, 0)
            for x in [0, 1, 2, 3, 4, 5, 6]:
                self.assertTrue(dfp0.has_path_to(x))
            for x in [7, 8, 9, 10, 11, 12]:
                self.assertFalse(dfp0.has_path_to(x))

            dfp7 = DepthFirstPaths(self.graph, 7)
            for x in [7, 8]:
                self.assertTrue(dfp7.has_path_to(x))
            for x in [1, 2, 3, 4, 5, 6, 9, 10, 11, 12]:
                self.assertFalse(dfp7.has_path_to(x))

        def test_path_to(self):
            dfp0 = DepthFirstPaths(self.graph, 0)
            self.assertEqual((0, 5, 4), dfp0.path_to(4))
            self.assertIsNone(dfp0.path_to(8))

            dfp12 = DepthFirstPaths(self.graph, 12)
            self.assertEqual((12, 9, 10), dfp12.path_to(10))


    unittest.main()
