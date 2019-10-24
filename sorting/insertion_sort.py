"""Sorting Algorithm: Insertion Sort"""


def insertion_sort(a):
    """Insertion Sort

    Time complexity: Between O(n) and O(n^2)
    Space complexity: O(1)

    :param a: A list to be sorted
    :type a: list
    :return: A new sorted list
    :rtype: list
    """

    b = [*a]
    for i in range(len(b)):
        temp = b[i]
        j = i - 1
        while j >= 0 and b[j] > temp:
            b[j+1] = b[j]
            j -= 1
        b[j+1] = temp
    return b


if __name__ == "__main__":

    import unittest
    from random import shuffle


    class TestInsertionSort(unittest.TestCase):

        ordered = None
        shuffled = None

        def setUp(self):
            self.ordered = [x for x in range(20)]
            self.shuffled = [*self.ordered]
            while self.ordered == self.shuffled:
                shuffle(self.shuffled)

        def test_insertion_sort(self):
            self.assertEqual(self.ordered, insertion_sort(self.shuffled))
            self.assertNotEqual(self.ordered, self.shuffled)


    unittest.main()
