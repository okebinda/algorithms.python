"""Edge-Weighted Directed Graph: Edge Weighted Directed Graph"""

from collections import defaultdict

from graphs.Graph import Graph
from .DirectedEdge import DirectedEdge


class EdgeWeightedDirectedGraph(Graph):

    def __init__(self, *, filename=None, vertices=None, edges=None):
        """EdgeWeightedDirectedGraph constructor.

        :param filename: File with graph edges to load
        :type filename: str
        :param vertices: A sequence of vertices to initialize
        :type vertices: iterable
        :param edges: A sequence of edges to initialize
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
                        v, w, weight = line.rstrip().split(' ')
                        self.add_edge(DirectedEdge(int(v), int(w),
                                                   float(weight)))

    def _load_vertices(self, vertices):
        """Initializes vertices of a graph based on a sequence of integers.

        :param vertices: Sequence of vertex integers to load
        :type vertices: iterable
        """

        if vertices is not None:
            for v in vertices:
                self.add_vertex(v)

    def _load_edges(self, edges):
        """Initializes edges of a graph based on a sequence of edges.

        :param edges: Sequence of edges to load
        :type edges: iterable
        """

        if edges is not None:
            for edge in edges:
                self.add_edge(edge)

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
        :return: True if edges exists, otherwise False
        :rtype: bool
        """

        v = edge.frm
        w = edge.to

        if self._adj[v]:
            for e in self._adj[v]:
                if e.frm == v and e.to == w:
                    return True
        return False

    def add_vertex(self, v):
        """Adds a vertex to the graph.

        :param v: Vertex to add
        :type v: int
        """

        self._vertices.add(v)

    def add_edge(self, edge):
        """Creates an edge between two vertices.

        :param edge: Edge to add
        :type edge: DirectedEdge
        """

        v = edge.frm
        w = edge.to

        if not {v, w}.issubset(self._vertices):
            raise ValueError(''.join(["One or more vertices in {} are not ",
                                      "in the graph."]).format((v, w)))

        if edge not in self:
            self._adj[v].append(edge)
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

        for v in self._vertices:
            for edge in self.adj(v):
                yield edge

    def __str__(self):
        """Generates a human readable representation of the graph.

        :return: Adjacency list per vertex
        :rtype: str
        """

        out = []
        out.append(' '.join([str(x) for x in self._vertices]))
        for v in sorted(self._vertices):
            for edge in self.adj(v):
                out.append("{:d} {:d} {:.5f}".format(edge.frm, edge.to, edge.weight))
        return "\n".join(out)

    def __repr__(self):
        """Generates an official string representation of the graph with enough
        information to recreate it.

        :return: A string representation of the graph that can be eval'd
        :rtype: str
        """

        return '{}(vertices={}, edges={})'.format(
            type(self).__name__,
            self._vertices,
            set(self))


