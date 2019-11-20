"""Directed Graph: Digraph"""

from collections import defaultdict


class Digraph:
    """A simple directed graph. Contains zero-indexed vertices and edges as
    adjacency lists for each vertex."""

    def __init__(self, *, filename=None, edges=None):
        """Digraph constructor.

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

    def order(self):
        """Reports the number of vertices in the graph.

        :return: Number of vertices in the graph
        :rtype: int
        """

        return max(self._vertices) + 1 if self._vertices else 0

    def size(self):
        """Reports the number of edges in the graph.

        :return: Number of edges in the graph
        :rtype: int
        """

        return self._size

    def add_edge(self, v, w):
        """Creates an edge from vertex v to vertex w.

        :param v: Vertex 1
        :type v: int
        :param w: Vertex 2
        :type w: int
        """

        self._vertices |= {v, w}
        self._adj[v].append(w)
        self._size += 1

    def adj(self, v):
        """Retrieves the adjacency list for a vertex.

        :param v: Vertex
        :type v: int
        :return: The adjacency list of vertex v
        :rtype: list
        """

        return self._adj[v]

    def reverse(self):
        """Generates a new Digraph based on the current one, but with all the
        edges reversed.

        :returns: A copy of this graph with the edges reversed
        :rtype: Digraph
        """

        R = Digraph()
        for v in range(self.order()):
            for w in self.adj(v):
                R.add_edge(w, v)
        return R

    def __str__(self):
        """Generates a human readable representation of the graph.

        :return: Adjacency list per vertex
        :rtype: str
        """

        out = []
        for v in range(self.order()):
            out.append(
                "{}: {}".format(v, ' '.join(list(map(lambda x: str(x),
                                                     self._adj[v])))))
        return "\n".join(out)


if __name__ == "__main__":

    import unittest
    from os import path


    class TestDigraph(unittest.TestCase):

        edges2 = ((0, 5),  (0, 1), (0, 6), (2, 0), (2, 3), (3, 5), (5, 4),
                  (6, 4), (6, 9), (7, 6), (8, 7), (9, 11), (9, 12), (9, 10),
                  (11, 12))

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyDG.txt')
            self.graph = Digraph(filename=data_file)
            self.graph2 = Digraph(edges=self.edges2)

        def test_order(self):
            self.assertEqual(13, self.graph.order())
            self.assertEqual(13, self.graph2.order())
            self.assertEqual(0, Digraph().order())

        def test_size(self):
            self.assertEqual(22, self.graph.size())
            self.assertEqual(15, self.graph2.size())
            self.assertEqual(0, Digraph().size())

        def test_adj(self):
            self.assertEqual([1, 5], sorted(self.graph.adj(0)))
            self.assertEqual([], sorted(self.graph.adj(1)))
            self.assertEqual([0, 3], sorted(self.graph.adj(2)))
            self.assertEqual([2, 5], sorted(self.graph.adj(3)))
            self.assertEqual([2, 3], sorted(self.graph.adj(4)))
            self.assertEqual([4], sorted(self.graph.adj(5)))
            self.assertEqual([0, 4, 8, 9], sorted(self.graph.adj(6)))
            self.assertEqual([6, 9], sorted(self.graph.adj(7)))
            self.assertEqual([6], sorted(self.graph.adj(8)))
            self.assertEqual([10, 11], sorted(self.graph.adj(9)))
            self.assertEqual([12], sorted(self.graph.adj(10)))
            self.assertEqual([4, 12], sorted(self.graph.adj(11)))
            self.assertEqual([9], sorted(self.graph.adj(12)))

            self.assertEqual([1, 5, 6], sorted(self.graph2.adj(0)))
            self.assertEqual([], sorted(self.graph2.adj(1)))
            self.assertEqual([0, 3], sorted(self.graph2.adj(2)))
            self.assertEqual([5], sorted(self.graph2.adj(3)))
            self.assertEqual([], sorted(self.graph2.adj(4)))
            self.assertEqual([4], sorted(self.graph2.adj(5)))
            self.assertEqual([4, 9], sorted(self.graph2.adj(6)))
            self.assertEqual([6], sorted(self.graph2.adj(7)))
            self.assertEqual([7], sorted(self.graph2.adj(8)))
            self.assertEqual([10, 11, 12], sorted(self.graph2.adj(9)))
            self.assertEqual([], sorted(self.graph2.adj(10)))
            self.assertEqual([12], sorted(self.graph2.adj(11)))
            self.assertEqual([], sorted(self.graph2.adj(12)))

        def test_add_edge(self):
            self.graph.add_edge(0, 6)
            self.assertEqual([1, 5, 6], sorted(self.graph.adj(0)))
            self.assertEqual([0, 4, 8, 9], sorted(self.graph.adj(6)))
            self.assertEqual(23, self.graph.size())

            self.graph2.add_edge(0, 7)
            self.assertEqual([1, 5, 6, 7], sorted(self.graph2.adj(0)))
            self.assertEqual([6], sorted(self.graph2.adj(7)))
            self.assertEqual(16, self.graph2.size())

            self.graph.add_edge(12, 13)
            self.assertEqual([9, 13], sorted(self.graph.adj(12)))
            self.assertEqual([], sorted(self.graph.adj(13)))
            self.assertEqual(24, self.graph.size())
            self.assertEqual(14, self.graph.order())

        def test_reverse(self):
            R = self.graph.reverse()
            self.assertEqual([2, 6], sorted(R.adj(0)))
            self.assertEqual([0], sorted(R.adj(1)))
            self.assertEqual([3, 4], sorted(R.adj(2)))
            self.assertEqual([2, 4], sorted(R.adj(3)))
            self.assertEqual([5, 6, 11], sorted(R.adj(4)))
            self.assertEqual([0, 3], sorted(R.adj(5)))
            self.assertEqual([7, 8], sorted(R.adj(6)))
            self.assertEqual([], sorted(R.adj(7)))
            self.assertEqual([6], sorted(R.adj(8)))
            self.assertEqual([6, 7, 12], sorted(R.adj(9)))
            self.assertEqual([9], sorted(R.adj(10)))
            self.assertEqual([9], sorted(R.adj(11)))
            self.assertEqual([10, 11], sorted(R.adj(12)))

            R2 = self.graph2.reverse()
            self.assertEqual([2], sorted(R2.adj(0)))
            self.assertEqual([0], sorted(R2.adj(1)))
            self.assertEqual([], sorted(R2.adj(2)))
            self.assertEqual([2], sorted(R2.adj(3)))
            self.assertEqual([5, 6], sorted(R2.adj(4)))
            self.assertEqual([0, 3], sorted(R2.adj(5)))
            self.assertEqual([0, 7], sorted(R2.adj(6)))
            self.assertEqual([8], sorted(R2.adj(7)))
            self.assertEqual([], sorted(R2.adj(8)))
            self.assertEqual([6], sorted(R2.adj(9)))
            self.assertEqual([9], sorted(R2.adj(10)))
            self.assertEqual([9], sorted(R2.adj(11)))
            self.assertEqual([9, 11], sorted(R2.adj(12)))

        def test_str(self):
            graph_out = [
                "0: 1 5",
                "1: ",
                "2: 3 0",
                "3: 2 5",
                "4: 2 3",
                "5: 4",
                "6: 0 8 4 9",
                "7: 9 6",
                "8: 6",
                "9: 10 11",
                "10: 12",
                "11: 12 4",
                "12: 9"
            ]
            self.assertEqual("\n".join(graph_out), self.graph.__str__())

            graph2_out = [
                "0: 5 1 6",
                "1: ",
                "2: 0 3",
                "3: 5",
                "4: ",
                "5: 4",
                "6: 4 9",
                "7: 6",
                "8: 7",
                "9: 11 12 10",
                "10: ",
                "11: 12",
                "12: "
            ]
            self.assertEqual("\n".join(graph2_out), self.graph2.__str__())


    unittest.main()
