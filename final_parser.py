from screener import screen

stack = []
pseudo_keywords = ["true", "false", "nil", "dummy"]
dic = {">": "gr", ">=": "ge", "<": "ls", "<=": "le", "==": "eq", "!=": "ne", "ge": "ge", "gr": "gr", "ls": "ls", "le": "le", "eq": "eq", "ne": "ne","+":"plus", "-":"neg"}

class Node:
    def __init__(self, content):
        self.type = None           ####### Problematic
        self.content = content
        self.line = -1
        self.children = []  
        self.siblings = []
        self.depth = 0
        
def print_tree(node):
    for i in range(node.depth):
        print(".", end="")
    print(str(node.content) + "\n")
    
    if len(node.children) > 0:
       for child in node.children:
            child.depth = node.depth + 1
            print_tree(child) 
            
    if len(node.siblings) > 0:
        for sibling in node.siblings:
            sibling.depth = node.depth
            print_tree(sibling)
            
def read(token):
    if token.type in ["IDENTIFIER", "INTEGER", "STRING"]:
        if token.type == "IDENTIFIER":
            leaf = Node("<ID:" + token.content + ">")
            stack.append(leaf)
            
        if token.type == "INTEGER":
            leaf = Node("<INT:" + str(token.content) + ">")
            stack.append(leaf)
            
        if token.type == "STRING":
            leaf = Node("<STR:" + token.content + ">")
            stack.append(leaf)
            
        if token.content in pseudo_keywords:
            leaf = Node(token.content)
            stack.append(leaf)
            
    #    print("Now reading: " + token.content)
    
    
def build_tree(token, num_children):
    # Need some code to ensure correnct operation = a print function
    
    node = Node(token.content)
    node.content = None
    node.line = -1
    node.child = None
    node.siblings = None
    
    for i in range(num_children):
        child = stack [-1]
        stack.pop()
        
        if node.child != None:        ## is not
            child.siblings = node.child
            
        node.child = child
        node.line = child.line
    
    # print_tree(node)   
    stack.append(node)
    
    for node in stack:
        print(node.content)
        
        
def procedure_E():
    if tokens[0].content == "let":
        read(tokens[0])
        tokens.pop(0)
        procedure_D()
        
        if tokens[0].content == "in":
            read(tokens[0])
            tokens.pop(0)
            procedure_E()
            build_tree("let", 2)
            
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Expecter 'in' but got " + str(tokens[0].content))
            exit(1)
            
    elif tokens[0].content == "fn":
        n = 0
        read(tokens[0])
        
        while tokens[0].type == "IDENTIFIER" or tokens[0].content == "(":
            procedure_Vb()
            n += 1
            
        if n == 0:
            print("Syntax error in line " + str(tokens[0].line) + ": Expected at least one Vb but got none")
            exit(1)
            
        if tokens[0].content == ".":
            read(tokens[0])
            tokens.pop(0)
            procedure_E()
            build_tree("lambda", n+1)
            
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Expected '.' but got " + str(tokens[0].content))
            exit(1)
            
    else:
        procedure_Ew()
        
def procedure_Ew():
    procedure_T()
    
    if tokens[0].content in ["where", "within"]:  # within was just suggested
        read(tokens[0])
        tokens.pop(0)
        procedure_Dr()
        build_tree("where", 2)
        
def procedure_T():
    procedure_Ta()
    
    n = 0
    
    while tokens[0].content in ",":
        read(tokens[0])
        tokens.pop(0)
        procedure_Ta()
        n += 1
        
    if n > 0:
        build_tree("tau", n+1)
    else:
        # print('T -> Ta')
        pass
    
def procedure_Ta():
    procedure_Tc()
    
    while tokens[0].content == "aug":
        read(tokens[0])
        tokens.pop(0)
        procedure_Tc()
        build_tree("aug", 2)
        
