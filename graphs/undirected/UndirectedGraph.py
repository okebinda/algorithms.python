"""Undirected Graph: UndirectedGraph"""

from collections import defaultdict

from graphs.Graph import Graph


class UndirectedGraph(Graph):
    """A simple undirected graph. Contains zero-indexed vertices and edges as
    adjacency lists for each vertex."""

    def __init__(self, *, filename=None, edges=None):
        """UndirectedGraph constructor.

        :param filename: File with graph edges to load
        :type filename: str
        :param edges: A sequence of edges (as tuples) to initialize
        :type edges: iterable
        """

        self._size = 0
        self._vertices = set()
        self._adj = defaultdict(list)
        self._read_file(filename)
        self._load_edges(edges)

    def _read_file(self, filename):
        """Initializes edges of a graph based on an input file.

        :param filename: File with graph edges to load
        :type filename: str
        """

        if filename is not None:
            with open(filename, 'rt') as fp:
                for line in fp:
                    self.add_edge(*tuple(map(lambda x: int(x),
                                             line.rstrip().split(' '))))

    def _load_edges(self, edges):
        """Initializes edges of a graph based on a sequence of edge tuples.

        :param edges: Sequence of edge tuples to load
        :type edges: iterable
        """

        if edges is not None:
            for edge in edges:
                self.add_edge(*edge)

    def size(self):
        """Reports the number of edges in the graph.

        :return: Number of edges in the graph
        :rtype: int
        """

        return self._size

    def __len__(self):
        """Reports the number of edges in the graph. Alias for self.size().

        :return: Number of edges in the graph
        :rtype: int
        """

        return self.size()

    def order(self):
        """Reports the number of vertices in the graph.

        :return: Number of vertices in the graph
        :rtype: int
        """

        return len(self._vertices)

    def __contains__(self, edge):
        """Determines if an edge exists in the graph.

        :param edge: An edge represented as a tuple (v, w) to test for
        :type edge: tuple
        :return: True if edges exists, other wise False
        :rtype: bool
        """

        v, w = edge
        return self._adj[v] and w in self._adj[v]

    def add_edge(self, v, w):
        """Creates an edge between two vertices.

        :param v: Vertex 1
        :type v: int
        :param w: Vertex 2
        :type w: int 
        """

        if not (v, w) in self:
            self._vertices |= {v, w}
            self._adj[v].append(w)
            self._adj[w].append(v)
            self._size += 1

    def adj(self, v):
        """Retrieves the adjacency list for a vertex.

        :param v: Vertex
        :type v: int
        :return: The adjacency list of vertex v
        :rtype: list
        """

        return self._adj[v]

    def __iter__(self):
        """Generates a sequence of graph edges in no particular order.

        :return: A sequence of graph edges
        :rtype: generator
        """

        completed = set()
        for v in self._vertices:
            for w in self._adj[v]:
                if (w, v) not in completed:
                    yield v, w
                    completed.add((v, w))

    def __str__(self):
        """Generates a human readable representation of the graph.

        :return: Vertex and edge count and adjacency list per vertex
        :rtype: str
        """

        out = []
        for v in sorted(self._vertices):
            out.append("{}: {}".format(v, ', '.join(list(map(lambda x: str(x),
                                                            self._adj[v])))))
        return "\n".join(out)


if __name__ == "__main__":

    import unittest
    from os import path


    class TestGraph(unittest.TestCase):

        edges2 = ((0, 5), (4, 3), (0, 1), (6, 4), (5, 4), (0, 2), (0, 6),
                  (5, 3))

        def setUp(self):
            data_path = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyG.txt')
            self.graph1 = UndirectedGraph(filename=data_path)
            self.graph2 = UndirectedGraph(edges=self.edges2)

        def test_size(self):
            self.assertEqual(13, self.graph1.size())
            self.assertEqual(8, self.graph2.size())
            self.assertEqual(0, UndirectedGraph().size())

        def test_len(self):
            self.assertEqual(13, len(self.graph1))
            self.assertEqual(8, len(self.graph2))
            self.assertEqual(0, len(UndirectedGraph()))

        def test_order(self):
            self.assertEqual(13, self.graph1.order())
            self.assertEqual(7, self.graph2.order())
            self.assertEqual(0, UndirectedGraph().order())

        def test_contains(self):
            self.assertTrue((11, 12) in self.graph1)
            self.assertTrue((12, 11) in self.graph1)
            self.assertFalse((12, 8) in self.graph1)
            self.assertTrue((0, 1) in self.graph2)
            self.assertFalse((6, 5) in self.graph2)
            self.assertFalse((1, 2) in UndirectedGraph())

        def test_add_edge(self):
            self.graph1.add_edge(9, 7)
            self.assertEqual(14, self.graph1.size())
            self.assertEqual([7, 10, 11, 12], sorted(self.graph1.adj(9)))
            self.assertEqual([8, 9], sorted(self.graph1.adj(7)))

            self.graph2.add_edge(2, 3)
            self.graph2.add_edge(2, 4)
            self.assertEqual(10, self.graph2.size())
            self.assertEqual([0, 3, 4], sorted(self.graph2.adj(2)))
            self.assertEqual([2, 4, 5], sorted(self.graph2.adj(3)))
            self.assertEqual([2, 3, 5, 6], sorted(self.graph2.adj(4)))

            # an edge that already exists shouldn't change anything
            self.graph2.add_edge(4, 3)
            self.assertEqual(10, self.graph2.size())
            self.assertEqual([2, 4, 5], sorted(self.graph2.adj(3)))
            self.assertEqual([2, 3, 5, 6], sorted(self.graph2.adj(4)))

        def test_adj(self):
            self.assertEqual([5, 1, 2, 6], self.graph1.adj(0))
            self.assertEqual([0], self.graph1.adj(1))
            self.assertEqual([0], self.graph1.adj(2))
            self.assertEqual([4, 5], self.graph1.adj(3))
            self.assertEqual([3, 6, 5], self.graph1.adj(4))
            self.assertEqual([0, 4, 3], self.graph1.adj(5))
            self.assertEqual([4, 0], self.graph1.adj(6))
            self.assertEqual([8], self.graph1.adj(7))
            self.assertEqual([7], self.graph1.adj(8))
            self.assertEqual([12, 10, 11], self.graph1.adj(9))
            self.assertEqual([9], self.graph1.adj(10))
            self.assertEqual([12, 9], self.graph1.adj(11))
            self.assertEqual([9, 11], self.graph1.adj(12))

        def test_iter(self):
            for edge in self.graph2:
                v, w = edge
                self.assertTrue((v, w) in self.edges2 or (w, v) in self.edges2)

        def test_str(self):
            graph1_out = [
                "0: 5, 1, 2, 6",
                "1: 0",
                "2: 0",
                "3: 4, 5",
                "4: 3, 6, 5",
                "5: 0, 4, 3",
                "6: 4, 0",
                "7: 8",
                "8: 7",
                "9: 12, 10, 11",
                "10: 9",
                "11: 12, 9",
                "12: 9, 11"
            ]
            self.assertEqual("\n".join(graph1_out), str(self.graph1))


    unittest.main()
