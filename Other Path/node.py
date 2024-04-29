class Node:
    def __init__(self, value):
        self.value = value
        self.children = []  
        self.level = 0
        
        
def preorder_traversal(root):
    if root is None:
        return

    if root.level == 0:
        print(root.value)
    else:
        print("." * root.level, root.value)

    for child in root.children:
        child.level = root.level + 1
        preorder_traversal(child)  # Recursively traverse each child node with increased level