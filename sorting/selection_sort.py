"""Sorting Algorithm: Selection Sort"""


def selection_sort(a):
    """Selection Sort

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
        min = i
        for j in range(i+1, n):
            if b[j] < b[min]:
                min = j
        b[i], b[min] = b[min], b[i]
    return b


if __name__ == "__main__":

    import unittest
    from random import shuffle


    class TestSelectionSort(unittest.TestCase):

        ordered = None
        shuffled = None

        def setUp(self):
            self.ordered = [x for x in range(20)]
            self.shuffled = [*self.ordered]
            while self.ordered == self.shuffled:
                shuffle(self.shuffled)

        def test_selection_sort(self):
            self.assertEqual(self.ordered, selection_sort(self.shuffled))
            self.assertNotEqual(self.ordered, self.shuffled)


    unittest.main()
