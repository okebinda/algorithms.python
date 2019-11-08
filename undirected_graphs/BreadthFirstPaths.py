"""Undirected Graph: Breadth-First Paths"""


class BreadthFirstPaths:
    """A Graph client that uses breadth-first search to find paths to all
        vertices connected to an initial vertex."""

    def __init__(self, G, s):
        """BreadthFirstPaths constructor.

        :param G: The complete graph to search
        :type G: Graph
        :param s: The starting vertex for all path searches
        :type s: int
        """

        self._marked = [False] * G.V()
        self._edge_to = [None] * G.V()
        self._s = s
        self._bfs(G, s)

    def _bfs(self, G, v):
        """Finds all paths on the graph from the initial vertex using
        breadth-first search.

        :param G: The complete graph to search
        :type G: Graph
        :param v: The vertex to start searching from
        :type v: int
        """

        stack = []
        self._marked[v] = True
        stack.append(v)
        while len(stack) > 0:
            v = stack.pop()
            for w in G.adj(v):
                if self._marked[w] is False:
                    self._edge_to[w] = v
                    self._marked[w] = True
                    stack.append(w)

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

    from .Graph import Graph


    class TestBreadthFirstPaths(unittest.TestCase):

        graph = None

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyG.txt')
            self.graph = Graph(filename=data_file)

        def test_has_path_to(self):
            bfp0 = BreadthFirstPaths(self.graph, 0)
            for x in [0, 1, 2, 3, 4, 5, 6]:
                self.assertTrue(bfp0.has_path_to(x))
            for x in [7, 8, 9, 10, 11, 12]:
                self.assertFalse(bfp0.has_path_to(x))

            bfp7 = BreadthFirstPaths(self.graph, 7)
            for x in [7, 8]:
                self.assertTrue(bfp7.has_path_to(x))
            for x in [1, 2, 3, 4, 5, 6, 9, 10, 11, 12]:
                self.assertFalse(bfp7.has_path_to(x))

        def test_path_to(self):
            bfp0 = BreadthFirstPaths(self.graph, 0)
            self.assertEqual((0, 6, 4), bfp0.path_to(4))
            self.assertIsNone(bfp0.path_to(8))

            bfp12 = BreadthFirstPaths(self.graph, 12)
            self.assertEqual((12, 9, 10), bfp12.path_to(10))


    unittest.main()
