"""Undirected Graph: Symbol Graph"""

from .Graph import Graph


class SymbolGraph:
    """An undirected graph with node labels."""

    def __init__(self, *, filename=None, sp=None):
        """SymbolGraph constructor.

        :param filename: File with graph edges to load
        :type filename: str
        :param sp: A string separating nodes on a single line in the input file
        :type sp: str
        """

        self._build_label_to_index_map(filename, sp)
        self._build_index_to_label_map()
        self._build_graph(filename, sp)

    def _build_label_to_index_map(self, filename, sp):
        """Reads the input file and builds the internal symbol table that maps
        node labels to indexes.

        :param filename: File with graph edges to load
        :type filename: str
        :param sp: A string separating nodes on a single line in the input file
        :type sp: str
        """

        self._st = {}
        if filename is not None:
            with open(filename, 'rt') as fp:
                for line in fp:
                    a = line.rstrip().split(sp)
                    i = 0
                    while i < len(a):
                        if a[i] not in self._st:
                            self._st[a[i]] = len(self._st)
                        i += 1

    def _build_index_to_label_map(self):
        """Build the list that maps node indexes to labels."""

        self._keys = [None] * len(self._st)
        for name in self._st:
            self._keys[self._st[name]] = name

    def _build_graph(self, filename, sp):
        """Reads the input file and builds the internal graph data structure.

        :param filename: File with graph edges to load
        :type filename: str
        :param sp: A string separating nodes on a single line in the input file
        :type sp: str
        """

        self._G = Graph()
        if filename is not None:
            with open(filename, 'rt') as fp:
                for line in fp:
                    a = line.rstrip().split(sp)
                    v = self._st[a[0]]
                    i = 1
                    while i < len(a):
                        self._G.add_edge(v, self._st[a[i]])
                        i += 1

    def exists(self, s):
        """Determines if a node label is in the graph.

        :param s: A node label
        :type s: str
        :return: True if label is in graph, False otherwise
        :rtype: bool
        """

        return s in self._st

    def index_of(self, s):
        """Reports the zero-based index of the node label, determined by input
        order.

        :param s: A node label
        :type s: str
        :return: The zero-based index of the node
        :rtype: int
        """

        return self._st[s]

    def name_of(self, v):
        """Reports the label of the node at the given zero-based index.

        :param v: A zero-based index of the node
        :type v: int
        :return: The label of the node
        :rtype: str
        """

        return self._keys[v]

    def size(self):
        """Reports the number of edges in the graph.

        :return: Number of edges in the graph
        :rtype: int
        """

        return self._G.size()

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

        return self._G.order()

    def __contains__(self, edge):
        """Determines if an edge exists in the graph.

        :param edge: An edge represented as a tuple (v, w) to test for
        :type edge: tuple
        :return: True if edges exists, other wise False
        :rtype: bool
        """

        v, w = edge
        return (self.index_of(v), self.index_of(w)) in self._G

    def add_edge(self, v, w):
        """Creates an edge between two vertices.

        :param v: Vertex 1 label
        :type v: str
        :param w: Vertex 2 label
        :type w: str
        """

        if v not in self._st:
            self._st[v] = len(self._keys)
            self._keys.append(v)

        if w not in self._st:
            self._st[w] = len(self._keys)
            self._keys.append(w)

        self._G.add_edge(self.index_of(v), self.index_of(w))

    def adj(self, v):
        """Retrieves the adjacency list for a vertex.

        :param v: Vertex label
        :type v: str
        :return: The adjacency list of vertex v
        :rtype: list
        """

        return list(map(lambda x: self.name_of(x),
                        self._G.adj(self.index_of(v))))

    def __iter__(self):
        """Generates a sequence of graph edges in no particular order.

        :return: A sequence of graph edges
        :rtype: generator
        """

        completed = set()
        for v in self._keys:
            for w in self.adj(v):
                if (w, v) not in completed:
                    yield v, w
                    completed.add((v, w))

    def __str__(self):
        """Generates a human readable representation of the graph.

        :return: Vertex and edge count and adjacency list per vertex
        :rtype: str
        """

        out = []
        for v in sorted(self._keys):
            out.append("{}: {}".format(v, ", ".join(sorted(self.adj(v)))))
        return "\n".join(out)

    def G(self):
        """Gets the internal graph data structure.

        :return: The internal graph representation
        :rtype: Graph
        """

        return self._G


