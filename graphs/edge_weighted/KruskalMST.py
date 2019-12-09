"""Edge-Weighted Graph: Kruskal's Minimum Spanning Tree"""

from containers.Queue import Queue
from containers.MinPriorityQueue import MinPriorityQueue
from graphs.UnionFind import UnionFind


class KruskalMST:
    """An EdgeWeightedGraph client that finds the minimum spanning tree for the
    graph. Uses Kruskal's algorithm."""

    def __init__(self, G):
        """KruskalMST constructor.

        :param G: The complete graph to analyze
        :type G: EdgeWeightedGraph
        """

        self._mst = Queue()
        pq = MinPriorityQueue()
        for edge in G:
            pq.enqueue(edge, edge.weight)
        uf = UnionFind(G.order())

        while pq and len(self._mst) < G.order() - 1:
            e = pq.dequeue()
            v = e.either()
            w = e.other(v)
            if uf.connected(v, w):
                continue
            uf.union(v, w)
            self._mst.enqueue(e)

    def __iter__(self):
        """Iterates over all the edges with the lowest weights: the Minimum
        Spanning Tree.

        :return: Iterator of edges
        :rtype: iterable
        """

        return iter(self._mst)

    def weight(self):
        """Reports the sum of all edge weights in the MST.

        :return: The sum of the lowest weights in the connected graph
        :rtype: numeric
        """

        return sum(map(lambda x: x.weight, self._mst))


if __name__ == "__main__":

    import unittest
    from os import path

    from .Edge import Edge
    from .EdgeWeightedGraph import EdgeWeightedGraph


    class TestKruskalMST(unittest.TestCase):

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyEWG.txt')
            self.graph = EdgeWeightedGraph(filename=data_file)
            self.mst = KruskalMST(self.graph)

        def test_iter(self):
            edges = [
                Edge(0, 7, 0.16),
                Edge(2, 3, 0.17),
                Edge(1, 7, 0.19),
                Edge(0, 2, 0.26),
                Edge(5, 7, 0.28),
                Edge(4, 5, 0.35),
                Edge(6, 2, 0.40)]
            self.assertEqual(edges, list(self.mst))

        def test_weight(self):
            self.assertEqual(1.81, round(self.mst.weight(), 2))


    unittest.main()
