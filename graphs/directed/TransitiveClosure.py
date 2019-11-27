"""Directed Graph: Transitive Closure"""

from .DirectedDepthFirstSearch import DirectedDepthFirstSearch


class TransitiveClosure:
    """A DirectedGraph client that uses depth-first search to determine if a
    directed path exists between any two vertices."""

    def __init__(self, G):
        """TransitiveClosure constructor.

        :param G: The complete graph to analyze
        :type G: Graph
        """

        self._all = [None] * G.order()
        for v in range(G.order()):
            self._all[v] = DirectedDepthFirstSearch(G, v)

    def reachable(self, v, w):
        """Determines if the vertex w is reachable from vertex v, such that:
        path v->...->w exists.

        :param v: The vertex to start checking reachability from
        :type v: int
        :param w: The vertex to check for reachability to
        :type w: int
        :return: True if w is reachable from v, False otherwise
        :rtype: bool
        """

        return self._all[v].marked(w)


if __name__ == "__main__":

    import unittest
    from os import path

    from .DirectedGraph import DirectedGraph
    from graphs.SymbolGraph import SymbolGraph


    class TestTransitiveClosure(unittest.TestCase):

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyDG.txt')
            graph = DirectedGraph(filename=data_file)
            self.tc = TransitiveClosure(graph)

        def test_reachable(self):
            self.assertTrue(self.tc.reachable(0, 4))
            self.assertTrue(self.tc.reachable(2, 5))
            self.assertTrue(self.tc.reachable(7, 3))
            self.assertTrue(self.tc.reachable(12, 5))
            self.assertFalse(self.tc.reachable(12, 7))
            self.assertFalse(self.tc.reachable(2, 9))
            self.assertFalse(self.tc.reachable(10, 8))

        def test_symbol_graph_client(self):

            # format of file after first line (all nodes) is:
            #   0->1->2->3...
            # where 0 is food for (directed to) 1, 2, 3...
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/food_web.txt')
            graph = SymbolGraph(DirectedGraph, filename=data_file, sp='->')
            tc = TransitiveClosure(graph.G())

            # v is in the food chain for w
            self.assertTrue(tc.reachable(graph.index_of('grass'),
                                         graph.index_of('fox')))
            self.assertTrue(tc.reachable(graph.index_of('worm'),
                                         graph.index_of('egret')))

            # v is not in the food chain for w
            self.assertFalse(tc.reachable(graph.index_of('shrew'),
                                          graph.index_of('algae')))
            self.assertFalse(tc.reachable(graph.index_of('fox'),
                                          graph.index_of('mosquito')))


    unittest.main()
