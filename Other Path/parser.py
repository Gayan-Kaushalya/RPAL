from screener import screen
from stack import Stack
from node import *

# A stack containing nodes
stack = Stack()

# Try to change this function
def build_tree(value, num_children):
    node = Node(value)
    node.children = [None] * num_children
    
    for i in range (num_children - 1, -1, -1): 
        if stack.is_empty():
            print("Can't build tree, stack is empty")
        node.children[i] = stack.pop()
    stack.push(node)
    
def print_tree():
    if not stack.is_empty():
        root = stack.pop()
        preorder_traversal(root)
    else:
        print("Tree is empty")
 
def read(expected_token):
    if tokens[0].content != expected_token:
        print("Syntax error in line " + str(tokens[0].line) + ": Expected " + str(expected_token) + " but got " + str(tokens[0].content))
        exit(1)
     
    if not tokens[0].is_last_token:
        del tokens[0]   

def parse(tokens):
    procedure_E()
    print_tree()
 
############################################################## 
def procedure_E():
    # E -> 'let' D 'in' E   
    #   -> 'fn'  Vb+ '.' E 
    #   ->  Ew
    
    if tokens[0].content == "let":
        read("let")
        procedure_D()
        
        if tokens[0].content == "in":
            read("in")
            procedure_E()
            build_tree("let", 2)
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Expected 'in' but got " + str(tokens[0].content))
            exit(1)
     
    # The fn function is not sure   
    elif tokens[0].content == "fn":
        read("fn")
        n = 0

        while tokens[0].type == "<IDENTIFIER>" or tokens[0].type == "(": 
            procedure_Vb()
            n += 1
            
        if tokens[0].content == ".":
            read(".")
            procedure_E()
            build_tree("lambda", n + 1)
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Expected '.' but got " + str(tokens[0].content))
            exit(1) 
        
    else:
        procedure_Ew()

##############################################################
def procedure_Ew():
    # Ew -> T 'where' Dr    
    #    -> T
    
    procedure_T()
    if tokens[0].content == "where":
        read("where")
        procedure_Dr()
        build_tree("where", 2)  
        
##############################################################
def procedure_T(): 
    # T -> Ta (','  Ta)+ 
    #   -> Ta
    
    procedure_Ta()
    
    n=0
    while tokens[0].content == ",":
        read(",")
        procedure_Ta()
        n+=1
        
    if n > 0:
        build_tree("tau", n+1)
        
##############################################################      
def procedure_Ta():
    # Ta -> Ta 'aug' Tc   
    #    -> Tc

    procedure_Tc()
    while tokens[0].content == "aug":
        read("aug")
        procedure_Tc()
        build_tree("aug", 2)  
        
##############################################################
def procedure_Tc():
    # Tc -> B '->' Tc '|' Tc
    #    -> B

    procedure_B()
    
    if tokens[0].content == "->":   # Should this be while or if?
        read("->")
        procedure_Tc()
        
        if tokens[0].content == "|":
            read("|")
            procedure_Tc()
            build_tree("->", 3)
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Expected '|' but got " + str(tokens[0].content))
            exit(1)
            
##############################################################
def procedure_B():
    # B -> B 'or' Bt 
    #   -> Bt

    procedure_Bt()
    while tokens[0].content == "or":
        read("or")
        procedure_Bt()
        build_tree("or", 2) 

##############################################################
def procedure_Bt():
    # Bt -> Bt '&' Bs    
    #    -> Bs
    
    procedure_Bs()
    while tokens[0].content == "&":
        read("&")
        procedure_Bs()
        build_tree("&", 2)
        
##############################################################
def procedure_Bs():
    # Bs -> 'not' Bp
    #    -> Bp
    
    if tokens[0].content == "not":
        read("not")
        procedure_Bp()
        build_tree("not", 1)
    else:
        procedure_Bp()
        
