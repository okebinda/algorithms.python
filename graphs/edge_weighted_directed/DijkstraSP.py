"""Edge-Weighted Directed Graph: Dijkstra's Shortest Path"""

import math

from containers.MinPriorityQueue import MinPriorityQueue


class DijkstraSP:
    """An EdgeWeightedDirectedGraph client that finds the shortest path between
    two vertices on the graph. Uses Dijkstra's algorithm."""

    def __init__(self, G, s):
        """DijkstraSP constructor.

        :param G: The complete graph to analyze
        :type G: EdgeWeightedDirectedGraph
        :param s: The starting vertex for all path searches
        :type s: int
        """

        self._edge_to = [None] * G.order()
        self._dist_to = [math.inf] * G.order()
        self._pq = MinPriorityQueue()

        self._dist_to[s] = 0.
        self._pq.enqueue(s, 0.)
        while self._pq:
            self._relax(G, self._pq.dequeue())

    def _relax(self, G, v):
        """Relaxes the stored distance between the starting vertex and the
        given vertex.

        :param G: The complete graph to analyze
        :type G: EdgeWeightedDirectedGraph
        :param v: The ending vertex
        :type v: int
        """

        for edge in G.adj(v):
            w = edge.to
            if self._dist_to[w] > self._dist_to[v] + edge.weight:
                self._dist_to[w] = self._dist_to[v] + edge.weight
                self._edge_to[w] = edge
                if w in self._pq:
                    self._pq.update_priority(w, self._dist_to[w])
                else:
                    self._pq.enqueue(w, self._dist_to[w])

    def dist_to(self, v):
        """Reports the shortest distance between the starting vertex and the
        given vertex.

        :param v: The ending vertex
        :type v: int
        :return: The distance between the starting and ending vertices
        :rtype: float
        """

        return self._dist_to[v]

    def has_path_to(self, v):
        """Report if there is a path between the starting vertex and the given
        vertex.

        :param v: The ending vertex
        :type v: int
        :return: True if a path exists, False otherwis
        :rtype: bool
        """

        return self._dist_to[v] < math.inf

    def path_to(self, v):
        """Reports the path (as a tuple of edges) between the starting vertex
        and the given vertex.

        :param v: The ending vertex
        :type v: int
        :return: A sequence of DirectedEdges forming the path between vertices
        :rtype: tuple
        """

        if not self.has_path_to(v):
            return None
        v_path = []
        edge = self._edge_to[v]
        while edge:
            v_path.append(edge)
            edge = self._edge_to[edge.frm]
        return tuple(v_path)


if __name__ == "__main__":

    import unittest
    from os import path

    from .EdgeWeightedDirectedGraph import EdgeWeightedDirectedGraph
    from .DirectedEdge import DirectedEdge


    class TestDijkstraSP(unittest.TestCase):

        def setUp(self):
            data_file = path.join(path.abspath(path.dirname(__file__)),
                                  'data/tinyEWD.txt')
            self.graph = EdgeWeightedDirectedGraph(filename=data_file)

        def test_dist_to(self):
            sp = DijkstraSP(self.graph, 0)
            self.assertEqual(0, round(sp.dist_to(0), 2))
            self.assertEqual(1.05, round(sp.dist_to(1), 2))
            self.assertEqual(0.26, round(sp.dist_to(2), 2))
            self.assertEqual(0.99, round(sp.dist_to(3), 2))
            self.assertEqual(0.38, round(sp.dist_to(4), 2))
            self.assertEqual(0.73, round(sp.dist_to(5), 2))
            self.assertEqual(1.51, round(sp.dist_to(6), 2))
            self.assertEqual(0.60, round(sp.dist_to(7), 2))

        def test_has_path_to(self):
            sp = DijkstraSP(self.graph, 0)
            self.assertTrue(sp.has_path_to(1))
            self.assertTrue(sp.has_path_to(2))
            self.assertTrue(sp.has_path_to(3))
            self.assertTrue(sp.has_path_to(4))
            self.assertTrue(sp.has_path_to(5))
            self.assertTrue(sp.has_path_to(6))
            self.assertTrue(sp.has_path_to(7))

            # default graph is connected, so let's add an extra edge
            self.graph.add_vertex(8)
            self.graph.add_edge(DirectedEdge(8, 1, 0.15))
            sp2 = DijkstraSP(self.graph, 0)
            self.assertFalse(sp2.has_path_to(8))

        def test_path_to(self):
            sp = DijkstraSP(self.graph, 0)
            path_to_6 = (
                DirectedEdge(3, 6, 0.52),
                DirectedEdge(7, 3, 0.39),
                DirectedEdge(2, 7, 0.34),
                DirectedEdge(0, 2, 0.26),
            )
            self.assertEqual(path_to_6, sp.path_to(6))


    unittest.main()
