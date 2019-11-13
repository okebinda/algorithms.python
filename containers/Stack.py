"""Container: Stack"""


class Stack:
    """A LIFO (Last In First Out) data structure implemented as a singly
    linked list"""

    class _Node:
        """A data node in the stack"""

        __slots__ = 'value', 'next'

        def __init__(self, value, next):
            """Node constructor

            :param value: Any data value
            :param next: The next node in the stack
            :type next: _Node
            """

            self.value = value
            self.next = next

    def __init__(self):
        """Stack constructor"""

        self._head = None
        self._cursor = None
        self._n = 0

    def __len__(self):
        """Reports number of elements on the stack

        :return: Length of stack
        :rtype: int
        """

        return self._n

    def __bool__(self):
        """Reports if stack contains any elements

        :return: False if empty, True otherwise
        :rtype: bool
        """

        return self._n > 0

    def push(self, value):
        """Adds an element to the top of the stack

        :param value: Any data value
        """

        self._head = self._Node(value, self._head)
        self._n += 1

    def pop(self):
        """Removes the top element from the stack and returns it

        :return: Value of element on top of the stack
        :raises: Exception
        """

        if not bool(self):
            raise Exception("Stack is empty.")
        prev_head = self._head
        self._head = self._head.next
        prev_head.next = None
        self._n -= 1
        return prev_head.value

    def __iter__(self):
        """Iterates over the stack, top-to-bottom"""

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


    class TestStack(unittest.TestCase):

        def setUp(self):
            self.stack = Stack()
            self.stack.push("m")
            self.stack.push("c")
            self.stack.push("s")
            self.stack.push("t")
            self.stack.push("b")
            self.stack.push("y")

        def test_len(self):
            self.assertEqual(6, len(self.stack))
            self.assertEqual(0, len(Stack()))

        def test_bool(self):
            self.assertTrue(bool(self.stack))
            self.assertFalse(bool(Stack()))

        def test_push(self):
            self.stack.push("a")
            self.assertEqual(7, len(self.stack))

        def test_pop(self):
            self.assertEqual("y", self.stack.pop())
            self.assertEqual(5, len(self.stack))

            self.assertEqual("b", self.stack.pop())
            self.assertEqual(4, len(self.stack))

            self.assertEqual("t", self.stack.pop())
            self.assertEqual(3, len(self.stack))

            self.assertEqual("s", self.stack.pop())
            self.assertEqual(2, len(self.stack))

            self.assertEqual("c", self.stack.pop())
            self.assertEqual(1, len(self.stack))

            self.assertEqual("m", self.stack.pop())
            self.assertEqual(0, len(self.stack))

            self.assertRaises(Exception, self.stack.pop)
            self.assertRaises(Exception, Stack().pop)

        def test_iter(self):
            letters = ['y', 'b', 't', 's', 'c', 'm']
            self.assertEqual(letters, list(self.stack))
            self.assertEqual(letters, [x for x in self.stack])
            self.assertEqual(letters, [*self.stack])

            self.assertEqual([], list(Stack()))


    unittest.main()