##############################################################
def procedure_Bp():
    # Bp -> A ('gr' | '>' ) A   
    #    -> A ('ge' | '>=' ) A   
    #    -> A ('ls' | '<' ) A    
    #    -> A ('le' | '<=' ) A  
    #    -> A 'eq' A            
    #    -> A 'ne' A             
    #    -> A
    
    procedure_A()
    
    if tokens[0].content == "gr" or tokens[0].content == ">":
        read(tokens[0].content)
        procedure_A()
        build_tree("gr", 2)
    elif tokens[0].content == "ge" or tokens[0].content == ">=":
        read(tokens[0].content)
        procedure_A()
        build_tree("ge", 2)
    elif tokens[0].content == "ls" or tokens[0].content == "<":
        read(tokens[0].content)
        procedure_A()
        build_tree("ls", 2)
    elif tokens[0].content == "le" or tokens[0].content == "<=":
        read(tokens[0].content)
        procedure_A()
        build_tree("le", 2)
    elif tokens[0].content == "eq":
        read("eq")
        procedure_A()
        build_tree("eq", 2)
    elif tokens[0].content == "ne":
        read("ne")
        procedure_A()
        build_tree("ne", 2)

##############################################################
def procedure_A():
    # A -> A '+' At  
    #   -> A '-' At  
    #   ->   '+' At
    #   ->   '-' At   
    #   -> At

    if tokens[0].content=="+":
        read("+")
        procedure_At()
    elif tokens[0].content=="-":
        read("-")
        procedure_At()
        build_tree("neg", 1)
    else:
        procedure_At()
        
    while tokens[0].content in ["+", "-"]:
        if tokens[0].content=="+":
            read("+")
            procedure_At()
            build_tree("+", 2)
        else:
            read("-")
            procedure_At()
            build_tree("-", 2)
    
##############################################################
def procedure_At():
    # At -> At '*' Af   
    #    -> At '/' Af    
    #    -> Af

    procedure_Af()
    while tokens[0].content in ["*", "/"]:
        if tokens[0].content=="*":
            read("*")
            procedure_Af()
            build_tree("*", 2)
        else:
            read("/")
            procedure_Af()
            build_tree("/", 2)

##############################################################
def procedure_Af():
    # Af -> Ap '**' Af  
    #    -> Ap
    
    procedure_Ap()
    if tokens[0].content == "**":     # Should this be while or if?
        read("**")
        procedure_Af()
        build_tree("**", 2)
 
##############################################################    
def procedure_Ap():
    # Ap -> Ap '@' <identifier> R
    #    -> R

    procedure_R()
    while tokens[0].content == "@":
        read("@")
        
        if tokens[0].type == "<IDENTIFIER>":
            read(tokens[0].content)
            procedure_R()
            build_tree("@", 3)             # Not sure whether this is 2 or 3 
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Expected an identifier but got " + str(tokens[0].content))
            exit(1)
    
