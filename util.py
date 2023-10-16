from queue import Queue
from collections import deque


class Node:
    """
    Represents a node in a search problem.
    """

    def _init_(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    """
    Represents a frontier for a depth-first search.
    """

    def _init_(self):
        self.frontier = deque()

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty.")
        else:
            node = self.frontier.pop()
            return node


class QueueFrontier:
    """
    Represents a frontier for a breadth-first search.
    """

    def _init_(self):
        self.frontier = Queue()

    def add(self, node):
        self.frontier.put(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier.queue)

    def empty(self):
        return self.frontier.empty()

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty.")
        else:
            node = self.frontier.get()
            return node