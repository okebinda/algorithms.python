"""Undirected Graph: Undirected Symbol Graph"""

from .Graph import Graph


class SymbolGraph(Graph):
    """An undirected graph with node labels."""

    def __init__(self, graph_class, *, filename=None, sp=None, vertices=None,
                 edges=None):
        """UndirectedSymbolGraph constructor.

        :;aram graph_class: Graph class to instantiate as the data structure
        :type graph_class: Graph class
        :param filename: File with graph edges to load
        :type filename: str
        :param sp: A string separating nodes on a single line in the input file
        :type sp: str
        :param vertices: A sequence of vertices to initialize
        :type vertices: iterable
        :param edges: A sequence of edges (as tuples) to initialize
        :type edges: iterable
        """

        self._G = graph_class()
        self._st = {}  # label: index
        self._keys = []  # index: label

        self._build_label_to_index_map_from_file(filename, sp)
        self._build_label_to_index_map_from_vertices(vertices)
        self._build_index_to_label_map()
        self._build_graph_from_file(filename, sp)
        self._build_graph_from_vertices_edges(vertices, edges)

    def _build_label_to_index_map_from_file(self, filename, sp):
        """Reads the input file and builds the internal symbol table that maps
        node labels to indexes.

        :param filename: File with graph edges to load
        :type filename: str
        :param sp: A string separating nodes on a single line in the input file
        :type sp: str
        """

        if filename is not None:
            with open(filename, 'rt') as fp:
                for i, v in enumerate(next(fp).rstrip().split(sp)):
                    self._st[v] = i

    def _build_label_to_index_map_from_vertices(self, vertices):
        """Builds the internal symbol table that maps node labels to indexes
        from a given sequence of vertices.

        :param vertices: A sequence of vertices to initialize
        :type vertices: Iterable
        """

        if vertices is not None:
            for i, v in enumerate(vertices, start=len(self._st)):
                self._st[v] = i

    def _build_index_to_label_map(self):
        """Build the list that maps node indexes to labels."""

        self._keys = [None] * len(self._st)
        for name in self._st:
            self._keys[self._st[name]] = name

    def _build_graph_from_file(self, filename, sp):
        """Reads the input file and builds the internal graph data structure.

        :param filename: File with graph edges to load
        :type filename: str
        :param sp: A string separating nodes on a single line in the input file
        :type sp: str
        """

        if filename is not None:
            with open(filename, 'rt') as fp:
                for i, line in enumerate(fp):
                    if i == 0:
                        for v in line.rstrip().split(sp):
                            self._G.add_vertex(self.index_of(v))
                    else:
                        a = line.rstrip().split(sp)
                        v = self._st[a[0]]
                        j = 1
                        while j < len(a):
                            self._G.add_edge(v, self._st[a[j]])
                            j += 1

    def _build_graph_from_vertices_edges(self, vertices, edges):
        """Builds the internal graph data structure from a given sequence of
        edges.

        :param vertices: A sequence of vertices to initialize
        :type vertices: Iterable
        :param edges: A sequence of edges (as tuples) to initialize
        :type edges: Iterable
        """

        if vertices is not None:
            for v in vertices:
                self._G.add_vertex(self._st[v])

        if edges is not None:
            for edge in edges:
                v, w = edge
                self._G.add_edge(self._st[v], self._st[w])

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

    def add_vertex(self, v):
        """Adds a vertex to the graph.

        :param v: Vertex to add
        :type v: str
        """

        if v not in self._st:
            self._st[v] = len(self._keys)
            self._keys.append(v)
            self._G.add_vertex(self._st[v])

    def add_edge(self, v, w):
        """Creates an edge between two vertices.

        :param v: Vertex 1 label
        :type v: str
        :param w: Vertex 2 label
        :type w: str
        """

        if not {v, w}.issubset(self._st):
            raise ValueError(''.join(["One or more vertices in {} are not ",
                                      "present in the graph."]).format((v, w)))

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

    def __repr__(self):
        """Generates an official string representation of the graph with enough
        information to recreate it.

        :return: A string representation of the graph that can be eval'd
        :rtype: str
        """

        return '{}({}, vertices={}, edges={})'.format(
            type(self).__name__,
            type(self._G).__name__,
            set(self._keys),
            set(self))

    def G(self):
        """Gets the internal graph data structure.

        :return: The internal graph representation
        :rtype: Graph
        """

        return self._G


