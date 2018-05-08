class Queue:
    def __init__(self, head=None):
        """implement queue by wrapping python built-in array"""
        self.storage = [head]

    def enqueue(self, new_element):
        self.storage.append(new_element)

    def peek(self):
        return self.storage[0]

    def dequeue(self):
        return self.storage.pop(0)

# Setup
q = Queue(1)
q.enqueue(2)
q.enqueue(3)

# Test peek
# Should be 1
print(q.peek(), 'should be', 1)

# Test dequeue
# Should be 1
print(q.dequeue(), 'should be', 1)

# Test enqueue
q.enqueue(4)
# Should be 2
print(q.dequeue(), 'should be', 2)
# Should be 3
print(q.dequeue(), 'should be', 3)
# Should be 4
print(q.dequeue(), 'should be', 4)
q.enqueue(5)
# Should be 5
print(q.peek(), 'should be', 5)