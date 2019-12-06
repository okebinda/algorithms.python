"""Edge-Weighted Graph: Edge Weighted Graph"""

from collections import defaultdict

from graphs.Graph import Graph
from .Edge import Edge


class EdgeWeightedGraph(Graph):

    def __init__(self, *, filename=None, vertices=None, edges=None):
        """EdgeWeightedGraph constructor.

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
                        self.add_edge(Edge(int(v), int(w), float(weight)))

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

        v = edge.either()
        w = edge.other(v)
        if self._adj[v]:
            for e in self._adj[v]:
                if (e.v == v and e.w == w) or (e.v == w and e.w == v):
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
        :type edge: Edge
        """

        v = edge.either()
        w = edge.other(v)

        if not {v, w}.issubset(self._vertices):
            raise ValueError(''.join(["One or more vertices in {} are not ",
                                      "present in the graph."]).format((v, w)))

        if edge not in self:
            self._adj[v].append(edge)
            self._adj[w].append(edge)
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
            for edge in self._adj[v]:
                if edge not in completed:
                    yield edge
                    completed.add(edge)

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

        return '{}(vertices={}, edges={})'.format(
            type(self).__name__,
            self._vertices,
            set(self))


if __name__ == "__main__":

    import unittest
    from os import path


    class TestEdgeWeightedGraph(unittest.TestCase):

        vertices2 = {0, 1, 2, 3}
        edges2 = {Edge(2, 1, 0.39), Edge(1, 3, 0.12), Edge(0, 2, 0.22)}

        def setUp(self):
            data_path = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyEWG.txt')
            self.graph1 = EdgeWeightedGraph(filename=data_path)
            self.graph2 = EdgeWeightedGraph(vertices=self.vertices2,
                                            edges=self.edges2)

        def test_size(self):
            self.assertEqual(16, self.graph1.size())
            self.assertEqual(3, self.graph2.size())
            self.assertEqual(0, EdgeWeightedGraph().size())

        def test_len(self):
            self.assertEqual(16, len(self.graph1))
            self.assertEqual(3, len(self.graph2))
            self.assertEqual(0, len(EdgeWeightedGraph()))

        def test_order(self):
            self.assertEqual(8, self.graph1.order())
            self.assertEqual(4, self.graph2.order())
            self.assertEqual(0, EdgeWeightedGraph().order())

        def test_contains(self):
            self.assertTrue(Edge(4, 5, 0.35) in self.graph1)
            self.assertTrue(Edge(0, 2, 0.26) in self.graph1)
            self.assertFalse(Edge(5, 2, 0.34) in self.graph1)

            self.assertTrue(Edge(1, 3, 0.12) in self.graph2)
            self.assertFalse(Edge(3, 0, 0.49) in self.graph2)

            # only vertices are checked for inclusion, not weight
            self.assertTrue(Edge(0, 2, 0.50) in self.graph1)

        def test_add_vertex(self):
            self.graph1.add_vertex(8)
            self.assertEqual(9, self.graph1.order())

            # adding existing vertex does nothing
            self.graph1.add_vertex(2)
            self.assertEqual(9, self.graph1.order())

            self.graph2.add_vertex(4)
            self.assertEqual(5, self.graph2.order())

        def test_add_edge(self):
            self.graph1.add_edge(Edge(5, 2, 3.9))
            self.assertEqual(17, len(self.graph1))
            self.assertEqual(
                [
                    Edge(4, 5, 0.35),
                    Edge(5, 7, 0.28),
                    Edge(1, 5, 0.32),
                    Edge(5, 2, 3.9)
                ],
                self.graph1.adj(5))
            self.assertEqual(
                [
                    Edge(2, 3, 0.17),
                    Edge(0, 2, 0.26),
                    Edge(1, 2, 0.36),
                    Edge(2, 7, 0.34),
                    Edge(6, 2, 0.40),
                    Edge(5, 2, 3.9)
                ],
                self.graph1.adj(2))

            # an edge that already exists shouldn't change anything
            self.graph1.add_edge(Edge(4, 5, 0.35))
            self.assertEqual(17, len(self.graph1))

            self.graph2.add_edge(Edge(2, 3, 0.03))
            self.assertEqual(4, len(self.graph2))
            self.assertEqual(
                [
                    Edge(2, 1, 0.39),
                    Edge(0, 2, 0.22),
                    Edge(2, 3, 0.03)
                ],
                self.graph2.adj(2))
            self.assertEqual(
                [
                    Edge(1, 3, 0.12),
                    Edge(2, 3, 0.03)
                ],
                self.graph2.adj(3))

        def test_adj(self):
            self.assertEqual(
                [
                    Edge(0, 7, 0.16),
                    Edge(0, 4, 0.38),
                    Edge(0, 2, 0.26),
                    Edge(6, 0, 0.58)
                ],
                self.graph1.adj(0))
            self.assertEqual(
                [
                    Edge(1, 5, 0.32),
                    Edge(1, 7, 0.19),
                    Edge(1, 2, 0.36),
                    Edge(1, 3, 0.29)
                ],
                self.graph1.adj(1))
            self.assertEqual(
                [
                    Edge(2, 3, 0.17),
                    Edge(0, 2, 0.26),
                    Edge(1, 2, 0.36),
                    Edge(2, 7, 0.34),
                    Edge(6, 2, 0.40)
                ],
                self.graph1.adj(2))
            self.assertEqual(
                [
                    Edge(2, 3, 0.17),
                    Edge(1, 3, 0.29),
                    Edge(3, 6, 0.52)
                ],
                self.graph1.adj(3))
            self.assertEqual(
                [
                    Edge(4, 5, 0.35),
                    Edge(4, 7, 0.37),
                    Edge(0, 4, 0.38),
                    Edge(6, 4, 0.93)
                ],
                self.graph1.adj(4))
            self.assertEqual(
                [
                    Edge(4, 5, 0.35),
                    Edge(5, 7, 0.28),
                    Edge(1, 5, 0.32),
                ],
                self.graph1.adj(5))
            self.assertEqual(
                [
                    Edge(6, 2, 0.40),
                    Edge(3, 6, 0.52),
                    Edge(6, 0, 0.58),
                    Edge(6, 4, 0.93)
                ],
                self.graph1.adj(6))
            self.assertEqual(
                [
                    Edge(4, 7, 0.37),
                    Edge(5, 7, 0.28),
                    Edge(0, 7, 0.16),
                    Edge(1, 7, 0.19),
                    Edge(2, 7, 0.34)
                ],
                self.graph1.adj(7))

        def test_iter(self):
            edges = [
                Edge(0, 7, 0.16),
                Edge(0, 4, 0.38),
                Edge(0, 2, 0.26),
                Edge(6, 0, 0.58),
                Edge(1, 5, 0.32),
                Edge(1, 7, 0.19),
                Edge(1, 2, 0.36),
                Edge(1, 3, 0.29),
                Edge(2, 3, 0.17),
                Edge(2, 7, 0.34),
                Edge(6, 2, 0.40),
                Edge(3, 6, 0.52),
                Edge(4, 5, 0.35),
                Edge(4, 7, 0.37),
                Edge(6, 4, 0.93),
                Edge(5, 7, 0.28)
            ]
            self.assertEqual(edges, list(self.graph1))
            
            self.assertEqual([Edge(0, 2, 0.22), Edge(1, 3, 0.12),
                              Edge(2, 1, 0.39)], list(self.graph2))

        def test_str(self):
            graph1_out = [
                "0: 0 7 0.16000, 0 4 0.38000, 0 2 0.26000, 6 0 0.58000",
                "1: 1 5 0.32000, 1 7 0.19000, 1 2 0.36000, 1 3 0.29000",
                "2: 2 3 0.17000, 0 2 0.26000, 1 2 0.36000, 2 7 0.34000, 6 2 0.40000",
                "3: 2 3 0.17000, 1 3 0.29000, 3 6 0.52000",
                "4: 4 5 0.35000, 4 7 0.37000, 0 4 0.38000, 6 4 0.93000",
                "5: 4 5 0.35000, 5 7 0.28000, 1 5 0.32000",
                "6: 6 2 0.40000, 3 6 0.52000, 6 0 0.58000, 6 4 0.93000",
                "7: 4 7 0.37000, 5 7 0.28000, 0 7 0.16000, 1 7 0.19000, 2 7 0.34000"
            ]
            self.assertEqual("\n".join(graph1_out), str(self.graph1))

        def test_repr(self):
            graph = eval(repr(self.graph1))
            self.assertEqual(graph.size(), self.graph1.size())
            self.assertEqual(graph.order(), self.graph1.order())
            for edge in graph:
                self.assertTrue(edge in self.graph1)


    unittest.main()
