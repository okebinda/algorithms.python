"""Edge Weighted Graph: Prim's Minimum Spanning Tree"""

import math

from containers.MinPriorityQueue import MinPriorityQueue


class PrimMST:
    """An EdgeWeightedGraph client that finds the minimum spanning tree for the
    graph. Uses Prim's algorithm."""

    def __init__(self, G):
        """PrimMST constructor.

        :param G: The complete graph to analyze
        :type G: EdgeWeightedGraph
        """

        self._edge_to = [None] * G.order()
        self._dist_to = [math.inf] * G.order()
        self._marked = [False] * G.order()
        self._pq = MinPriorityQueue()

        self._dist_to[0] = 0.0
        self._pq.enqueue(0, 0.0)
        while self._pq:
            self._visit(G, self._pq.dequeue())

    def _visit(self, G, v):
        """Visits each connected graph node and finds the lowest weighted
        edges.

        :param G: The complete graph to analyze
        :type G: EdgeWeightedGraph
        :param v: The starting vertex
        :type v: int
        """

        self._marked[v] = True
        for edge in G.adj(v):
            w = edge.other(v)
            if self._marked[w]:
                continue
            if edge.weight < self._dist_to[w]:
                self._edge_to[w] = edge
                self._dist_to[w] = edge.weight
                if w in self._pq:
                    self._pq.update_priority(w, self._dist_to[w])
                else:
                    self._pq.enqueue(w, self._dist_to[w])

    def __iter__(self):
        """Iterates over all the edges with the lowest weights: the Minimum
        Spanning Tree.

        :return: Iterator of edges
        :rtype: iterable
        """

        return iter(self._edge_to[1:])

    def weight(self):
        """Reports the sum of all edge weights in the MST.

        :return: The sum of the lowest weights in the connected graph
        :rtype: numeric
        """

        return sum(self._dist_to)


if __name__ == "__main__":

    import unittest
    from os import path

    from .EdgeWeightedGraph import EdgeWeightedGraph
    from .Edge import Edge


    class TestPrimMST(unittest.TestCase):

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyEWG.txt')
            self.graph = EdgeWeightedGraph(filename=data_file)
            self.mst = PrimMST(self.graph)

        def test_iter(self):
            edges = [
                Edge(1, 7, 0.19),
                Edge(0, 2, 0.26),
                Edge(2, 3, 0.17),
                Edge(4, 5, 0.35),
                Edge(5, 7, 0.28),
                Edge(6, 2, 0.40),
                Edge(0, 7, 0.16)]
            self.assertEqual(edges, list(self.mst))

        def test_weight(self):
            self.assertEqual(1.81, round(self.mst.weight(), 2))


    unittest.main()
