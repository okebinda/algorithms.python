"""Directed Graph: DirectedGraph

A directed graph (digraph) is a graph (G) that contains a set of vertices (V)
and a set of edges (E), where the first vertex in an edge tuple has a directed
connection to the second vertex but not the other way around.

For example, given the following digraph:

    0 → 1
    ↕ ↙ ↶
    2 → 3

We can describe the graph as follows:

    G = (V, E)
    V = {0, 1, 2, 3}
    E = {(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)}
"""

from collections import defaultdict

from graphs.Graph import Graph


class DirectedGraph(Graph):
    """A simple directed graph. Contains zero-indexed vertices and edges as
    adjacency lists for each vertex."""

    def __init__(self, *, filename=None, vertices=None, edges=None):
        """DirectedGraph constructor.

        :param filename: File with graph edges to load
        :type filename: str
        :param vertices: A sequence of vertices to initialize
        :type vertices: iterable
        :param edges: A sequence of edges (as tuples) to initialize
        :type edges: iterable
        """

        self._size = 0
        self._vertices = set()
        self._adj = defaultdict(list)
        self._read_file(filename)
        self._load_vertices(vertices)
        self._load_edges(edges)

    def _read_file(self, filename):
        """Initializes edges of a graph based on an input file.

        :param filename: File with graph edges to load
        :type filename: str
        """

        if filename is not None:
            with open(filename, 'rt') as fp:
                for i, line in enumerate(fp):
                    if i == 0:
                        self._vertices = set(map(lambda x: int(x),
                                                 line.rstrip().split(' ')))
                    else:
                        self.add_edge(*tuple(map(lambda x: int(x),
                                                 line.rstrip().split(' '))))

    def _load_vertices(self, vertices):
        """Initializes vertices of a graph based on a sequence of integers.

        :param vertices: Sequence of vertex integers to load
        :type vertices: iterable
        """

        if vertices is not None:
            for v in vertices:
                self.add_vertex(v)

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

    def add_vertex(self, v):
        """Adds a vertex to the graph.

        :param v: Vertex to add
        :type v: int
        """

        self._vertices.add(v)

    def add_edge(self, v, w):
        """Creates an edge from vertex v to vertex w.

        :param v: Vertex 1
        :type v: int
        :param w: Vertex 2
        :type w: int
        """

        if not {v, w}.issubset(self._vertices):
            raise ValueError(''.join(["One or more vertices in {} are not ",
                                      "present in the graph."]).format((v, w)))

        if (v, w) not in self:
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

    def __iter__(self):
        """Generates a sequence of graph edges in no particular order.

        :return: A sequence of graph edges
        :rtype: Iterable
        """

        for v in self._vertices:
            for w in self._adj[v]:
                yield v, w

    def reverse(self):
        """Generates a new Digraph based on the current one, but with all the
        edges reversed.

        :returns: A copy of this graph with the edges reversed
        :rtype: Digraph
        """

        R = DirectedGraph(vertices=self._vertices)
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
        for v in sorted(self._vertices):
            out.append("{}: {}".format(v, ', '.join(list(map(lambda x: str(x),
                                                            self._adj[v])))))
        return "\n".join(out)

    def __repr__(self):
        """Generates an official string representation of the graph with enough
        information to recreate it.

        :return: A string representation of the graph that can be eval'd
        :rtype: str
        """

        return "{}(vertices={}, edges={})".format(
            type(self).__name__,
            self._vertices,
            set(self))


