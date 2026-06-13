class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, data):
        new_node = StackNode(data)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if not self.head:
            raise IndexError
        data = self.head.data
        self.head = self.head.next
        return data

    def peek(self):
        if not self.head:
            return None
        return self.head.data

    def __str__(self):
        current = self.head
        result = []
        while current:
            result.append(str(current.data))
            current = current.next
        return "[" + ", ".join(result) + "]"