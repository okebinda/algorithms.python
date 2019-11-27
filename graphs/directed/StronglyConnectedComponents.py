"""Directed Graph: Kosaraju-Sharir Strongly Connected Components"""

from .DepthFirstOrder import DepthFirstOrder


class StronglyConnectedComponents:
    """A DirectedGraph client that uses depth-first search to find groups of
    nodes that can mutually reach each other - strongly connected components.
    In other words, for any given pair of nodes v and w, v can reach w and w
    can reach v. Uses Kosaraju-Sharir algorithm."""

    def __init__(self, G):
        """StronglyConnectedComponents constructor.

        :param G: The complete graph to analyze
        :type G: Graph
        """

        self._marked = [False] * G.order()
        self._id = [None] * G.order()
        self._count = 0

        dfo = DepthFirstOrder(G.reverse())
        for v in dfo.reverse_postorder():
            if not self._marked[v]:
                self._dfs(G, v)
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
            if not self._marked[w]:
                self._dfs(G, w)

    def strongly_connected(self, v, w):
        """Determines if two vertices are strongly connected.

        :param v: The first vertex to check for a connection
        :type v: int
        :param w: The second vertex to check for a connection
        :type w: int
        :return: True if vertices are strongly connected, False otherwise
        :rtype: bool
        """

        return self._id[v] == self._id[w]

    def id(self, v):
        """Reports the internal ID used for the entire strongly connected
        component that a vertex belongs to.

        :param v: A vertex that is a member of a strongly connected component
        :type v: int
        :return: The internal ID of the strongly connected component
        :rtype: int
        """

        return self._id[v]

    def count(self):
        """Reports the total number of strongly connected components in the
        graph.

        :return: The count of strongly connected components in the graph
        :rtype: int
        """

        return self._count


if __name__ == "__main__":

    import unittest
    from os import path

    from .DirectedGraph import DirectedGraph
    from graphs.SymbolGraph import SymbolGraph


    class TestStronglyConnectedComponents(unittest.TestCase):

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyDG.txt')
            self.graph = DirectedGraph(filename=data_file)
            self.scc = StronglyConnectedComponents(self.graph)

        def test_strongly_connected(self):
            self.assertTrue(self.scc.strongly_connected(0, 2))
            self.assertTrue(self.scc.strongly_connected(2, 0))
            self.assertTrue(self.scc.strongly_connected(11, 12))
            self.assertTrue(self.scc.strongly_connected(12, 11))
            self.assertFalse(self.scc.strongly_connected(1, 8))
            self.assertFalse(self.scc.strongly_connected(4, 9))

        def test_id(self):
            self.assertEqual(0, self.scc.id(1))
            self.assertEqual(1, self.scc.id(3))
            self.assertEqual(2, self.scc.id(10))
            self.assertEqual(3, self.scc.id(6))
            self.assertEqual(4, self.scc.id(7))

        def test_count(self):
            self.assertEqual(5, self.scc.count())

        def test_client(self):
            components = [[] for _ in range(self.scc.count())]
            for v in range(self.graph.order()):
                components[self.scc.id(v)].append(v)
            self.assertEqual([
                [1],
                [0, 2, 3, 4, 5],
                [9, 10, 11, 12],
                [6, 8],
                [7]
            ], components)

        def test_symbol_graph_client(self):

            # format of file after first line (all nodes) is:
            #   0->1->2->3...
            # where 0 is food for (directed to) 1, 2, 3...
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/food_web.txt')
            graph = SymbolGraph(DirectedGraph, filename=data_file, sp='->')
            scc = StronglyConnectedComponents(graph.G())
            components = [[] for _ in range(scc.count())]
            for v in range(graph.order()):
                components[scc.id(v)].append(graph.name_of(v))
            self.assertEqual([
                ['fox'],
                ['frog', 'salamander', 'shrew', 'egret', 'snake', 'fish'],
                ['algae'],
                ['ant'],
                ['worm'],
                ['slug'],
                ['mosquito'],
                ['grass']
            ], components)


    unittest.main()
