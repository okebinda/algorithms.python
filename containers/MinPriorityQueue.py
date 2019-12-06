"""Container: Minimum Priority Queue"""


class MinPriorityQueue:
    """A minimum priority queue using a heap-ordered list."""

    def __init__(self):
        """MinPriorityQueue constructor."""

        self._pq = [None]
        self._values = [None]
        self._n = 0

    def __len__(self):
        """Reports number of elements in the priority queue

        :return: Length of priority queue
        :rtype: int
        """

        return self._n

    def __bool__(self):
        """Reports if priority queue contains any elements

        :return: False if empty, True otherwise
        :rtype: bool
        """

        return self._n > 0

    def enqueue(self, value, i):
        """Adds an element to the priority queue, re-ordering the heap as
        necessary.

        :param value: Any data value
        :param i: The priority of the item
        :type i: numeric
        """
        
        self._pq.append(i)
        self._values.append(value)
        self._n += 1
        self._swim(self._n)

    def dequeue(self):
        """Removes the first element in the priority queue and returns it,
        re-ordering the heap as necessary.

        :return: Value of element at the front of the queue
        :raises: Exception
        """

        if not bool(self):
            raise Exception("{} is empty.".format(type(self).__name__))

        value = self._values[1]
        self._pq[1], self._pq[self._n] = self._pq[self._n], self._pq[1]
        self._values[1], self._values[self._n] = (self._values[self._n],
                                                  self._values[1])
        self._n -= 1
        del self._pq[self._n + 1]
        del self._values[self._n + 1]
        self._sink(1)
        return value

    def peek(self):
        """Reports the value of the first element in the priority queue without
        removing it.

        :return: Value of element at the front of the queue
        :raises: Exception
        """

        if not bool(self):
            raise Exception("{} is empty.".format(type(self).__name__))
        return self._values[1]

    def update_priority(self, value, i):
        """Modifies the priority associated with given value.

        :param value: Value of element to change priority of
        :param i: New priority
        :param i: numeric
        """

        index = self._values.index(value)
        self._pq[index] = i

        # swap with last and reorder
        self._pq[index], self._pq[self._n] = self._pq[self._n], self._pq[index]
        self._values[index], self._values[self._n] = (self._values[self._n],
                                                      self._values[index])
        self._swim(self._n)

    def __contains__(self, value):
        """Determines if a value is in the priority queue.

        :param value: Value of element to search for
        :return: True if value is in priority queue, otherwise False
        :rtype: bool
        """

        return value in self._values

    def _swim(self, k):
        """Re-orders the heap from the bottom up.

        :param k: The heap index to start re-ordering from
        :type k: int
        """

        while k > 1 and self._pq[k//2] > self._pq[k]:
            self._pq[k//2], self._pq[k] = self._pq[k], self._pq[k//2]
            self._values[k//2], self._values[k] = (self._values[k],
                                                   self._values[k//2])
            k //= 2

    def _sink(self, k):
        """Re-orders the heap from the top down.

        :param k: The heap index to start re-ordering from
        :type k: int
        """

        while k * 2 <= self._n:
            j = k * 2
            if j < self._n and self._pq[j] > self._pq[j+1]:
                j += 1
            if not self._pq[k] > self._pq[j]:
                break
            self._pq[k], self._pq[j] = self._pq[j], self._pq[k]
            self._values[k], self._values[j] = self._values[j], self._values[k]
            k = j


if __name__ == "__main__":

    import unittest


    class TestMinPriorityQueue(unittest.TestCase):

        def setUp(self):
            self.pq = MinPriorityQueue()
            self.pq.enqueue('c', 3)
            self.pq.enqueue('d', 4)
            self.pq.enqueue('b', 2)
            self.pq.enqueue('g', 7)
            self.pq.enqueue('f', 6)

        def test_len(self):
            self.assertEqual(5, len(self.pq))
            self.assertEqual(0, len(MinPriorityQueue()))

        def test_bool(self):
            self.assertTrue(bool(self.pq))
            self.assertFalse(bool(MinPriorityQueue()))

        def test_enqueue(self):
            self.pq.enqueue('a', 1)
            self.assertEqual(6, len(self.pq))
            self.assertEqual("a", self.pq.peek())

            self.pq.enqueue('e', 5)
            self.assertEqual(7, len(self.pq))
            self.assertEqual("a", self.pq.peek())

        def test_dequeue(self):
            self.assertEqual("b", self.pq.dequeue())
            self.assertEqual(4, len(self.pq))

            self.assertEqual("c", self.pq.dequeue())
            self.assertEqual(3, len(self.pq))

            self.assertEqual("d", self.pq.dequeue())
            self.assertEqual(2, len(self.pq))

            self.assertEqual("f", self.pq.dequeue())
            self.assertEqual(1, len(self.pq))

            self.assertEqual("g", self.pq.dequeue())
            self.assertEqual(0, len(self.pq))

            self.assertRaises(Exception, self.pq.dequeue)

        def test_peek(self):
            self.assertEqual("b", self.pq.peek())
            self.assertRaises(Exception, MinPriorityQueue().peek)

        def test_update_priority(self):
            self.pq.update_priority('d', 1)
            self.assertEqual("d", self.pq.peek())
            self.assertEqual(5, len(self.pq))

            self.pq.update_priority('g', 5)
            self.assertEqual("d", self.pq.peek())
            self.assertEqual(5, len(self.pq))

            self.pq.update_priority('c', 0)
            self.assertEqual("c", self.pq.peek())
            self.assertEqual(5, len(self.pq))

            self.assertRaises(ValueError, self.pq.update_priority, 'z', 3)

        def test_contains(self):
            self.assertTrue('b' in self.pq)
            self.assertFalse('z' in self.pq)


    unittest.main()
