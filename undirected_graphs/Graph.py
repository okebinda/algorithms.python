"""Undirected Graph: Graph"""


class Graph:
    """A simple undirected graph. Contains zero-indexed vertices and edges as
    adjacency lists for each vertex."""

    def __init__(self, *, filename=None, size=None):
        """Graph constructor.

        :param filename: File with graph edges to load
        :type filename: str
        :param size: Number of graph vertices to initialize
        :type size: int
        """

        self._V = 0
        self._E = 0
        self._adj = []

        self._set_size(size)
        self._read_file(filename)

    def _set_size(self, size):
        """Initializes vertex count for graph, including empty adjacency lists.

        :param size: Number of graph vertices to initialize
        :type size: int
        """

        if size is not None:
            self._V = size
            self._adj = [[] for x in range(size)]

    def _read_file(self, filename):
        """Initializes edges of a graph based on an input file.

        :param filename: File with graph edges to load
        :type filename: str
        """

        if filename is not None:
            with open(filename, 'rt') as fp:
                for i, line in enumerate(fp):
                    if i == 0:
                        self._set_size(int(line))
                    elif i == 1:
                        # self._E = int(line)
                        pass
                    else:
                        edge = tuple(map(lambda x: int(x),
                                         line.rstrip().split(' ')))
                        self.add_edge(edge[0], edge[1])

    def V(self):
        """Reports the number of vertices in the graph.

        :return: Number of vertices in the graph
        :rtype: int
        """

        return self._V

    def E(self):
        """Reports the number of edges in the graph.

        :return: Number of edges in the graph
        :rtype: int
        """

        return self._E

    def add_edge(self, v, w):
        """Creates an edge between two vertices.

        :param v: Vertex 1
        :type v: int
        :param w: Vertex 2
        :type w: int 
        """

        self._adj[v].append(w)
        self._adj[w].append(v)
        self._E += 1

    def adj(self, v):
        """Retrieves the adjacency list for a vertex.

        :param v: Vertex
        :type v: int
        :return: The adjacency list of vertex v
        :rtype: list
        """
        return self._adj[v]

    def __str__(self):
        """Generates a human readable representation of the graph.

        :return: Vertex and edge count and adjacency list per vertex
        :rtype: str
        """

        out = ["Vertices: {}".format(self._V), "Edges: {}".format(self._E)]
        for v, adj in enumerate(self._adj):
            out.append("{}: {}".format(v, ' '.join(list(map(lambda x: str(x),
                                                            adj)))))
        return "\n".join(out)


if __name__ == "__main__":

    import unittest
    from os import path


    class TestGraph(unittest.TestCase):

        graph1 = None
        graph2 = None

        def setUp(self):
            data_path = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyG.txt')
            self.graph1 = Graph(filename=data_path)
            self.graph2 = Graph(size=5)

        def test_V(self):
            self.assertEqual(13, self.graph1.V())
            self.assertEqual(5, self.graph2.V())
            self.assertEqual(0, Graph().V())

        def test_E(self):
            self.assertEqual(13, self.graph1.E())
            self.assertEqual(0, self.graph2.E())
            self.assertEqual(0, Graph().E())

        def test_add_edge(self):
            self.graph1.add_edge(9, 7)
            self.assertEqual(14, self.graph1.E())
            self.assertEqual([7, 10, 11, 12], sorted(self.graph1.adj(9)))
            self.assertEqual([8, 9], sorted(self.graph1.adj(7)))

            self.graph2.add_edge(2, 3)
            self.graph2.add_edge(2, 4)
            self.assertEqual(2, self.graph2.E())
            self.assertEqual([3, 4], sorted(self.graph2.adj(2)))
            self.assertEqual([2], sorted(self.graph2.adj(3)))
            self.assertEqual([2], sorted(self.graph2.adj(4)))

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

        def test_str(self):
            graph1_out = [
                "Vertices: 13",
                "Edges: 13",
                "0: 5 1 2 6",
                "1: 0",
                "2: 0",
                "3: 4 5",
                "4: 3 6 5",
                "5: 0 4 3",
                "6: 4 0",
                "7: 8",
                "8: 7",
                "9: 12 10 11",
                "10: 9",
                "11: 12 9",
                "12: 9 11"
            ]
            self.assertEqual("\n".join(graph1_out), self.graph1.__str__())


    unittest.main()
