"""Edge Weighted Graph: Edge"""


class Edge:

    __slots__ = 'v', 'w', 'weight'

    def __init__(self, v, w, weight):
        """Edge constructor.

        :param v: Vertex 1
        :type v: int
        :param w: Vertex 2
        :type w: int
        :param weight: Edge weight
        :type weight: float
        """

        self.v = v
        self.w = w
        self.weight = weight

    def either(self):
        """Reports one of the vertices - doesn't matter which.

        :return: A vertex
        :rtype: int
        """

        return self.v

    def other(self, vertex):
        """Reports the vertex that is adjacent to the one given in the edge.

        :param vertex: A vertex
        :type vertex: int
        :return: The other vertex
        :rtype: int
        """

        if vertex == self.v:
            return self.w
        elif vertex == self.w:
            return self.v
        else:
            raise ValueError(
                "The vertex `{}` is not in the edge.".format(vertex))

    def __eq__(self, other):
        """Compares equality.

        :param other: An edge to compare with
        :type other: Edge
        :return: True if equal, False otherwise
        :rtype: bool
        """

        return self.weight == other.weight

    def __ne__(self, other):
        """Compares non-equality.

        :param other: An edge to compare with
        :type other: Edge
        :return: True if not equal, False otherwise
        :rtype: bool
        """

        return self.weight != other.weight

    def __lt__(self, other):
        """Compares less than.

        :param other: An edge to compare with
        :type other: Edge
        :return: True if self is less than other, False otherwise
        :rtype: bool
        """

        return self.weight < other.weight

    def __le__(self, other):
        """Compares less than or equal to.

        :param other: An edge to compare with
        :type other: Edge
        :return: True if self is less than or equal to other, False otherwise
        :rtype: bool
        """

        return self.weight <= other.weight

    def __gt__(self, other):
        """Compares greater than.

        :param other: An edge to compare with
        :type other: Edge
        :return: True if self is greater than other, False otherwise
        :rtype: bool
        """

        return self.weight > other.weight

    def __ge__(self, other):
        """Compares greater than or equal to.

        :param other: An edge to compare with
        :type other: Edge
        :return: True if self is greater than or equal to other, else False
        :rtype: bool
        """

        return self.weight >= other.weight

    def __hash__(self):
        """Generates the object's hash value.

        :return: The object's hash
        :rtype: int
        """

        return hash(self.v) ^ hash(self.w) ^ hash(self.weight)

    def __str__(self):
        """Generates a human readable representation of the edge.

        :return: The edge vertices and weight space delimited
        :rtype: str
        """

        return "{:d} {:d} {:.5f}".format(self.v, self.w, self.weight)

    def __repr__(self):
        """Generates an official string representation of the edge with enough
        information to recreate it.

        :return: A string representation of the edge that can be eval'd
        :rtype: str
        """

        return "{}({:d}, {:d}, {:.5f})".format(type(self).__name__, self.v,
                                               self.w, self.weight)


if __name__ == "__main__":

    import unittest


    class TestEdge(unittest.TestCase):

        def setUp(self):
            self.edge = Edge(1, 2, 4.1)

        def test_either(self):
            self.assertEqual(1, self.edge.either())

        def test_other(self):
            self.assertEqual(2, self.edge.other(self.edge.v))
            self.assertEqual(1, self.edge.other(self.edge.w))
            self.assertRaises(ValueError, self.edge.other, 200)

        def test_eq(self):
            self.assertTrue(self.edge == Edge(3, 4, 4.1))
            self.assertFalse(self.edge == Edge(3, 4, 4.0))

        def test_ne(self):
            self.assertTrue(self.edge != Edge(3, 4, 2.5))
            self.assertFalse(self.edge != Edge(3, 4, 4.1))

        def test_lt(self):
            self.assertTrue(self.edge < Edge(3, 4, 8.9))
            self.assertFalse(self.edge < Edge(3, 4, 0.4))

        def test_lt(self):
            self.assertTrue(self.edge <= Edge(3, 4, 5))
            self.assertTrue(self.edge <= Edge(5, 6, 4.1))
            self.assertFalse(self.edge <= Edge(3, 4, 2.9))

        def test_gt(self):
            self.assertTrue(self.edge > Edge(3, 4, 1.8))
            self.assertFalse(self.edge > Edge(3, 4, 6.7))

        def test_ge(self):
            self.assertTrue(self.edge >= Edge(3, 4, 3.45))
            self.assertTrue(self.edge >= Edge(3, 4, 4.1))
            self.assertFalse(self.edge >= Edge(3, 4, 7.2))

        def test_hash(self):
            self.assertEqual(230584300921368583, hash(self.edge))

        def test_str(self):
            self.assertEqual("1 2 4.10000", str(self.edge))

        def test_repr(self):
            self.assertEqual("Edge(1, 2, 4.10000)", repr(self.edge))
            self.assertEqual(eval(repr(self.edge)), self.edge)

    unittest.main()
