"""Sorting Algorithm: Heapsort"""


def heapsort(a):
    """Heapsort

        Time complexity: O(nlogn)
        Space complexity: O(1)

        :param a: A list to be sorted
        :type a: list
        :return: A new sorted list
        :rtype: list
        """

    def heapify(heap, n, i):
        """Creates a heap-ordered binary tree

        :param heap: A list to heap order
        :type heap: list
        :param n: Length of sub list to heapify
        :type n: int
        :param i: Index of element to heap order
        :type i: int
        """

        max = i
        l = i*2 + 1
        r = i*2 + 2
        if l < n and heap[i] < heap[l]:
            max = l
        if r < n and heap[max] < heap[r]:
            max = r
        if max != i:
            heap[i], heap[max] = heap[max], heap[i]
            heapify(heap, n, max)

    b = [*a]
    n = len(b)
    for i in range(n, -1, -1):
        heapify(b, n, i)
    for i in range(n-1, 0, -1):
        b[0], b[i] = b[i], b[0]
        heapify(b, i, 0)
    return b


if __name__ == "__main__":

    import unittest
    from random import shuffle


    class TestHeapsort(unittest.TestCase):

        ordered = None
        shuffled = None

        def setUp(self):
            self.ordered = [x for x in range(20)]
            self.shuffled = [*self.ordered]
            while self.ordered == self.shuffled:
                shuffle(self.shuffled)

        def test_heapsort(self):
            self.assertEqual(self.ordered, heapsort(self.shuffled))
            self.assertNotEqual(self.ordered, self.shuffled)


    unittest.main()
