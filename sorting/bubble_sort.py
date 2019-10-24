"""Sorting Algorithm: Bubble Sort"""


def bubble_sort(a):
    """Bubble Sort

    Time complexity: O(n^2)
    Space complexity: O(1)

    :param a: A list to be sorted
    :type a: list
    :return: A new sorted list
    :rtype: list
    """

    b = [*a]
    n = len(b)
    for i in range(n):
        for j in range(n-i-1):
            if b[j] > b[j+1]:
                b[j], b[j+1] = b[j+1], b[j]
    return b


if __name__ == "__main__":

    import unittest
    from random import shuffle


    class TestBubbleSort(unittest.TestCase):

        ordered = None
        shuffled = None

        def setUp(self):
            self.ordered = [x for x in range(20)]
            self.shuffled = [*self.ordered]
            while self.ordered == self.shuffled:
                shuffle(self.shuffled)

        def test_bubble_sort(self):
            self.assertEqual(self.ordered, bubble_sort(self.shuffled))
            self.assertNotEqual(self.ordered, self.shuffled)


    unittest.main()