##############################################################
def procedure_R():
    # R -> R Rn   
    #   -> Rn

    procedure_Rn()
    while tokens[0].type in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"] or tokens[0].content in ["true", "false","nil", "(", "dummy"]: 
        procedure_Rn()
        build_tree("gamma", 2)
    
##############################################################
def procedure_Rn():    # we can create a variable named tok_type
    # Rn -> <IDENTIFIER>
    #    -> <INTEGER>
    #    -> <STRING>
    #    -> 'true'      
    #    -> 'false'      
    #    -> 'nil'      
    #    -> '(' E ')'
    #    -> 'dummy'     
    
    value = tokens[0].content
    
    if tokens[0].type == "<IDENTIFIER>":
        read(value)
        build_tree("<ID:" + value + ">", 0)
        
    elif tokens[0].type == "<INTEGER>":
        read(value)
        build_tree("<INT:" + value + ">", 0)
        
    elif tokens[0].type == "<STRING>":
        read(value)
        build_tree("<STR:" + value + ">", 0)
        
    elif value in ["true", "false", "nil", "dummy"]:
        read(value)
        build_tree(value, 0)
        
    elif value == "(":
        read("(")
        procedure_E()
        
        if tokens[0].content == ")":        #### Should we call value again here?
            read(")")
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Expected ')' but got " + str(tokens[0].content))
            exit(1)
            
    else:
        print("Syntax error in line " + str(tokens[0].line) + ": Expected an identifier, integer, string, 'true', 'false', 'nil', '(', or 'dummy' but got " + str(tokens[0].content))
        exit(1)

##############################################################
def procedure_D():
    """
    D   -> Da 'within' D    => 'within'
        -> Da
    """
    # print("parsing in D", tokens[0])
    Da()
    if tokens[0].content == "within":
        read("within")
        procedure_D()
        build_tree("within", 2)
    # print("Returning from D")

def Da():
    """
    Da  -> Dr ('and' Da)+    => 'and'
        -> Dr
    """
    # print("parsing in Da", tokens[0])
    procedure_Dr()
    n=0
    while tokens[0].content == "and":
        read("and")
        procedure_Dr()
        n+=1
    if n>0:  # check if there are more than one 'and' in the input
        build_tree("and", n+1)
    # print("Returning from Da")

def procedure_Dr():
    """
    Dr  -> 'rec' Db    => 'rec'
        -> Db
    """
    # print("parsing in Dr", tokens[0])
    if tokens[0].content == "rec":
        read("rec")
        Db()
        build_tree("rec", 1)
    else:
        Db()
    # print("Returning from Dr")

def Db():
    """
    Db  -> Vl '=' E    => '='  first set of vl is <identifier>
        -> <identifier> Vb+ '=' E    => 'fcn_form'
        -> '(' D ')'
    """
    # print("parsing in Db", tokens[0])
    if tokens[0].content == "(":
        read("(")
        procedure_D()
        read(")")


    elif tokens[0].type == "<IDENTIFIER>":
        val = tokens[0].content
        read(tokens[0].content)
        build_tree(val,0)  ####<id

        if tokens[0].content=="," or tokens[0].content == "=":  #checking if this should go through vl
            Vl()
            read("=")
            procedure_E()
            build_tree("=", 2)
        
        else: # going through Vb path
            n=0
            procedure_Vb()
            n+=1
            while tokens[0].type == "<IDENTIFIER>" or tokens[0].type == "(":  # check if the next token is in the first set of Vb
                read(tokens[0].content)
                procedure_Vb()
                n+=1
            read("=")
            procedure_E()
            build_tree("fcn_form", n+2)
    # else:
    #     Vl()
        
    # print("Returning from Db")

def procedure_Vb(): 
    """
    Vb -> <identifier>
        -> '(' Vl ')'
        -> '(' ')'  => '()'
    """
    # print("parsing in Vb", tokens[0])
    if tokens[0].type == "<IDENTIFIER>":
        val = tokens[0].content
        # print(tokens[0])
        read(tokens[0].content)
        build_tree(val, 0)     ####<id
    elif tokens[0].content == "(":
        read("(")
        if tokens[0].content == ")":
            read(")")
            build_tree("()", 0)
        elif tokens[0].type == "<IDENTIFIER>": #first set of Vl
            val = tokens[0].content
            read(tokens[0].content)
            build_tree(val,0)    ####<id
            Vl()
            read(")")
    else:
        print("Syntax error in line " + str(tokens[0].line) + ": Expected an identifier or '(' but got " + str(tokens[0].content))
        exit(1)
    # print("Returning from Vb")

def Vl():
    """
    Vl  -> <identifier> (',' <identifier>)*    => ','?
    """ 
    # print("parsing in Vl", tokens[0])
    n=0
    while tokens[0].content == ",":
        read(",")
        if tokens[0].type == "<IDENTIFIER>":
            val = tokens[0].content
            read(tokens[0].content)
            build_tree(val,0)    ####<id
            n+=1
        else:
            print("Error from Vl")
    if n>0:
        build_tree(",", n+1) 
    # print("Returning from Vl")



prog_file = input()
tokens = screen(prog_file)
parse(tokens)