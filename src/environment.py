class Environment(object):
    def __init__(self, number, parent):
        self.name = "e_" + str(number)
        self.variables = {}
        self.children = []
        self.parent = parent
        
    def add_child(self, child):
        self.children.append(child)
        child.variables.update(self.variables)
        
    def add_variable(self, key, value):
        self.variables[key] = value