def procedure_Tc():
    procedure_B()
    
    while tokens[0].content == "->":
        read(tokens[0])
        tokens.pop(0)
        procedure_Tc()
        
        if tokens[0].content == "|":
            read(tokens[0])
            tokens.pop(0)
            procedure_Tc()
            build_tree("->", 3) 
            
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Expected '|' but got " + str(tokens[0].content))
            exit(1)
            
def procedure_B():
    procedure_Bt()
    
    while tokens[0].content == "or":
        read(tokens[0])
        tokens.pop(0)
        procedure_Bt()
        build_tree("or", 2)
        
def procedure_Bt():
    procedure_Bs()
    
    while tokens[0].content == "&":
        read(tokens[0])
        tokens.pop(0)
        procedure_Bs()
        build_tree("&", 2)
        
def procedure_Bs():
    if tokens[0].content == "not":
        read(tokens[0])
        tokens.pop(0)
        procedure_Bp()
        build_tree("not", 1)
        
    else:
        procedure_Bp()
        
def procedure_Bp():
    procedure_A()
    
    if tokens[0].content in [">", ">=", "<", "<=", "gr", "ge", "ls", "le", "eq", "ne"]:
        read(tokens[0])
        tokens.pop(0)
        procedure_A()
        build_tree(dic[tokens[0].content], 2)
        
def procedure_A():
    if tokens[0].content in ["+", "-"]:
        read(tokens[0])
        tokens.pop(0)
        build_tree(dic[tokens[0].content], 1)
        
    else:
        procedure_At()
        
    while tokens[0].content in ["+", "-"]:
        if tokens[0].content == "+":
            read(tokens[0])
            tokens.pop(0)
            procedure_At()
            build_tree("plus", 2)
        else:
            read(tokens[0])
            tokens.pop(0)
            procedure_At()
            build_tree("neg", 1)
            
def procedure_At():
    procedure_Af()
    
    while tokens[0].content in "*" or tokens[0].content == "/":
        if tokens[0].content == "*":
            read(tokens[0])
            tokens.pop(0)
            procedure_Af()
            build_tree("*", 2)
        else:
            read(tokens[0])
            tokens.pop(0)
            procedure_Af()
            build_tree("/", 2)
            
def procedure_Af(): 
    procedure_Ap()
    
    while tokens[0].content == "**":
        read(tokens[0])
        tokens.pop(0)
        procedure_Af()
        build_tree("**", 2)
        
def procedure_Ap():
    procedure_R()
    
    while tokens[0].content == "@":
            read(tokens[0])
            tokens.pop(0)
            procedure_R()
            build_tree("@", 2)
            
def procedure_R():
    procedure_Rn()
    
    while tokens[0].type in ["IDENTIFIER", "INTEGER", "STRING", "KEYWORD"] or tokens[0].content == "(" or tokens[0].content in pseudo_keywords:
        
        procedure_Rn()
        build_tree("gamma", 2)

def procedure_Rn():
    if tokens[0].type in ["IDENTIFIER", "INTEGER", "STRING"]:
        read(tokens[0])
        tokens.pop(0)
        
    elif tokens[0].content == "(":
        read(tokens[0])
        tokens.pop(0)
        procedure_E()
        
        if tokens[0].content == ")":
            read(tokens[0])
            tokens.pop(0)
            
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Expected ')' but got " + str(tokens[0].content))
            exit(1)
            
    else:
        if tokens[0].content in pseudo_keywords:
            read(tokens[0])
            tokens.pop(0)
            
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Expected a keyword but got " + str(tokens[0].content))
            exit(1)
            
def procedure_D():
    print("D")
    procedure_Da()
    
    if tokens[0].content == "within":
        read(tokens[0])
        tokens.pop(0)
        procedure_D()
        build_tree("within", 2)
        
def procedure_Da():
    procedure_Dr()
    
    n = 0
    
    while tokens[0].content == "and":
        n += 1
        read(tokens[0])
        tokens.pop(0)
        procedure_Dr()
        
    if n > 0:
        build_tree("and", n+1)
        
