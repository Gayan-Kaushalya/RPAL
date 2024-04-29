from screener import screen
from stack import Stack
from node import *

# A stack containing nodes
stack = Stack()

# Try to change this function
def build_tree(value, num_children):
    node = Node(value)
    node.children = [None] * num_children
    
    for i in range (num_children - 1, -1, -1): #i = 5 4 3 2 1 0 for 6 children
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
        print(f"Error: Expected {expected_token} but got {tokens[0].content}")
        exit(1)
     
    if not tokens[0].is_last_token:
        del tokens[0]   

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        tokens[0] = self.tokens[0] # initializing the first token as 0th

    

        
    def E(self):
        """E->'let' D 'in' E    => 'let'
            -> 'fn'  Vb+ '.' E  => 'lambda'
            ->  Ew;
        """
        # print("parsing in E", tokens[0])
        if tokens[0].content == "let":
            read("let")
            self.D()
            read("in")
            self.E()
            build_tree("let", 2)   #decide the number of children 3
        elif tokens[0].content == "fn":
            read("fn")
            n = 0
            self.Vb()
            n += 1
            while tokens[0].type == "<IDENTIFIER>" or tokens[0].type == "(": # first set of Vb ->[ <IDENTIFIER> , '(' ]
                self.Vb()
                n += 1
            read(".")
            self.E()
            build_tree("lambda", n+1 )  #decide the number of children 4
        else:
            self.Ew()
        # print("Returning from E")

    def Ew(self):
        """ Ew-> T 'where' Dr    => 'where'
                -> T;
        """
        # print("parsing in Ew", tokens[0])
        self.T()
        if tokens[0].content == "where":
            read("where")
            self.Dr()
            build_tree("where", 2)  #decide the number of children 5
        # print("Returning from Ew")
    
    def T(self):
        """ 
        T   -> Ta (','  Ta)+    => 'tau'
            -> Ta;
        -------------------------------
        T -> Ta (',' Ta)*
        """
        # print("parsing in T", tokens[0])
        self.Ta()
        if tokens[0].content == ",":
            n=0
            while tokens[0].content == ",":
                read(",")
                self.Ta()
                n+=1
            build_tree("tau", n+1) #decide the number of children 6
        # print("Returning from T")

    def Ta(self):
        """ 
        Ta  -> Ta 'aug' Tc    => 'aug'
            -> Tc;
        -------------------------------
        Ta -> Tc ('aug' Tc)*
        
        """
        # print("parsing in Ta", tokens[0])
        self.Tc()
        while tokens[0].content == "aug":
            read("aug")
            self.Tc()
            build_tree("aug", 2)  #decide the number of children 7
        # print("Returning from Ta")

    def Tc(self):
        """
        Tc  -> B '->' Tc '|' Tc   => '->'
            -> B;
        --------------------------------
        Tc -> B (   |  '->' Tc '|' Tc)
        """
        # print("parsing in Tc", tokens[0])
        self.B()
        if tokens[0].content == "->":
            read("->")
            self.Tc()
            read("|")
            self.Tc()
            build_tree("->", 3)
        # print("Returning from Tc")

    def B(self):
        """
        B   -> B 'or' Bt    => 'or'
            -> Bt;
        --------------------------------
        B -> Bt ('or' Bt)*
        """
        # print("parsing in B", tokens[0])
        self.Bt()
        while tokens[0].content == "or":
            read("or")
            self.Bt()
            build_tree("or", 2)  #decide the number of children 9
        # print("Returning from B")

    def Bt(self):
        """
        Bt  -> Bt '&' Bs    => '&'
            -> Bs;
        --------------------------------
        Bt -> Bs ('&' Bs)*
        """
        # print("parsing in Bt", tokens[0])
        self.Bs()
        while tokens[0].content == "&":
            read("&")
            self.Bs()
            build_tree("&", 2)
        # print("Returning from Bt")

    def Bs(self):
        """
        Bs  -> 'not' Bp    => 'not'
            -> Bp;
        """
        # print("parsing in Bs", tokens[0])
        if tokens[0].content == "not":
            read("not")
            self.Bp()
            build_tree("not", 1)
        else:
            self.Bp()
        # print("Returning from Bs")

    def Bp(self):
        """
        Bp  -> A ('gr' | '>' ) A    => 'gr'
            -> A ('ge' | '>=' ) A   => 'ge'
            -> A ('ls' | '<' ) A    => 'ls'
            -> A ('le' | '<=' ) A   => 'le'
            -> A 'eq' A             => 'eq'
            -> A 'ne' A             => 'ne'
            -> A;
        """
        # print("parsing in Bp", tokens[0])
        self.A()
        if tokens[0].content == "gr" or tokens[0].content == ">":
            read(tokens[0].content)
            self.A()
            build_tree("gr", 2)
        elif tokens[0].content == "ge" or tokens[0].content == ">=":
            read(tokens[0].content)
            self.A()
            build_tree("ge", 2)
        elif tokens[0].content == "ls" or tokens[0].content == "<":
            read(tokens[0].content)
            self.A()
            build_tree("ls", 2)
        elif tokens[0].content == "le" or tokens[0].content == "<=":
            read(tokens[0].content)
            self.A()
            build_tree("le", 2)
        elif tokens[0].content == "eq":
            read("eq")
            self.A()
            build_tree("eq", 2)
        elif tokens[0].content == "ne":
            read("ne")
            self.A()
            build_tree("ne", 2)
        # other values should not be passed from this
        # print("Returning from Bp")

    def A(self):
        """
        A   -> A '+' At    => '+'
            -> A '-' At    => '-'
            ->   '+' At
            ->   '-' At    => 'neg'
            -> At;
        --------------------------------
        A -> ( '+' At | '-' At | At ) ( '+' At | '-' At)*
        """
        # print("parsing in A", tokens[0])
        if tokens[0].content=="+":
            read("+")
            self.At()
        elif tokens[0].content=="-":
            read("-")
            self.At()
            build_tree("neg", 1)
        else:
            self.At()
        while tokens[0].content == "+" or tokens[0].content == "-":
            if tokens[0].content=="+":
                read("+")
                self.At()
                build_tree("+", 2)
            elif tokens[0].content=="-":
                read("-")
                self.At()
                build_tree("-", 2)
        # print("Returning from A")

    def At(self):
        """
        At  -> At '*' Af    => '*'
            -> At '/' Af    => '/'
            -> Af;
        --------------------------------
        At -> Af (* Af | / Af)*
        """
        # print("parsing in At", tokens[0])
        self.Af()
        while tokens[0].content == "*" or tokens[0].content == "/":
            if tokens[0].content=="*":
                read("*")
                self.Af()
                build_tree("*", 2)
            elif tokens[0].content=="/":
                read("/")
                self.Af()
                build_tree("/", 2)
        # print("Returning from At")

    def Af(self):
        """
        Af  -> Ap '**' Af    => '**'
            -> Ap;
        ------------------------
        Af -> Ap (    | ** Af)
        """
        # print("parsing in Af", tokens[0])
        self.Ap()
        if tokens[0].content == "**":
            read("**")
            self.Af()
            build_tree("**", 2)
        # print("Returning from Af")
        
    def Ap(self):
        """
        Ap  -> Ap '@' <identifier> R    => '@'
            -> R;
        ---------------------------------
        Ap -> R ( @ identifier R)*
            
        """
        # print("parsing in Ap", tokens[0])
        self.R()
        while tokens[0].content == "@":
            read("@")
            # check if the next token is an identifier
            if tokens[0].type == "<IDENTIFIER>":
                read(tokens[0].content)
                self.R()
                build_tree("@", 3)
            else:
                print(f"Error: Expected an identifier but got {tokens[0].content}")
                exit(1)
            
        # print("Returning from Ap")        

    def R(self):
        """
        R   -> R Rn    => 'gamma'
            -> Rn;
        -------------
        R -> Rn+
        """
        # print("parsing in R", tokens[0])
        self.Rn()
        while tokens[0].type in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"] or tokens[0].content in ["true", "false","nil", "(", "dummy"]: # check if the next token is in the first set of Rn
            self.Rn()
            build_tree("gamma", 2)
        # print("Returning from R")

    def Rn(self):
        """
        Rn  -> <Identifier>
            -> <Integer>
            -> <String>
            -> 'true'       => 'true'
            -> 'false'      => 'false'
            -> 'nil'        => 'nil'
            -> '(' E ')'
            -> 'dummy'      => 'dummy';
        """
        # print("parsing in Rn", tokens[0])
        if tokens[0].content == "true":
            read("true")
            build_tree("true", 0)
        elif tokens[0].content == "false":
            read("false")
            build_tree("false", 0)
        elif tokens[0].content == "nil":
            read("nil")
            build_tree("nil", 0)
        elif tokens[0].content == "dummy":
            read("dummy")
            build_tree("dummy", 0)
        elif tokens[0].content == "(":
            read("(")
            self.E()
            read(")")
        # for other Identifier tokens
        elif tokens[0].type == "<IDENTIFIER>":
            val = tokens[0].content
            read(tokens[0].content)
            build_tree("id :"+ val, 0)
        elif tokens[0].type == "<INTEGER>":
            val = tokens[0].content
            read(tokens[0].content)
            build_tree("int :"+ val, 0)
        elif tokens[0].type == "<STRING>":
            val = tokens[0].content
            read(tokens[0].content)
            build_tree("str :"+ val, 0)
        else:
            print(f"Error: Expected an identifier, integer, string, 'true', 'false', 'nil', '(', or 'dummy' but got {tokens[0].content}")
            exit(1)
        # print("Returning from Rn")

    def D(self):
        """
        D   -> Da 'within' D    => 'within'
            -> Da;
        """
        # print("parsing in D", tokens[0])
        self.Da()
        if tokens[0].content == "within":
            read("within")
            self.D()
            build_tree("within", 2)
        # print("Returning from D")

    def Da(self):
        """
        Da  -> Dr ('and' Da)+    => 'and'
            -> Dr;
        """
        # print("parsing in Da", tokens[0])
        self.Dr()
        n=0
        while tokens[0].content == "and":
            read("and")
            self.Dr()
            n+=1
        if n>0:  # check if there are more than one 'and' in the input
            build_tree("and", n+1)
        # print("Returning from Da")

    def Dr(self):
        """
        Dr  -> 'rec' Db    => 'rec'
            -> Db;
        """
        # print("parsing in Dr", tokens[0])
        if tokens[0].content == "rec":
            read("rec")
            self.Db()
            build_tree("rec", 1)
        else:
            self.Db()
        # print("Returning from Dr")

    def Db(self):
        """
        Db  -> Vl '=' E    => '='  first set of vl is <identifier>
            -> <identifier> Vb+ '=' E    => 'fcn_form';
            -> '(' D ')';
        """
        # print("parsing in Db", tokens[0])
        if tokens[0].content == "(":
            read("(")
            self.D()
            read(")")


        elif tokens[0].type == "<IDENTIFIER>":
            val = tokens[0].content
            read(tokens[0].content)
            build_tree(val,0)

            if tokens[0].content=="," or tokens[0].content == "=":  #checking if this should go through vl
                self.Vl()
                read("=")
                self.E()
                build_tree("=", 2)
            
            else: # going through Vb path
                n=0
                self.Vb()
                n+=1
                while tokens[0].type == "<IDENTIFIER>" or tokens[0].type == "(":  # check if the next token is in the first set of Vb
                    read(tokens[0].content)
                    self.Vb()
                    n+=1
                read("=")
                self.E()
                build_tree("fcn_form", n+2)
        # else:
        #     self.Vl()
            
        # print("Returning from Db")

    def Vb(self): 
        """
        Vb -> <identifier>
            -> '(' Vl ')'
            -> '(' ')'  => '()';
        """
        # print("parsing in Vb", tokens[0])
        if tokens[0].type == "<IDENTIFIER>":
            val = tokens[0].content
            # print(tokens[0])
            read(tokens[0].content)
            build_tree(val, 0)
        elif tokens[0].content == "(":
            read("(")
            if tokens[0].content == ")":
                read(")")
                build_tree("()", 0)
            elif tokens[0].type == "<IDENTIFIER>": #first set of Vl
                val = tokens[0].content
                read(tokens[0].content)
                build_tree(val,0)
                self.Vl()
                read(")")
        else:
            print(f"Error: Expected an identifier or  '(' but got {tokens[0].content}")
            exit(1)
        # print("Returning from Vb")

    def Vl(self):
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
                build_tree(val,0)
                n+=1
            else:
                print("Error from Vl")
        if n>0:
            build_tree(",", n+1) 
        # print("Returning from Vl")



prog_file = input()
tokens = screen(prog_file)


tokens[0] = tokens[0]

P = Parser(tokens)
#P.stripDel()
P.E()
print_tree()