if __name__ == "__main__":

    import unittest
    from os import path


    class TestDigraph(unittest.TestCase):

        vertices2 = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
        edges2 = ((0, 5),  (0, 1), (0, 6), (2, 0), (2, 3), (3, 5), (5, 4),
                  (6, 4), (6, 9), (7, 6), (8, 7), (9, 11), (9, 12), (9, 10),
                  (11, 12))

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyDG.txt')
            self.graph1 = DirectedGraph(filename=data_file)
            self.graph2 = DirectedGraph(vertices=self.vertices2,
                                        edges=self.edges2)

        def test_size(self):
            self.assertEqual(22, self.graph1.size())
            self.assertEqual(15, self.graph2.size())
            self.assertEqual(0, DirectedGraph().size())

        def test_len(self):
            self.assertEqual(22, len(self.graph1))
            self.assertEqual(15, len(self.graph2))
            self.assertEqual(0, len(DirectedGraph()))

        def test_order(self):
            self.assertEqual(13, self.graph1.order())
            self.assertEqual(13, self.graph2.order())
            self.assertEqual(0, DirectedGraph().order())

        def test_contains(self):
            self.assertTrue((2, 3) in self.graph1)
            self.assertFalse((9, 4) in self.graph1)
            self.assertTrue((3, 5) in self.graph2)
            self.assertFalse((9, 1) in self.graph2)
            self.assertFalse((1, 2) in DirectedGraph())

        def test_adj(self):
            self.assertEqual([1, 5], sorted(self.graph1.adj(0)))
            self.assertEqual([], sorted(self.graph1.adj(1)))
            self.assertEqual([0, 3], sorted(self.graph1.adj(2)))
            self.assertEqual([2, 5], sorted(self.graph1.adj(3)))
            self.assertEqual([2, 3], sorted(self.graph1.adj(4)))
            self.assertEqual([4], sorted(self.graph1.adj(5)))
            self.assertEqual([0, 4, 8, 9], sorted(self.graph1.adj(6)))
            self.assertEqual([6, 9], sorted(self.graph1.adj(7)))
            self.assertEqual([6], sorted(self.graph1.adj(8)))
            self.assertEqual([10, 11], sorted(self.graph1.adj(9)))
            self.assertEqual([12], sorted(self.graph1.adj(10)))
            self.assertEqual([4, 12], sorted(self.graph1.adj(11)))
            self.assertEqual([9], sorted(self.graph1.adj(12)))

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
            self.graph1.add_edge(0, 6)
            self.assertEqual([1, 5, 6], sorted(self.graph1.adj(0)))
            self.assertEqual([0, 4, 8, 9], sorted(self.graph1.adj(6)))
            self.assertEqual(23, self.graph1.size())

            # cannot add edge to a non-existent node
            self.assertRaises(ValueError, self.graph1.add_edge, 12, 13)
            self.assertEqual(23, self.graph1.size())
            self.assertEqual(13, self.graph1.order())

            self.graph2.add_edge(0, 7)
            self.assertEqual([1, 5, 6, 7], sorted(self.graph2.adj(0)))
            self.assertEqual([6], sorted(self.graph2.adj(7)))
            self.assertEqual(16, self.graph2.size())

            # an edge that already exists shouldn't change anything
            self.graph2.add_edge(6, 4)
            self.assertEqual(16, self.graph2.size())
            self.assertEqual([], sorted(self.graph2.adj(4)))
            self.assertEqual([4, 9], sorted(self.graph2.adj(6)))

        def test_iter(self):
            self.assertEqual(sorted(self.edges2), sorted(self.graph2))

        def test_reverse(self):
            R = self.graph1.reverse()
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
            graph1_out = [
                "0: 1, 5",
                "1: ",
                "2: 3, 0",
                "3: 2, 5",
                "4: 2, 3",
                "5: 4",
                "6: 0, 8, 4, 9",
                "7: 9, 6",
                "8: 6",
                "9: 10, 11",
                "10: 12",
                "11: 12, 4",
                "12: 9"
            ]
            self.assertEqual("\n".join(graph1_out), str(self.graph1))

            graph2_out = [
                "0: 5, 1, 6",
                "1: ",
                "2: 0, 3",
                "3: 5",
                "4: ",
                "5: 4",
                "6: 4, 9",
                "7: 6",
                "8: 7",
                "9: 11, 12, 10",
                "10: ",
                "11: 12",
                "12: "
            ]
            self.assertEqual("\n".join(graph2_out), str(self.graph2))

        def test_repr(self):
            self.assertEqual(
                ''.join([
                    "DirectedGraph(",
                    "vertices={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, ",
                    "edges={(0, 1), (6, 4), (5, 4), (6, 9), (7, 6), (9, 10), ",
                    "(0, 6), (2, 0), (9, 11), (0, 5), (2, 3), (8, 7), ",
                    "(11, 12), (9, 12), (3, 5)})"]),
                repr(self.graph2))

            graph = eval(repr(self.graph2))
            self.assertEqual(15, graph.size())
            self.assertEqual(13, graph.order())



    unittest.main()
