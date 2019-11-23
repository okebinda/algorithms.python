"""Directed Graph: Depth-First Search"""


class DirectedDepthFirstSearch:
    """A DirectedGraph client that uses depth-first search to find paths to all
    vertices connected to an initial vertex."""

    def __init__(self, G, s):
        """DirectedDepthFirstSearch constructor.

        :param G: The complete graph to search
        :type G: DirectedGraph
        :param s: The starting vertex or vertices for all path searches
        :type s: int | iterable
        """

        self._marked = [False] * G.order()

        # try to iterate over s first
        try:
            for v in s:
                if self._marked[v] is False:
                    self._dfs(G, v)

        # s is not iterable, try single value
        except TypeError:
            self._dfs(G, s)

    def _dfs(self, G, v):
        """Finds all paths on the graph from the initial vertex using
        depth-first search.

        :param G: The complete graph to search
        :type G: DirectedGraph
        :param v: The vertex to start searching from
        :type v: int
        """

        self._marked[v] = True
        for w in G.adj(v):
            if not self._marked[w]:
                self._dfs(G, w)

    def marked(self, v):
        """Reports if the given vertex is reachable from the starting vertex.

        :param v: The vertex to search for
        :type v: int
        :return: True if the vertex is reachable from the starting vertex
        :rtype: bool
        """

        return self._marked[v]


if __name__ == "__main__":

    import unittest
    from os import path

    from .DirectedGraph import DirectedGraph


    class TestDirectedDepthFirstSearch(unittest.TestCase):

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyDG.txt')
            self.graph = DirectedGraph(filename=data_file)

        def test_marked(self):
            reachable1 = DirectedDepthFirstSearch(self.graph, 1)
            self.assertEqual([1], [v for v in range(self.graph.order())
                                   if reachable1.marked(v)])

            reachable2 = DirectedDepthFirstSearch(self.graph, 2)
            self.assertEqual(
                [0, 1, 2, 3, 4, 5],
                [v for v in range(self.graph.order()) if reachable2.marked(v)])

            reachable3 = DirectedDepthFirstSearch(self.graph, [1, 2, 6])
            self.assertEqual(
                [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12],
                [v for v in range(self.graph.order()) if reachable3.marked(v)])


    unittest.main()
