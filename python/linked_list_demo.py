# https://classroom.udacity.com/courses/ud513/lessons/7117335401/concepts/78875247320923


class Element:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, head: Element=None):
        self.head = head

    def append(self, new_element: Element):
        current = self.head

        # directly add element if head is None
        if self.head is None:
            self.head = new_element
            return

        # iterate thru next element
        while current.next:
            current = current.next
        current.next = new_element

    def get_position(self, position: int):
        """Get an element from a particular position.
        Assume the first position is "1".
        Return "None" if position is not in the list."""
        if position < 1:
            return None

        counter = 1
        current = self.head
        while current:
            if counter == position:
                return current
            current = current.next
            counter += 1
        return None

    def insert(self, new_element: Element, position: int):
        """Insert a new node at the given position.
        Assume the first position is "1".
        Inserting at position 3 means between
        the 2nd and 3rd elements."""
        if position < 1:
            print("can't insert element into position lesser than 1")
            return

        if position == 1:
            # swap the first element (head) with new element
            new_element.next = self.head
            self.head = new_element
            return

        counter = 1
        current = self.head
        while current and counter:
            # shift elements after position 1 step to right
            if counter == position - 1:
                new_element.next, current.next = current.next, new_element
            
            current = current.next
            counter += 1

    def delete(self, value):
        """Delete the first node with a given value."""
        current, prev = self.head, None
        while current.value != value and current.next:
            # shift elements after deleted element 1 step to left
            prev, current = current, current.next

        if current.value == value:
            if prev:
                prev.next = current.next
            else:
                self.head = current.next


#################
#
## Test cases

# Set up some Elements
e1 = Element(1)
e2 = Element(2)
e3 = Element(3)
e4 = Element(4)

# Start setting up a LinkedList
ll = LinkedList(e1)
ll.append(e2)
ll.append(e3)

# Test get_position
# Should print 3
print(ll.head.next.next.value, '→', ll.head.next.next.value == 3)

# Should also print 3
print(ll.get_position(3).value, '→', ll.get_position(3).value == 3)

# Test insert
ll.insert(e4, 3)
# Should print 4
print(ll.get_position(3).value, '→', ll.get_position(3).value == 4)

# Test delete
ll.delete(1)
# Should print 2
print(ll.get_position(1).value, '→', ll.get_position(1).value == 2)

# Should print 4
print(ll.get_position(2).value, '→', ll.get_position(2).value == 4)

# Should print 3
print(ll.get_position(3).value, '→', ll.get_position(3).value == 3)