"""Directed Graph: Depth-First Order"""

from collections import deque


class DepthFirstOrder:
    """A DirectedGraph client that uses depth-first search to visit all
    vertices and store them in pre-order, post-order, and reverse post-order
    collections for further processing."""

    def __init__(self, G):
        """DepthFirstOrder constructor.

        :param G: The complete graph to search
        :type G: DirectedGraph
        """

        self._pre = deque()
        self._post = deque()
        self._reverse_post = deque()
        self._marked = [False] * G.order()

        for v in range(G.order()):
            if not self._marked[v]:
                self._dfs(G, v)

    def _dfs(self, G, v):
        """Visits all vertices on a graph and stores them in pre-order,
        post-order, and reverse post-order using depth-first search.

        :param G: The complete graph to search
        :type G: DirectedGraph
        :param v: The vertex to start searching from
        :type v: int
        """

        self._pre.append(v)

        self._marked[v] = True
        for w in G.adj(v):
            if not self._marked[w]:
                self._dfs(G, w)

        self._post.append(v)
        self._reverse_post.append(v)

    def preorder(self):
        """Generates a sequence of vertices in pre-order.

        :return: A sequence of graph vertices
        :rtype: Iterable
        """

        while self._pre:
            yield self._pre.popleft()

    def postorder(self):
        """Generates a sequence of vertices in post-order.

        :return: A sequence of graph vertices
        :rtype: Iterable
        """

        while self._post:
            yield self._post.popleft()

    def reverse_postorder(self):
        """Generates a sequence of vertices in reverse post-order.

        :return: A sequence of graph vertices
        :rtype: Iterable
        """

        while self._reverse_post:
            yield self._reverse_post.pop()


if __name__ == "__main__":

    import unittest

    from .DirectedGraph import DirectedGraph


    class TestDepthFirstOrder(unittest.TestCase):

        vertices = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
        edges = ((0, 5), (0, 1), (0, 6), (2, 0), (2, 3), (3, 5), (5, 4),
                 (6, 4), (6, 9), (7, 6), (8, 7), (9, 11), (9, 12), (9, 10),
                 (11, 12))

        def setUp(self):
            graph = DirectedGraph(vertices=self.vertices, edges=self.edges)
            self.dfo = DepthFirstOrder(graph)

        def test_preorder(self):
            self.assertEqual([0, 5, 4, 1, 6, 9, 11, 12, 10, 2, 3, 7, 8],
                             list(self.dfo.preorder()))

        def test_postorder(self):
            self.assertEqual([4, 5, 1, 12, 11, 10, 9, 6, 0, 3, 2, 7, 8],
                             list(self.dfo.postorder()))

        def test_reverse_postorder(self):
            self.assertEqual([8, 7, 2, 3, 0, 6, 9, 10, 11, 12, 1, 5, 4],
                             list(self.dfo.reverse_postorder()))


    unittest.main()
