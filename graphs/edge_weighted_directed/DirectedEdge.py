"""Edge-Weighted Directed Graph: Directed Edge"""


class DirectedEdge:

    __slots__ = 'frm', 'to', 'weight'

    def __init__(self, v, w, weight):
        """DirectedEdge constructor.

        :param v: Vertex 1
        :type v: int
        :param w: Vertex 2
        :type w: int
        :param weight: Edge weight
        :type weight: float
        """

        self.frm = v
        self.to = w
        self.weight = weight

    def __eq__(self, other):
        """Compares equality.

        :param other: An edge to compare with
        :type other: Edge
        :return: True if equal, False otherwise
        :rtype: bool
        """

        return (self.frm == other.frm and self.to == other.to
                and self.weight == other.weight)

    def __ne__(self, other):
        """Compares non-equality.

        :param other: An edge to compare with
        :type other: Edge
        :return: True if not equal, False otherwise
        :rtype: bool
        """

        return (self.frm != other.frm or self.to != other.to
                or self.weight != other.weight)

    def __hash__(self):
        """Generates the object's hash value.

        :return: The object's hash
        :rtype: int
        """

        return hash(self.frm) ^ hash(self.to) ^ hash(self.weight)

    def __str__(self):
        """Generates a human readable representation of the edge.

        :return: The edge vertices and weight space delimited
        :rtype: str
        """

        return "{:d} {:d} {:.5f}".format(self.frm, self.to, self.weight)

    def __repr__(self):
        """Generates an official string representation of the edge with enough
        information to recreate it.

        :return: A string representation of the edge that can be eval'd
        :rtype: str
        """

        return "{}({:d}, {:d}, {:.5f})".format(type(self).__name__, self.frm,
                                               self.to, self.weight)


if __name__ == "__main__":

    import unittest


    class TestDirectedEdge(unittest.TestCase):

        def setUp(self):
            self.edge = DirectedEdge(1, 2, 4.1)

        def test_eq(self):
            self.assertEqual(DirectedEdge(1, 2, 4.1), self.edge)

        def test_ne(self):
            self.assertNotEqual(DirectedEdge(1, 2, 3.1), self.edge)
            self.assertNotEqual(DirectedEdge(2, 1, 4.1), self.edge)

        def test_hash(self):
            self.assertEqual(230584300921368583, hash(self.edge))

        def test_str(self):
            self.assertEqual("1 2 4.10000", str(self.edge))

        def test_repr(self):
            self.assertEqual("DirectedEdge(1, 2, 4.10000)", repr(self.edge))


    unittest.main()
