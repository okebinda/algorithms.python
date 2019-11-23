"""Directed Graph: Topological Sort"""

from .DirectedCycle import DirectedCycle
from .DepthFirstOrder import DepthFirstOrder


class TopologicalSort:
    """A DirectedGraph client that performs a topological sort on a Directed
    Acyclic Graph (DAG), useful for things like resolving dependencies or
    scheduling."""

    def __init__(self, G):
        """TopologicalSort constructor.

        :param G: The complete graph to search
        :type G: DirectedGraph
        """

        self._order = None
        cycle_finder = DirectedCycle(G)
        if not cycle_finder.has_cycle():
            dfs = DepthFirstOrder(G)
            self._order = dfs.reverse_postorder()

    def order(self):
        """Reports the sorted nodes.

        :return: A sequence of nodes sorted topologically
        :rtype: Iterable
        """

        return self._order

    def has_order(self):
        """Determines if nodes have been ordered.

        :return: True if nodes have been ordered, false otherwise
        :rtype: bool
        """

        return self._order is not None


if __name__ == "__main__":

    import unittest
    from os import path

    from .DirectedGraph import DirectedGraph
    from graphs.SymbolGraph import SymbolGraph


    class TestTopologicalSort(unittest.TestCase):

        edges = ((0, 5), (0, 1), (0, 6), (2, 0), (2, 3), (3, 5), (5, 4),
                 (6, 4), (6, 9), (7, 6), (8, 7), (9, 11), (9, 12), (9, 10),
                 (11, 12))

        def setUp(self):
            graph = DirectedGraph(edges=self.edges)
            self.ts = TopologicalSort(graph)

        def test_has_order(self):
            self.assertTrue(self.ts.has_order())

        def test_order(self):
            self.assertEqual([8, 7, 2, 3, 0, 6, 9, 10, 11, 12, 1, 5, 4],
                             list(self.ts.order()))

        def test_order_symbol_graph(self):

            # format of file is:
            #   0/1/2/3...
            # where 0 is a prerequisite for (directed to) 1, 2, 3...
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/jobs.txt')
            graph = SymbolGraph(DirectedGraph, filename=data_file, sp='/')
            ts = TopologicalSort(graph.G())
            ordered = [
                'Calculus',
                'Linear Algebra',
                'Introduction to CS',
                'Advanced Programming',
                'Algorithms',
                'Scientific Computing',
                'Databases',
                'Theoretical CS',
                'Artificial Intelligence',
                'Machine Learning',
                'Robotics',
                'Neural Networks',
                'Computational Biology'
            ]
            self.assertEqual(ordered, list(map(lambda x: graph.name_of(x),
                                               ts.order())))


    unittest.main()
