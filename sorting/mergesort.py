"""Sorting Algorithm: Mergesort"""


def mergesort(a):
    """Mergesort

    Time complexity: O(nlogn)
    Space complexity: O(n)

    :param a: A list to be sorted
    :type a: list
    :return: A new sorted list
    :rtype: list
    """

    b = [*a]
    n = len(b)
    if n <= 1:
        return b
    mid = n // 2
    left, right = mergesort(b[:mid]), mergesort(b[mid:])
    return _merge(left, right, b)


def _merge(left, right, merged):
    """Sorts a list by merging ordered sub lists

    :param left: The left-half slice of merged
    :type left: list
    :param right: The right-half slice of merged
    :type right: list
    :param merged: The list being merged
    :type merged: list
    :return: The merged list
    :rtype: list
    """

    left_cursor, right_cursor = 0, 0
    while left_cursor < len(left) and right_cursor < len(right):
        if left[left_cursor] <= right[right_cursor]:
            merged[left_cursor + right_cursor] = left[left_cursor]
            left_cursor += 1
        else:
            merged[left_cursor + right_cursor] = right[right_cursor]
            right_cursor += 1
    for left_cursor in range(left_cursor, len(left)):
        merged[left_cursor + right_cursor] = left[left_cursor]
    for right_cursor in range(right_cursor, len(right)):
        merged[left_cursor + right_cursor] = right[right_cursor]
    return merged


if __name__ == "__main__":

    import unittest
    from random import shuffle


    class TestMergesort(unittest.TestCase):

        def setUp(self):
            self.ordered = [x for x in range(20)]
            self.shuffled = [*self.ordered]
            while self.ordered == self.shuffled:
                shuffle(self.shuffled)

        def test_mergesort(self):
            self.assertEqual(self.ordered, mergesort(self.shuffled))
            self.assertNotEqual(self.ordered, self.shuffled)


    unittest.main()
