"""Learning data structures in python.
https://www.youtube.com/playlist?list=PL5tcWHG-UPH112e7AN7C-fwDVPVrt0wpV
"""

# ==============================================================================
# Stacks
# option 1

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def is_empty(self):
        return self.items == []

    def get_stack(self):
        return self.items

    def peek(self):
        if not self.is_empty():
            return self.items[-1]


s = Stack()
s.push('a')
s.push('b')
print(s.get_stack())
s.pop()
print(s.get_stack())
print(s.peek())

#applying stack in practice
def is_match(p1, p2):
    return True if p1+p2 in ['()', '[]', '{}'] else False


def is_paren_balanced(paren_string):
    s = Stack()
    is_balanced = True
    index = 0
    while index < len(paren_string) and is_balanced:
        paren = paren_string[index]
        if paren in "{[(":
            s.push(paren)
        else:
            if s.is_empty():
                is_balanced = False
            else:
                top = s.pop()
                if not is_match(top, paren):
                    is_balanced = False
        index += 1
    return s.is_empty() and is_balanced

print(is_paren_balanced('()'))


# option 2
# the differences between a list and a deque is that a list is a continuous chunk of memory
# while a deque is a "double-linked list".
# Each entry is stored in its own memoery address
# and has a reference to BOTH the next and previous entry in the list
# this allows to easily add nodes to both ends of the list
# this means that: 1)indexing (eg L[1]) is slower than a list
# but 2)appending / popping is quicker (no need to create a big chunk of memory)
# to be precise, appending/ popping is constant time
# this is why this is a good choice for a stack data structure
# ADDED BONUS: .pop and .append are atomic (thread-safe) for deques


from collections import deque
mystack = deque()
mystack.append('a')
mystack.append('b')
print(mystack)
mystack.pop()
print(mystack)
mystack.pop()
print(mystack)


# option 3 - lifo queue
# this is designed to be fully thread-safe
# however it's slower
# general rule of thumb - use deque to implement a stack, unless you're doing threading


from queue import LifoQueue
mystack = LifoQueue()
mystack.put(1)
mystack.put(2)
mystack.put(3)
print(mystack)
print(mystack.get()) #3
print(mystack.get()) #2
print(mystack.get()) #1
# print(mystack.get()) #nothing (throws a silent error, as in YES, it stops execution)
# print(mystack.get()) #nothing (throws a silent error, as in YES, it stops execution)


print("-------------------- Queues --------------------")
# ==============================================================================
# Stacks
# 1 - lists
# you can use lists
# but same problem as with stacks - not very efficient
# this is because inserting an element into a list requires shifting the entire thing by 1
q = []
q.append('eat')
q.append('code')
q.append('repeat')
print(q)
q.pop(0) # NOTE: we're using 0 here, not just ()

# 2 - deque
# adding / removing elements from EITHER END = O(1)
# poor performance when randomly accessing elements
# Dan Bader also said - great default choice to implement a stack / queue
from collections import deque
q = deque()
q.append('eat')
q.append('sleep')
q.append('code')
print(q)
print(q.popleft())
print(q)

# 3 - queue class
# supports multiple concurrent producers and consumers
from queue import Queue
q = Queue()
q.put('eat')
q.put('sleep')
q.put('code')

print(q)
q.get()