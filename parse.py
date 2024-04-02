import screener



class Node:
    def __init__(self, terminal):
        self.terminal = terminal
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __str__(self):
        return self.terminal

    
def build_tree(terminal, num_children):
    if num_children == 0:
        return Node(terminal)
    
    node = Node(terminal)
    for i in range(num_children):
        child = build_tree(terminal, num_children - 1)
        node.add_child(child)
    
    return node

def read(terminal):
    pass

def parse(token_list):
    pass
    

# Expressions
def procedure_E():
    if token_list[0].content == 'let':
        read('let')
        procedure_D()
        read('in')
        procedure_E()
        build_tree('let', 2)
        
    elif token_list[0].content == 'fn':
        read('fn')
        procedure_Vb()                              # This should be once or more
        read('.')
        procedure_E()
        build_tree('lambda', 2)
        
    else:
        procedure_Ew()
        
def procedure_Ew():
    procedure_T()
    
    if token_list[0].content == 'where':
        read('where')
        procedure_Dr()
        build_tree('where', 2)
        
        
# Tuple Expressions
def procedure_T():
    procedure_Ta()
    
    while token_list[0].content == ',':
        read(',')
        procedure_Ta()
        build_tree('tau', 2)                       ## Not sure about this
        
# Not sure about this and other procedures with common prefixes on right
def procedure_Ta():
    procedure_Tc()
    
    while token_list[0].content == 'aug':
        read('aug')
        procedure_Ta()
        build_tree('aug', 2)
        
def procedure_Tc():
    procedure_B()
    
    if token_list[0].content == '->':
        read('->')
        procedure_Tc()
        read('|')
        procedure_Tc()
        
        build_tree('->', 3)
        
# Boolean Expressions
def procedure_B():
    procedure_Bt()
    
    if token_list[0].content == 'or':
        read('or')
        procedure_B()
        build_tree('or', 2)
        
def procedure_Bt():
    procedure_Bs()
    
    if token_list[0].content == '&':
        read('&')
        procedure_Bt()
        build_tree('&', 2)
        
def procedure_Bs():
    procedure_Bp()
    
    if token_list[0].content == 'not':
        read('not')
        procedure_Bp()
        build_tree('not', 1)
        
def procedure_Bp():
    procedure_A()
    
    if token_list[0].content in ['gr', '>', 'ge', '>=', 'ls', '<', 'le', '<=', 'eq', 'ne']:
        
        read(token_list[0].content)
        procedure_A()
        build_tree(token_list[0].content, 2)
        
# Arithmetic Expressions
def procedure_A():
    procedure_At()
    
    if token_list[0].content in ['-', '+']:
        read(token_list[0].content)
        procedure_A()                                  ## Something to handle here
        build_tree(token_list[0].content, 2)
        
def procedure_At():
    procedure_Af()
    
    if token_list[0].content in ['*', '/']:
        read(token_list[0].content)
        procedure_At()
        build_tree(token_list[0].content, 2)
        
def procedure_Af():
    procedure_Ap()
    
    if token_list[0].content == '**':
        read('**')
        procedure_Af()
        build_tree('**', 2)
        
def procedure_Ap():
    procedure_R()
    
    if token_list[0].content == '@':
        read('@')
        procedure_Ap()
        build_tree('@', 2)
        
# Rators and Rands
def procedure_R():
    if token_list[0].type == '<IDENTIFIER>':
        read(token_list[0].content)
        build_tree(token_list[0].content, 0)
        
    elif token_list[0].content == '(':
        read('(')
        procedure_E()
        read(')')
        
    
def procedure_Rn():
    if token_list[0].type in ['<IDENTIFIER>', '<INTEGER>', '<STRING>']:
        read(token_list[0].content)
        build_tree(token_list[0].content, 0)
        
    elif token_list[0].content in ['true', 'false', 'nil', 'dummy']:
        read(token_list[0].content)
        build_tree(token_list[0].content, 0)
        
    elif token_list[0].content == '(':
        read('(')
        procedure_E()
        read(')')
        
    else:
        raise SyntaxError
    
# Declarations
def procedure_D():
    procedure_Da()
    
    if token_list[0].content == 'within':
        read('within')
        procedure_D()
        build_tree('within', 2)
        
def procedure_Da():
    procedure_Dr()
    
    while token_list[0].content == 'and':
        read('and')
        procedure_Dr()
        build_tree('and', 2)
        
def procedure_Dr():
    if token_list[0].content == 'rec':
        read('rec')
        procedure_Db()
        build_tree('rec', 1)
        
    else:
        procedure_Db()
        
def procedure_Db():
    if token_list[0].content == '(':
        read('(')
        procedure_D()
        read(')')
        
    elif token_list[0].type == '<IDENTIFIER>':
        read(token_list[0].content)
        read('=')
        procedure_E()
        build_tree('=', 2)
        
    else:
        raise SyntaxError
    
# Value Bindings
def procedure_Vb():
    procedure_Vl()
    
    if token_list[0].content == 'within':
        read('within')
        procedure_Vb()
        build_tree('within', 2)
        
def procedure_Vl():
    read(token_list[0].content)
    
    if token_list[0].content == ',':
        read(',')
        procedure_Vl()
        build_tree(',', 2)        
        

        
file_name = input()

token_list = screener.screen(file_name)
