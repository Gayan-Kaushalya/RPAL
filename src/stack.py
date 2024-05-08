class Stack:
    def __init__(self):
        self.stack = []
        
    def __getitem__(self, index):
        return self.stack[index]
    
    def __setitem__(self, index, value):
        self.stack[index] = value
        
    def __reversed__(self):
        return reversed(self.stack)

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            print("Stack is empty.")
            exit(1)

    def is_empty(self):
        return len(self.stack) == 0