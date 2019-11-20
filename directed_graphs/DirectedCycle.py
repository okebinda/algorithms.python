"""Directed Graph: Directed Cycle"""


class DirectedCycle:
    """A Digraph client that uses depth-first search to detect a cycle in the
    graph."""

    def __init__(self, G):
        """DirectedCycle constructor.

        :param G: The complete graph to search
        :type G: Digraph
        """

        self._marked = [False] * G.order()
        self._on_stack = [False] * G.order()
        self._edge_to = [0] * G.order()
        self._cycle = []

        for v in range(G.order()):
            if not self._marked[v]:
                self._dfs(G, v)

    def _dfs(self, G, v):
        """Finds the first cycle (if any) on a graph using depth-first search.

        :param G: The complete graph to search
        :type G: Graph
        :param v: The vertex to start searching from
        :type v: int
        """

        self._marked[v] = True
        self._on_stack[v] = True
        for w in G.adj(v):
            if self.has_cycle():
                return
            elif not self._marked[w]:
                self._edge_to[w] = v
                self._dfs(G, w)
            elif self._on_stack[w]:
                self._cycle = []
                x = v
                while x != w:
                    self._cycle.append(x)
                    x = self._edge_to[x]
                self._cycle.append(w)
                self._cycle.append(v)
        self._on_stack[v] = False

    def has_cycle(self):
        """Reports if the graph has at least one cycle.

        :return: True if a cycle exists, otherwise false
        :rtype: bool
        """

        return bool(self._cycle)

    def cycle(self):
        """Reports the first cycle found in the graph.

        :return: The cycle sequence found.
        :rtype: iterable
        """

        return self._cycle


if __name__ == "__main__":

    import unittest
    from os import path

    from .Digraph import Digraph


    class TestDirectedCycle(unittest.TestCase):

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyDG.txt')
            self.graph = Digraph(filename=data_file)

        def test_has_cycle(self):
            dc = DirectedCycle(self.graph)
            self.assertTrue(dc.has_cycle())

        def test_cycle(self):
            dc = DirectedCycle(self.graph)
            self.assertEqual([3, 2, 3], dc.cycle())


    unittest.main()
