"""Container: Queue"""

from collections.abc import Iterable, Sized


class Queue(Iterable, Sized):
    """A FIFO (First In First Out) data structure implemented as a singly
    linked list"""

    class _Node:
        """A data node in the queue"""

        __slots__ = 'value', 'next'

        def __init__(self, value):
            """Node constructor

            :param value: Any data value
            """

            self.value = value
            self.next = None

    def __init__(self):
        """Queue constructor"""

        self._head = None
        self._tail = None
        self._cursor = None
        self._n = 0

    def __len__(self):
        """Reports number of elements in the queue

        :return: Length of queue
        :rtype: int
        """

        return self._n

    def __bool__(self):
        """Reports if queue contains any elements

        :return: False if empty, True otherwise
        :rtype: bool
        """

        return self._n > 0


    def enqueue(self, value):
        """Adds an element to the end of the queue

        :param value: Any data value
        """

        new_tail = self._Node(value)
        if bool(self):
            self._tail.next = new_tail
        else:
            self._head = new_tail
        self._tail = new_tail
        self._n += 1

    def dequeue(self):
        """Removes the first element in the queue and returns it

        :return: Value of element at the front of the queue
        :raises: Exception
        """

        if not bool(self):
            raise Exception("Queue is empty.")
        prev_head = self._head
        self._head = self._head.next
        prev_head.next = None
        self._n -= 1
        if not bool(self):
            self._tail = None
        return prev_head.value

    def peek(self):
        """Reports the value of the first element in the queue without removing
        it.

        :return: Value of element at the front of the queue
        :raises: Exception
        """

        if not bool(self):
            raise Exception("Queue is empty.")
        return self._head.value

    def __iter__(self):
        """Iterates over the queue, front-to-back

        :return: Queue
        """

        self._cursor = self._head
        return self

    def __next__(self):
        """Helps __iter__() to iterate

        :raises: StopIteration
        """

        if self._cursor is None:
            raise StopIteration
        value = self._cursor.value
        self._cursor = self._cursor.next
        return value


if __name__ == "__main__":

    import unittest


    class TestQueue(unittest.TestCase):

        def setUp(self):
            self.queue = Queue()
            self.queue.enqueue("m")
            self.queue.enqueue("c")
            self.queue.enqueue("s")
            self.queue.enqueue("t")
            self.queue.enqueue("b")
            self.queue.enqueue("y")

        def test_len(self):
            self.assertEqual(6, len(self.queue))
            self.assertEqual(0, len(Queue()))

        def test_bool(self):
            self.assertTrue(bool(self.queue))
            self.assertFalse(bool(Queue()))

        def test_enqueue(self):
            self.queue.enqueue("a")
            self.assertEqual(7, len(self.queue))

        def test_dequeue(self):
            self.assertEqual("m", self.queue.dequeue())
            self.assertEqual(5, len(self.queue))

            self.assertEqual("c", self.queue.dequeue())
            self.assertEqual(4, len(self.queue))

            self.assertEqual("s", self.queue.dequeue())
            self.assertEqual(3, len(self.queue))

            self.assertEqual("t", self.queue.dequeue())
            self.assertEqual(2, len(self.queue))

            self.assertEqual("b", self.queue.dequeue())
            self.assertEqual(1, len(self.queue))

            self.assertEqual("y", self.queue.dequeue())
            self.assertEqual(0, len(self.queue))

            self.assertRaises(Exception, self.queue.dequeue)
            self.assertRaises(Exception, Queue().dequeue)

        def test_peek(self):
            self.assertEqual('m', self.queue.peek())
            self.assertRaises(Exception, Queue().peek)

        def test_iter(self):
            letters = ['m', 'c', 's', 't', 'b', 'y']
            self.assertEqual(letters, list(self.queue))
            self.assertEqual(letters, [x for x in self.queue])
            self.assertEqual(letters, [*self.queue])

            self.assertEqual([], list(Queue()))


    unittest.main()
