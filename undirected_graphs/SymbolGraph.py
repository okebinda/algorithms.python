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

        self._G = Graph(size=len(self._st))
        if filename is not None:
            with open(filename, 'rt') as fp:
                for line in fp:
                    a = line.rstrip().split(sp)
                    v = self._st[a[0]]
                    i = 1
                    while i < len(a):
                        self._G.add_edge(v, self._st[a[i]])
                        i += 1

    def contains(self, s):
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

        def test_contains(self):
            self.assertTrue(self.graph.contains('JFK'))
            self.assertTrue(self.graph.contains('ORD'))
            self.assertTrue(self.graph.contains('ATL'))
            self.assertFalse(self.graph.contains('ABC'))
            self.assertFalse(self.graph.contains('XYZ'))

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
