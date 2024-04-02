from screener import screen

stack = []
p = None

class Node(content, left_child=None, right_child=None):
    def __init__(self, content, left_child=None, right_child=None):
        self.content = content
        self.left_child = left_child
        self.right_child = right_child
    

'''
class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []
'''

def parse_program(tokens):
    # Parse the program starting from the root rule
    return parse_E(tokens)

def parse_E(tokens):
    if tokens and tokens[0].content == 'let':  
        tokens.pop(0)  
        parse_D(tokens)
        if tokens and tokens[0].content == 'in':
            tokens.pop(0) 
            parse_E(tokens) 
            
            build_tree('let', 2)      # Where do we create the node for 'in'?
            print("E -> let D in E")
            
        else:
            return SyntaxError
            # print("Syntax Error in line {token[0].line}. Expected 'in' but got {tokens[0].content}")
        
    elif tokens and tokens[0].content == 'fn':
        tokens.pop(0) 
        while True:
            parse_Vb(tokens)
            if not tokens or (tokens[0].content != '(' and tokens[0].type != '<IDENTIFIER>'):  # Not sure about this condition
                break
        if tokens and tokens[0].content == '.':
            tokens.pop(0)  
            parse_E(tokens)
            
            build_tree('lambda', 2)
            print("E -> fn Vb+ . E")
            
        else:
            return SyntaxError
    else:
        parse_Ew(tokens)

def parse_Ew(tokens):
    parse_T(tokens)
    if tokens and tokens[0].content == 'where':
        tokens.pop(0)  
        parse_Dr(tokens)

def parse_T(tokens):
    parse_Ta(tokens)
    while tokens and tokens[0].content == ',':
        tokens.pop(0)  
        parse_Ta(tokens)

def parse_Ta(tokens):
    parse_Tc(tokens)
    while tokens and tokens[0].content == 'aug':
        tokens.pop(0)  
        parse_Tc(tokens)

def parse_Tc(tokens):
    parse_B(tokens)
    if tokens and tokens[0].content == '->':
        tokens.pop(0)  
        parse_Tc(tokens)
        if tokens and tokens[0].content == '|':
            tokens.pop(0)  
            parse_Tc(tokens)
        else:
            return SyntaxError

def parse_B(tokens):
    parse_Bt(tokens)
    while tokens and tokens[0].content == 'or':
        tokens.pop(0)  
        parse_Bt(tokens)

def parse_Bt(tokens):
    parse_Bs(tokens)
    while tokens and tokens[0].content == '&':
        tokens.pop(0)  
        parse_Bs(tokens)

def parse_Bs(tokens):
    if tokens and tokens[0].content == 'not':
        tokens.pop(0)  
        parse_Bp(tokens)
    else:
        parse_Bp(tokens)

def parse_Bp(tokens):
    parse_A(tokens)
    while tokens and tokens[0] in ['gr', '>', 'ge', '>=', 'ls', '<', 'le', '<=', 'eq', 'ne']:
        tokens.pop(0)
        parse_A(tokens)

def parse_A(tokens):
    while tokens and tokens[0] in ['+', '-']:
        tokens.pop(0)  
        parse_At(tokens)
    else:
        return SyntaxError
        
def parse_At(tokens):
    parse_Af(tokens)
    while tokens and tokens[0] in ['*', '/']:
        tokens.pop(0)  
        parse_Af(tokens)

def parse_Af(tokens):
    parse_Ap(tokens)
    if tokens and tokens[0] == '**':
        tokens.pop(0)  
        parse_Af(tokens)

def parse_Ap(tokens):
    parse_R(tokens)
    while tokens and tokens[0] == '@':
        tokens.pop(0)  
        if tokens and tokens[0].type == '<IDENTIFIER>':
            tokens.pop(0).content  
            parse_R(tokens)

def parse_R(tokens):
    parse_Rn(tokens)
    while tokens and tokens[0] in ['(', '<IDENTIFIER>', '<INTEGER>', '<STRING>', 'true', 'false', 'nil', 'dummy']:
        parse_Rn(tokens)

def parse_Rn(tokens):
    if tokens and tokens[0].type in ['<IDENTIFIER>', '<INTEGER>', '<STRING>']:
        tokens.pop(0) 
    elif tokens and tokens[0] in ['true', 'false', 'nil', 'dummy']:
        tokens.pop(0)  
    elif tokens and tokens[0].content == '(':
        tokens.pop(0)  
        parse_E(tokens)
        if tokens and tokens[0].content == ')':
            tokens.pop(0)  
        else:
            return SyntaxError
    else:
        return SyntaxError 

def parse_D(tokens):
    parse_Da(tokens)
    if tokens and tokens[0] == 'within':
        tokens.pop(0)  
        parse_D(tokens)

def parse_Da(tokens):
    parse_Dr(tokens)
    while tokens and tokens[0] == 'and':
        tokens.pop(0)  
        parse_Dr(tokens)

def parse_Dr(tokens):
    if tokens and tokens[0] == 'rec':
        tokens.pop(0)
        parse_Db(tokens)
    else:
        parse_Db(tokens)

def parse_Db(tokens):
    if tokens and tokens[0] == '(':
        tokens.pop(0)  
        parse_D(tokens)
        if tokens and tokens[0].content == ')':
            tokens.pop(0)  
        else:
            return SyntaxError
    elif tokens and tokens[0].type == '<IDENTIFIER>':
        tokens.pop(0).content  
        if tokens and tokens[0]== '=':
            tokens.pop(0)  
            parse_E(tokens)
        else:
            while True:
                parse_Vb(tokens)
                if not tokens or (tokens[0].content != '(' and tokens[0].type != 'IDENTIFIER'):
                    break
                tokens.pop(0)  
        if tokens and tokens[0].content == '=':
            tokens.pop(0)  
            parse_E(tokens)
        else:
            return SyntaxError

def parse_Vb(tokens):
    if tokens and tokens[0].type == '<IDENTIFIER>':
        tokens.pop(0)  
    elif tokens and tokens[0] == '(':
        tokens.pop(0)  
        if tokens and tokens[0] == ')':
            tokens.pop(0)  
        elif tokens and tokens[0] == '<IDENTIFIER>':
            parse_Vl(tokens)
            if tokens and tokens[0] == ')':
                tokens.pop(0) 
            else:
                return SyntaxError
        else:
            return SyntaxError
    else:
        return SyntaxError

def parse_Vl(tokens):
    if tokens and tokens[0].type == 'IDENTIFIER':
        tokens.pop(0)
        while tokens and tokens[0].content == ',':
            tokens.pop(0)  
            if tokens and tokens[0].type == 'IDENTIFIER':
                tokens.pop(0)
            else:
                return SyntaxError       


def build_tree(content, num_children):
  #  p = None # Change the variable name later
    
    for i in range(num_children):
        c = stack.pop(0)
        c.right_child = p
        p = c
        
    stack.insert(0, Node(content, p))
    
    
'''
def print_ast(node, depth=0):
    if node is not None:
        if node.type == 'literal':
            print("  " * depth + f"..{node.value}")
        else:
            print("  " * depth + f".{node.value}")
        for child in node.children:
            print_ast(child, depth + 1)

'''
file_name = input()
tokens = screen(file_name)
print(len(tokens))
for token in tokens:
    print(token.content)
    
    
#ast = parse_program(tokens)
#print_ast(ast)