if __name__ == "__main__":

    import unittest
    from os import path

    from graphs.undirected.BreadthFirstPaths import BreadthFirstPaths
    from graphs.undirected.UndirectedGraph import UndirectedGraph
    from graphs.directed.DirectedGraph import DirectedGraph


    class TestSymbolGraph(unittest.TestCase):

        vertices = ('ATL', 'DEN', 'DFW', 'HOU', 'JFK', 'LAS', 'LAX', 'MCO',
                    'ORD', 'PHX')
        edges = {('JFK', 'MCO'), ('ORD', 'DEN'), ('ORD', 'HOU'),
                 ('DFW', 'PHX'), ('JFK', 'ATL'), ('ORD', 'DFW'),
                 ('ORD', 'PHX'), ('ATL', 'HOU'), ('DEN', 'PHX'),
                 ('PHX', 'LAX'), ('JFK', 'ORD'), ('DEN', 'LAS'),
                 ('DFW', 'HOU'), ('ORD', 'ATL'), ('LAS', 'LAX'),
                 ('ATL', 'MCO'), ('HOU', 'MCO'), ('LAS', 'PHX')}

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'undirected/data/routes.txt')
            self.graph1 = SymbolGraph(UndirectedGraph, filename=data_file)
            self.graph2 = SymbolGraph(DirectedGraph, vertices=self.vertices,
                                      edges=self.edges)

        def test_exists(self):
            self.assertTrue(self.graph1.exists('JFK'))
            self.assertTrue(self.graph1.exists('ORD'))
            self.assertTrue(self.graph1.exists('ATL'))
            self.assertFalse(self.graph1.exists('ABC'))
            self.assertFalse(self.graph1.exists('XYZ'))

            self.assertTrue(self.graph2.exists('JFK'))
            self.assertTrue(self.graph2.exists('ORD'))
            self.assertTrue(self.graph2.exists('ATL'))
            self.assertFalse(self.graph2.exists('ABC'))
            self.assertFalse(self.graph2.exists('XYZ'))

        def test_index_of(self):
            self.assertEqual(0, self.graph1.index_of('ATL'))
            self.assertEqual(1, self.graph1.index_of('DEN'))
            self.assertEqual(2, self.graph1.index_of('DFW'))
            self.assertEqual(3, self.graph1.index_of('HOU'))

            self.assertEqual(0, self.graph2.index_of('ATL'))
            self.assertEqual(1, self.graph2.index_of('DEN'))
            self.assertEqual(2, self.graph2.index_of('DFW'))
            self.assertEqual(3, self.graph2.index_of('HOU'))

        def test_name_of(self):
            self.assertEqual("ATL", self.graph1.name_of(0))
            self.assertEqual("DEN", self.graph1.name_of(1))
            self.assertEqual("DFW", self.graph1.name_of(2))
            self.assertEqual("HOU", self.graph1.name_of(3))

            self.assertEqual("ATL", self.graph2.name_of(0))
            self.assertEqual("DEN", self.graph2.name_of(1))
            self.assertEqual("DFW", self.graph2.name_of(2))
            self.assertEqual("HOU", self.graph2.name_of(3))

        def test_size(self):
            self.assertEqual(18, self.graph1.size())
            self.assertEqual(18, self.graph2.size())

        def test_len(self):
            self.assertEqual(18, len(self.graph1))
            self.assertEqual(18, len(self.graph2))

        def test_order(self):
            self.assertEqual(10, self.graph1.order())
            self.assertEqual(10, self.graph2.order())

        def test_contains(self):
            self.assertTrue(('JFK', 'ATL') in self.graph1)
            self.assertTrue(('ATL', 'JFK') in self.graph1)
            self.assertFalse(('ORD', 'LAX') in self.graph1)

            self.assertTrue(('JFK', 'ATL') in self.graph2)
            self.assertFalse(('ATL', 'JFK') in self.graph2)
            self.assertFalse(('ORD', 'LAX') in self.graph2)

        def test_add_edge(self):

            # add edge with existing nodes
            self.graph1.add_edge('ORD', 'LAX')
            self.assertEqual(19, self.graph1.size())
            self.assertEqual(10, self.graph1.order())
            self.assertTrue(('ORD', 'LAX') in self.graph1)

            self.graph2.add_edge('ORD', 'LAX')
            self.assertEqual(19, self.graph2.size())
            self.assertEqual(10, self.graph2.order())
            self.assertTrue(('ORD', 'LAX') in self.graph2)

            # an edge that already exists shouldn't change anything
            self.graph1.add_edge('JFK', 'ATL')
            self.assertEqual(19, self.graph1.size())
            self.assertEqual(10, self.graph1.order())

            self.graph2.add_edge('JFK', 'ATL')
            self.assertEqual(19, self.graph2.size())
            self.assertEqual(10, self.graph2.order())

            # adding edge a new node raises an error
            self.assertRaises(ValueError, self.graph1.add_edge, 'LAX', 'SAN')
            self.assertEqual(19, self.graph1.size())
            self.assertEqual(10, self.graph1.order())

            self.assertRaises(ValueError, self.graph2.add_edge, 'LAX', 'SAN')
            self.assertEqual(19, self.graph2.size())
            self.assertEqual(10, self.graph2.order())

        def test_adj(self):
            self.assertEqual(['ATL', 'MCO', 'ORD'],
                             sorted(self.graph1.adj('JFK')))
            self.assertEqual(['ATL', 'DEN', 'DFW', 'HOU', 'JFK', 'PHX'],
                             sorted(self.graph1.adj('ORD')))

            self.assertEqual(['ATL', 'MCO', 'ORD'],
                             sorted(self.graph2.adj('JFK')))
            self.assertEqual(['ATL', 'DEN', 'DFW', 'HOU', 'PHX'],
                             sorted(self.graph2.adj('ORD')))

        def test_iter(self):
            edges = (('JFK', 'MCO'), ('ORD', 'DEN'), ('ORD', 'HOU'),
                     ('DFW', 'PHX'), ('JFK', 'ATL'), ('ORD', 'DFW'),
                     ('ORD', 'PHX'), ('ATL', 'HOU'), ('DEN', 'PHX'),
                     ('PHX', 'LAX'), ('JFK', 'ORD'), ('DEN', 'LAS'),
                     ('DFW', 'HOU'), ('ORD', 'ATL'), ('LAS', 'LAX'),
                     ('ATL', 'MCO'), ('HOU', 'MCO'), ('LAS', 'PHX'))
            for edge in self.graph1:
                v, w = edge
                self.assertTrue((v, w) in edges or (w, v) in edges)

            for edge in self.graph2:
                v, w = edge
                self.assertTrue((v, w) in edges)

        def test_str(self):
            graph1_out = [
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
            self.assertEqual("\n".join(graph1_out), str(self.graph1))

            graph2_out = [
                "ATL: HOU, MCO",
                "DEN: LAS, PHX",
                "DFW: HOU, PHX",
                "HOU: MCO",
                "JFK: ATL, MCO, ORD",
                "LAS: LAX, PHX",
                "LAX: ",
                "MCO: ",
                "ORD: ATL, DEN, DFW, HOU, PHX",
                "PHX: LAX"
            ]
            self.assertEqual("\n".join(graph2_out), str(self.graph2))

        def test_repr(self):
            graph = eval(repr(self.graph1))
            self.assertEqual(18, graph.size())
            self.assertEqual(10, graph.order())

        def test_G(self):
            self.assertIsInstance(self.graph1.G(), UndirectedGraph)
            self.assertIsInstance(self.graph2.G(), DirectedGraph)

        def test_client(self):
            self.assertEqual(
                ['ATL', 'MCO', 'ORD'],
                sorted([self.graph1.name_of(v) for v in self.graph1.G().adj(
                    self.graph1.index_of('JFK'))]))
            self.assertEqual(
                ['LAS', 'PHX'],
                sorted([self.graph1.name_of(v) for v in self.graph1.G().adj(
                    self.graph1.index_of('LAX'))]))

            self.assertEqual(
                ['ATL', 'MCO', 'ORD'],
                sorted([self.graph2.name_of(v) for v in self.graph2.G().adj(
                    self.graph2.index_of('JFK'))]))
            self.assertEqual(
                ['HOU', 'MCO'],
                sorted([self.graph2.name_of(v) for v in self.graph2.G().adj(
                    self.graph2.index_of('ATL'))]))

        def test_degrees_of_separation_client(self):
            bfs1 = BreadthFirstPaths(self.graph1.G(),
                                     self.graph1.index_of('JFK'))
            self.assertEqual(
                ['JFK', 'ORD', 'PHX', 'LAS'],
                [self.graph1.name_of(v) for v in bfs1.path_to(
                    self.graph1.index_of('LAS'))])
            self.assertEqual(
                ['JFK', 'ORD', 'DFW'],
                [self.graph1.name_of(v) for v in bfs1.path_to(
                    self.graph1.index_of('DFW'))])

            # BreadthFirstPaths is meant for undirected, but works for directed
            # too
            bfs2 = BreadthFirstPaths(self.graph2.G(),
                                     self.graph2.index_of('JFK'))
            self.assertEqual(
                ['JFK', 'ORD', 'DEN', 'LAS'],
                [self.graph2.name_of(v) for v in bfs2.path_to(
                    self.graph2.index_of('LAS'))])
            self.assertEqual(
                ['JFK', 'ORD', 'DFW'],
                [self.graph2.name_of(v) for v in bfs2.path_to(
                    self.graph2.index_of('DFW'))])

        def test_combo_graph(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'undirected/data/routes.txt')
            vertices = {'SAN', 'CLT', 'IAH'}
            edges = {('LAX', 'SAN'), ('CLT', 'IAH')}
            graph = SymbolGraph(UndirectedGraph, filename=data_file,
                                vertices=vertices, edges=edges)

            self.assertEqual(20, graph.size())
            self.assertEqual(13, graph.order())


    unittest.main()
