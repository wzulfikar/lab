> Fri, 27 Apr 2018 at 5:48:07 MYT

### Lesson 2: List-Based Collection

1. collection: group of things
- list-based collection: collection with few additional rules/constraints, ie. order
- linked list store reference for next element
- adding element into linked list is easy because it's just a matter of changing the reference, hence the constant time (unlike adding element in array where it requires to shift all subsequent elements)
- doubly linked list is just linked list, with added reference to its previous element (instead of just next element)
- stacks: put element on top of each other → **LIFO** (last in first out)
- stacks can be very useful when we only care about the most recent element
- specific term used in stacks:
    - `push`: adding element into stack
    - `pop`: take element from stack
- queue: kind-of opposite of stack
- structure of queue: **FIFO** (first in first out)
- common terms used in queue:
    - `enqueue`: adding element to tail
    - `dequeue`: remove head element
    - `peek`: looking at head element without actually removing it
- **deque**: double-ended queue; a queue that can be queued/dequeued from both direction
- **priority queue**: queue with added constraint (priority point). element with highest priority will be taken first when doing dequeue operation (doesn't follow FIFO structure). if element has same priority, the oldest element will be taken.
