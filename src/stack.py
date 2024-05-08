class Stack:
    def __init__(self):
        self.stack = []
        
    # The following three methods are implemented to make the class iterable and indexable
    def __getitem__(self, index):
        return self.stack[index]
    
    def __setitem__(self, index, value):
        self.stack[index] = value
        
    def __reversed__(self):
        return reversed(self.stack)

    # The following function lets you push an item onto the stack.
    def push(self, item):
        self.stack.append(item)

    # The following function lets you pop an item from the stack.
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            print("Stack is empty.")
            exit(1)

    # The following function lets you check whether the stack is empty.
    def is_empty(self):
        return len(self.stack) == 0