"""Undirected Graph: Connected Components"""


class ConnectedComponents:
    """A graph client that uses depth-first search to find groups of nodes that
    are adjacent - connected components."""

    def __init__(self, G):
        """ConnectedComponents constructor.

        :param G: The complete graph to analyze
        :type G: Graph
        """

        self._marked = [False] * G.order()
        self._id = [None] * G.order()
        self._count = 0
        for s in range(G.order()):
            if self._marked[s] is False:
                self._dfs(G, s)
                self._count += 1

    def _dfs(self, G, v):
        """Finds all vertices on the graph that are connected to the initial
        vertex using depth-first search.

        :param G: The complete graph to search
        :type G: Graph
        :param v: The vertex to start searching from
        :type v: int
        """

        self._marked[v] = True
        self._id[v] = self._count
        for w in G.adj(v):
            if self._marked[w] is False:
                self._dfs(G, w)

    def connected(self, v, w):
        """Determines if two vertices are connected.

        :param v: The first vertex to check for a connection
        :type v: int
        :param w: The second vertex to check for a connection
        :type w: int
        :return: True if vertices are connected, False otherwise
        :rtype: bool
        """

        return self._id[v] == self._id[w]

    def id(self, v):
        """Reports the internal ID used for the entire connected component that
        a vertex belongs to.

        :param v: A vertex that is a member of a connected component
        :type v: int
        :return: The internal ID of the connected component
        :rtype: int
        """

        return self._id[v]

    def count(self):
        """Reports the total number of connected components in the graph.

        :return: The count of connected components in the graph
        :rtype: int
        """

        return self._count


if __name__ == "__main__":

    import unittest
    from os import path

    from .UndirectedGraph import UndirectedGraph


    class TestConnectedComponents(unittest.TestCase):

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyG.txt')
            self.graph = UndirectedGraph(filename=data_file)

        def test_connected(self):
            cc = ConnectedComponents(self.graph)
            self.assertTrue(cc.connected(0, 4))
            self.assertFalse(cc.connected(0, 10))

        def test_id(self):
            cc = ConnectedComponents(self.graph)
            self.assertEqual(0, cc.id(0))
            self.assertEqual(0, cc.id(4))
            self.assertEqual(1, cc.id(7))
            self.assertEqual(2, cc.id(10))

        def test_count(self):
            cc = ConnectedComponents(self.graph)
            self.assertEqual(3, cc.count())

        def test_client(self):
            cc = ConnectedComponents(self.graph)
            components = [[] for _ in range(cc.count())]
            for v in range(self.graph.order()):
                components[cc.id(v)].append(v)
            self.assertEqual([
                [0, 1, 2, 3, 4, 5, 6],
                [7, 8],
                [9, 10, 11, 12]
            ], components)


    unittest.main()