if __name__ == "__main__":

    import unittest
    from os import path

    from .BreadthFirstPaths import BreadthFirstPaths


    class TestSymbolGraph(unittest.TestCase):

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/routes.txt')
            self.graph = SymbolGraph(filename=data_file)

        def test_exists(self):
            self.assertTrue(self.graph.exists('JFK'))
            self.assertTrue(self.graph.exists('ORD'))
            self.assertTrue(self.graph.exists('ATL'))
            self.assertFalse(self.graph.exists('ABC'))
            self.assertFalse(self.graph.exists('XYZ'))

        def test_index_of(self):
            self.assertEqual(0, self.graph.index_of('JFK'))
            self.assertEqual(1, self.graph.index_of('MCO'))
            self.assertEqual(2, self.graph.index_of('ORD'))
            self.assertEqual(3, self.graph.index_of('DEN'))

        def test_name_of(self):
            self.assertEqual("JFK", self.graph.name_of(0))
            self.assertEqual("MCO", self.graph.name_of(1))
            self.assertEqual("ORD", self.graph.name_of(2))
            self.assertEqual("DEN", self.graph.name_of(3))

        def test_size(self):
            self.assertEqual(18, self.graph.size())

        def test_len(self):
            self.assertEqual(18, len(self.graph))

        def test_order(self):
            self.assertEqual(10, self.graph.order())

        def test_contains(self):
            self.assertTrue(('JFK', 'ATL') in self.graph)
            self.assertTrue(('ATL', 'JFK') in self.graph)
            self.assertFalse(('ORD', 'LAX') in self.graph)

        def test_add_edge(self):

            # add edge with existing nodes
            self.graph.add_edge('ORD', 'LAX')
            self.assertEqual(19, self.graph.size())
            self.assertEqual(10, self.graph.order())
            self.assertTrue(('ORD', 'LAX') in self.graph)

            # an edge that already exists shouldn't change anything
            self.graph.add_edge('JFK', 'ATL')
            self.assertEqual(19, self.graph.size())
            self.assertEqual(10, self.graph.order())

            # add edge with one new node
            self.graph.add_edge('LAX', 'SAN')
            self.assertEqual(20, self.graph.size())
            self.assertEqual(11, self.graph.order())
            self.assertTrue(('LAX', 'SAN') in self.graph)
            self.assertEqual(10, self.graph.index_of('SAN'))

            # add edge with two new nodes
            self.graph.add_edge('CLT', 'IAH')
            self.assertEqual(21, self.graph.size())
            self.assertEqual(13, self.graph.order())
            self.assertTrue(('CLT', 'IAH') in self.graph)
            self.assertEqual(11, self.graph.index_of('CLT'))
            self.assertEqual(12, self.graph.index_of('IAH'))

        def test_adj(self):
            self.assertEqual(['ATL', 'MCO', 'ORD'],
                             sorted(self.graph.adj('JFK')))
            self.assertEqual(['ATL', 'DEN', 'DFW', 'HOU', 'JFK', 'PHX'],
                             sorted(self.graph.adj('ORD')))

        def test_iter(self):
            edges = (('JFK', 'MCO'), ('ORD', 'DEN'), ('ORD', 'HOU'),
                     ('DFW', 'PHX'), ('JFK', 'ATL'), ('ORD', 'DFW'),
                     ('ORD', 'PHX'), ('ATL', 'HOU'), ('DEN', 'PHX'),
                     ('PHX', 'LAX'), ('JFK', 'ORD'), ('DEN', 'LAS'),
                     ('DFW', 'HOU'), ('ORD', 'ATL'), ('LAS', 'LAX'),
                     ('ATL', 'MCO'), ('HOU', 'MCO'), ('LAS', 'PHX'))
            for edge in self.graph:
                v, w = edge
                self.assertTrue((v, w) in edges or (w, v) in edges)

        def test_str(self):
            graph_out = [
                "ATL: HOU, JFK, MCO, ORD",
                "DEN: LAS, ORD, PHX",
                "DFW: HOU, ORD, PHX",
                "HOU: ATL, DFW, MCO, ORD",
                "JFK: ATL, MCO, ORD",
                "LAS: DEN, LAX, PHX",
                "LAX: LAS, PHX",
                "MCO: ATL, HOU, JFK",
                "ORD: ATL, DEN, DFW, HOU, JFK, PHX",
                "PHX: DEN, DFW, LAS, LAX, ORD"
            ]
            self.assertEqual("\n".join(graph_out), str(self.graph))

        def test_G(self):
            self.assertIsInstance(self.graph.G(), Graph)

        def test_client(self):
            self.assertEqual(
                ['ATL', 'MCO', 'ORD'],
                sorted([self.graph.name_of(v) for v in self.graph.G().adj(
                    self.graph.index_of('JFK'))]))
            self.assertEqual(
                ['LAS', 'PHX'],
                sorted([self.graph.name_of(v) for v in self.graph.G().adj(
                    self.graph.index_of('LAX'))]))

        def test_degrees_of_separation_client(self):
            bfs = BreadthFirstPaths(self.graph.G(), self.graph.index_of('JFK'))
            self.assertEqual(
                ['JFK', 'ORD', 'PHX', 'LAS'],
                [self.graph.name_of(v) for v in bfs.path_to(
                    self.graph.index_of('LAS'))])
            self.assertEqual(
                ['JFK', 'ORD', 'DFW'],
                [self.graph.name_of(v) for v in bfs.path_to(
                    self.graph.index_of('DFW'))])


    unittest.main()