def procedure_Dr():                             # Not sure
    if tokens[0].content == "rec":
        read(tokens[0])
        tokens.pop(0)
        procedure_Db()
        build_tree("rec", 1)
        
    else:
        procedure_Db()
        
def procedure_Db():
    if tokens[0].content == "(":
        read(tokens[0])
        tokens.pop(0)
        procedure_D()
        
        if tokens[0].content == ")":
            read(tokens[0])
            tokens.pop(0)
            build_tree("()", 1)
            
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Expected ')' but got " + str(tokens[0].content))
            exit(1)
            
    elif tokens[0].type == "IDENTIFIER":
        read(tokens[0])
        tokens.pop(0)
        
        if tokens[0].content == ",":
            read(tokens[0])
            tokens.pop(0)
            procedure_Vb()
            
            if tokens[0].content == "=":
                build_tree(",", 2)
                read(tokens[0])
                tokens.pop(0)
                procedure_E()
                build_tree("=", 2)
                
            else:
                print("Syntax error in line " + str(tokens[0].line) + ": Expected '=' but got " + str(tokens[0].content))
                exit(1)
                
        else:
            if tokens[0].content == "=":
                read(tokens[0])
                tokens.pop(0)
                procedure_E()
                build_tree("=", 2)
                
            else:
                n = 0
                
                while tokens[0].type in ["IDENTIFIER","KEYWORD"] or tokens[0].content == "(": # not sure
                    procedure_Vb()
                    n += 1
                    
                if n == 0:
                    print("Syntax error in line " + str(tokens[0].line) + ": Expected at least one Vb but got none")
                    exit(1)
                    
                if tokens[0].content == "=":
                    read(tokens[0])
                    tokens.pop(0)
                    procedure_E()
                    build_tree("function_form", n+2)
                    
                else:
                    print("Syntax error in line " + str(tokens[0].line) + ": Expected '=' but got " + str(tokens[0].content))
                    exit(1)
                    
def procedure_Vb():
    if tokens[0].type == "IDENTIFIER": # not sure we need keywords too
        read(tokens[0])
        tokens.pop(0)
        
    elif tokens[0].content == "(":
        read(tokens[0])
        tokens.pop(0)
        
        if tokens[0].content == ")":
            read(tokens[0])
            tokens.pop(0)
            
            if tokens[0].content == ")":
                build_tree("()", 0)
                read(tokens[0])
                tokens.pop(0)
                
            else:
                procedure_Vl()
                
                if tokens[0].content == ")":
                    #read(tokens[0])
                    #tokens.pop(0)
                    pass
                    
                else:
                    print("Syntax error in line " + str(tokens[0].line) + ": Expected ')' but got " + str(tokens[0].content))
                    exit(1)
                    
        read(tokens[0])
        tokens.pop(0)
        
    else:
        print("Syntax error in line " + str(tokens[0].line) + ": Expected an identifier or '(' but got " + str(tokens[0].content))
        exit(1)
        
def procedure_Vl():
    if tokens[0].type not in ["IDENTIFIER", "KEYWORD"]:
        print("Syntax error in line " + str(tokens[0].line) + ": Expected an identifier or keyword but got " + str(tokens[0].content))
        exit(1)
        
    else:
        read(tokens[0])
        tokens.pop(0)
        
        n = 0
        
        while tokens[0].content == ",":
            read(tokens[0])
            tokens.pop(0)
            if tokens[0].type not in ["IDENTIFIER", "KEYWORD"]:
                print("Syntax error in line " + str(tokens[0].line) + ": Expected an identifier or keyword but got " + str(tokens[0].content))
                exit(1)
                
            else:
                read(tokens[0])
                tokens.pop(0)
                n += 1
                
        if n > 0:
            build_tree(",", n+1)
    
file_name = input()
tokens = screen(file_name)
procedure_E()
print_tree(stack[0])