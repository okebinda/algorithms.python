"""Sorting Algorithm: Shellsort"""


def shellsort(a):
    """Shellsort

    Time complexity: Between O(nlogn) and O(nlog^2n) ?
    Space complexity: O(1)

    :param a: A list to be sorted
    :type a: list
    :return: A new sorted list
    :rtype: list
    """

    b = [*a]
    n = len(b)
    gap = n // 2
    while gap > 0:
        for i in range(n):
            temp = b[i]
            j = i
            while j >= gap and b[j-gap] > temp:
                b[j] = b[j-gap]
                j -= gap
            b[j] = temp
        gap //= 2
    return b


if __name__ == "__main__":

    import unittest
    from random import shuffle


    class TestShellsort(unittest.TestCase):

        ordered = None
        shuffled = None

        def setUp(self):
            self.ordered = [x for x in range(20)]
            self.shuffled = [*self.ordered]
            while self.ordered == self.shuffled:
                shuffle(self.shuffled)

        def test_shellsort(self):
            self.assertEqual(self.ordered, shellsort(self.shuffled))
            self.assertNotEqual(self.ordered, self.shuffled)


    unittest.main()
