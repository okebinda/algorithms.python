"""Sorting Algorithm: Quicksort"""

from random import shuffle


def quicksort(a):
    """Quicksort

    Time complexity: O(nlogn)
    Space complexity: O(logn)

    :param a: A list to be sorted
    :type a: list
    :return: A new sorted list
    :rtype: list
    """

    def partition(srt, start, end):
        """Partitions a list by placing the first item between two sub lists:
        lower ranked items on the left, higher ranked items on the right

        :param srt: The list being sorted
        :type srt: list
        :param start: The beginning index of the sub list to be partitioned
        :type start: int
        :param end: The ending index of the sub list to be partitioned
        :type end: int
        :return: The index of the partitioned item
        :rtype: int
        """

        follower = leader = start
        while leader < end:
            if srt[leader] < srt[end]:
                srt[follower], srt[leader] = srt[leader], srt[follower]
                follower += 1
            leader += 1
        srt[follower], srt[end] = srt[end], srt[follower]
        return follower

    def sort(srt, start, end):
        """Sorts a list recursively by placing one element at a time in order
        using the partition() function

        :param srt: The list being sorted
        :type srt: list
        :param start: The beginning index of the sub list to be sorted
        :type start: int
        :param end: The ending index of the sub list to be sorted
        :type end: int
        """

        if start >= end:
            return
        p = partition(srt, start, end)
        sort(srt, start, p-1)
        sort(srt, p+1, end)

    b = [*a]
    shuffle(b)
    sort(b, 0, len(b)-1)
    return b


if __name__ == "__main__":

    import unittest


    class TestQuicksort(unittest.TestCase):

        ordered = None
        shuffled = None

        def setUp(self):
            self.ordered = [x for x in range(20)]
            self.shuffled = [*self.ordered]
            while self.ordered == self.shuffled:
                shuffle(self.shuffled)

        def test_quicksort(self):
            self.assertEqual(self.ordered, quicksort(self.shuffled))
            self.assertNotEqual(self.ordered, self.shuffled)


    unittest.main()
