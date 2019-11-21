"""Graphs: Abstract Graph Base Class"""

from abc import ABC, abstractmethod
from collections.abc import Collection


class Graph(ABC, Collection):
    """An abstract base class for graphs."""

    @abstractmethod
    def size(self):
        """Reports the number of edges in the graph.

        :return: Number of edges in the graph
        :rtype: int
        """
        pass

    @abstractmethod
    def order(self):
        """Reports the number of vertices in the graph.

        :return: Number of vertices in the graph
        :rtype: int
        """
        pass

    @abstractmethod
    def add_edge(self, v, w):
        """Creates an edge between two vertices.

        :param v: Vertex 1
        :type v: int
        :param w: Vertex 2
        :type w: int
        """
        pass

    @abstractmethod
    def adj(self, v):
        """Retrieves the adjacency list for a vertex.

        :param v: Vertex
        :type v: int
        :return: The adjacency list of vertex v
        :rtype: list
        """
        pass