if __name__ == "__main__":

    import unittest
    from os import path


    class TestEdgeWeightedDirectedGraph(unittest.TestCase):

        vertices2 = {0, 1, 2, 3}
        edges2 = {DirectedEdge(2, 1, 0.39), DirectedEdge(1, 3, 0.12),
                  DirectedEdge(0, 2, 0.22)}

        def setUp(self):
            data_path = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyEWD.txt')
            self.graph1 = EdgeWeightedDirectedGraph(filename=data_path)
            self.graph2 = EdgeWeightedDirectedGraph(vertices=self.vertices2,
                                                    edges=self.edges2)

        def test_size(self):
            self.assertEqual(15, self.graph1.size())
            self.assertEqual(3, self.graph2.size())
            self.assertEqual(0, EdgeWeightedDirectedGraph().size())

        def test_len(self):
            self.assertEqual(15, len(self.graph1))
            self.assertEqual(3, len(self.graph2))
            self.assertEqual(0, len(EdgeWeightedDirectedGraph()))

        def test_order(self):
            self.assertEqual(8, self.graph1.order())
            self.assertEqual(4, self.graph2.order())
            self.assertEqual(0, EdgeWeightedDirectedGraph().order())

        def test_contains(self):
            self.assertTrue(DirectedEdge(4, 5, 0.35) in self.graph1)
            self.assertTrue(DirectedEdge(7, 3, 0.39) in self.graph1)
            self.assertFalse(DirectedEdge(5, 2, 0.47) in self.graph1)

            # only vertices are checked for inclusion, not weight
            self.assertTrue(DirectedEdge(4, 7, 0.15) in self.graph1)

            self.assertTrue(DirectedEdge(1, 3, 0.12) in self.graph2)
            self.assertFalse(DirectedEdge(3, 2, 0.18) in self.graph2)

        def test_add_vertex(self):
            self.graph1.add_vertex(8)
            self.assertEqual(9, self.graph1.order())

            # adding existing vertex does nothing
            self.graph1.add_vertex(4)
            self.assertEqual(9, self.graph1.order())

            self.graph2.add_vertex(4)
            self.assertEqual(5, self.graph2.order())

        def test_add_edge(self):
            self.graph1.add_edge((DirectedEdge(5, 2, 0.47)))
            self.assertEqual(16, len(self.graph1))
            self.assertEqual([
                DirectedEdge(5, 4, 0.35),
                DirectedEdge(5, 7, 0.28),
                DirectedEdge(5, 1, 0.32),
                DirectedEdge(5, 2, 0.47),
            ], self.graph1.adj(5))

        def test_adj(self):
            self.assertEqual([
                DirectedEdge(0, 4, 0.38),
                DirectedEdge(0, 2, 0.26),
            ], self.graph1.adj(0))
            self.assertEqual([
                DirectedEdge(1, 3, 0.29),
            ], self.graph1.adj(1))
            self.assertEqual([
                DirectedEdge(2, 7, 0.34),
            ], self.graph1.adj(2))
            self.assertEqual([
                DirectedEdge(3, 6, 0.52),
            ], self.graph1.adj(3))
            self.assertEqual([
                DirectedEdge(4, 5, 0.35),
                DirectedEdge(4, 7, 0.37),
            ], self.graph1.adj(4))
            self.assertEqual([
                DirectedEdge(5, 4, 0.35),
                DirectedEdge(5, 7, 0.28),
                DirectedEdge(5, 1, 0.32),
            ], self.graph1.adj(5))
            self.assertEqual([
                DirectedEdge(6, 2, 0.40),
                DirectedEdge(6, 0, 0.58),
                DirectedEdge(6, 4, 0.93),
            ], self.graph1.adj(6))
            self.assertEqual([
                DirectedEdge(7, 5, 0.28),
                DirectedEdge(7, 3, 0.39),
            ], self.graph1.adj(7))

        def test_iter(self):
            edges = [
                DirectedEdge(0, 4, 0.38),
                DirectedEdge(0, 2, 0.26),
                DirectedEdge(1, 3, 0.29),
                DirectedEdge(2, 7, 0.34),
                DirectedEdge(3, 6, 0.52),
                DirectedEdge(4, 5, 0.35),
                DirectedEdge(4, 7, 0.37),
                DirectedEdge(5, 4, 0.35),
                DirectedEdge(5, 7, 0.28),
                DirectedEdge(5, 1, 0.32),
                DirectedEdge(6, 2, 0.40),
                DirectedEdge(6, 0, 0.58),
                DirectedEdge(6, 4, 0.93),
                DirectedEdge(7, 5, 0.28),
                DirectedEdge(7, 3, 0.39),
            ]
            self.assertEqual(edges, list(iter(self.graph1)))

        def test_str(self):
            output = [
                "0 1 2 3 4 5 6 7",
                "0 4 0.38000",
                "0 2 0.26000",
                "1 3 0.29000",
                "2 7 0.34000",
                "3 6 0.52000",
                "4 5 0.35000",
                "4 7 0.37000",
                "5 4 0.35000",
                "5 7 0.28000",
                "5 1 0.32000",
                "6 2 0.40000",
                "6 0 0.58000",
                "6 4 0.93000",
                "7 5 0.28000",
                "7 3 0.39000",
            ]
            self.assertEqual("\n".join(output), str(self.graph1))

        def test_rep(self):
            graph = eval(repr(self.graph1))
            self.assertEqual(graph.size(), self.graph1.size())
            self.assertEqual(graph.order(), self.graph1.order())
            for edge in graph:
                self.assertTrue(edge in self.graph1)


    unittest.main()
