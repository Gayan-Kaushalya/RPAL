from screener import screen
from stack import Stack
from node import Node

# A stack containing nodes
stack = Stack()

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

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.next_token = self.tokens[0] # initializing the first token as 0th
    '''
    def stripDel(self):

        while self.pos < (len(self.tokens) -1) and  ((self.tokens[self.pos].type) == "<DELETE>" or (self.tokens[self.pos].type) == "<COMMENT>"):
            self.pos+=1
            self.next_token = self.tokens[self.pos]
    '''
    def read(self, expected_token):
        # print("Reading ", expected_token)
      #  self.stripDel()

        if self.next_token.content != expected_token:
            print(f"Error: Expected {expected_token} but got {self.next_token.content}")
            exit(1)
        self.pos+=1
        if self.pos < len(self.tokens):
            self.next_token = self.tokens[self.pos]
      #  tokens.pop(0)

      #  self.stripDel()

        # print("Next Token", self.next_token)
        
    def E(self):
        """E->'let' D 'in' E    => 'let'
            -> 'fn'  Vb+ '.' E  => 'lambda'
            ->  Ew;
        """
        # print("parsing in E", self.next_token)
        if self.next_token.content == "let":
            self.read("let")
            self.D()
            self.read("in")
            self.E()
            build_tree("let", 2)   #decide the number of children 3
        elif self.next_token.content == "fn":
            self.read("fn")
            n = 0
            self.Vb()
            n += 1
            while self.next_token.type == "<IDENTIFIER>" or self.next_token.type == "(": # first set of Vb ->[ <IDENTIFIER> , '(' ]
                self.Vb()
                n += 1
            self.read(".")
            self.E()
            build_tree("lambda", n+1 )  #decide the number of children 4
        else:
            self.Ew()
        # print("Returning from E")

    def Ew(self):
        """ Ew-> T 'where' Dr    => 'where'
                -> T;
        """
        # print("parsing in Ew", self.next_token)
        self.T()
        if self.next_token.content == "where":
            self.read("where")
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
        # print("parsing in T", self.next_token)
        self.Ta()
        if self.next_token.content == ",":
            n=0
            while self.next_token.content == ",":
                self.read(",")
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
        # print("parsing in Ta", self.next_token)
        self.Tc()
        while self.next_token.content == "aug":
            self.read("aug")
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
        # print("parsing in Tc", self.next_token)
        self.B()
        if self.next_token.content == "->":
            self.read("->")
            self.Tc()
            self.read("|")
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
        # print("parsing in B", self.next_token)
        self.Bt()
        while self.next_token.content == "or":
            self.read("or")
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
        # print("parsing in Bt", self.next_token)
        self.Bs()
        while self.next_token.content == "&":
            self.read("&")
            self.Bs()
            build_tree("&", 2)
        # print("Returning from Bt")

    def Bs(self):
        """
        Bs  -> 'not' Bp    => 'not'
            -> Bp;
        """
        # print("parsing in Bs", self.next_token)
        if self.next_token.content == "not":
            self.read("not")
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
        # print("parsing in Bp", self.next_token)
        self.A()
        if self.next_token.content == "gr" or self.next_token.content == ">":
            self.read(self.next_token.content)
            self.A()
            build_tree("gr", 2)
        elif self.next_token.content == "ge" or self.next_token.content == ">=":
            self.read(self.next_token.content)
            self.A()
            build_tree("ge", 2)
        elif self.next_token.content == "ls" or self.next_token.content == "<":
            self.read(self.next_token.content)
            self.A()
            build_tree("ls", 2)
        elif self.next_token.content == "le" or self.next_token.content == "<=":
            self.read(self.next_token.content)
            self.A()
            build_tree("le", 2)
        elif self.next_token.content == "eq":
            self.read("eq")
            self.A()
            build_tree("eq", 2)
        elif self.next_token.content == "ne":
            self.read("ne")
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
        # print("parsing in A", self.next_token)
        if self.next_token.content=="+":
            self.read("+")
            self.At()
        elif self.next_token.content=="-":
            self.read("-")
            self.At()
            build_tree("neg", 1)
        else:
            self.At()
        while self.next_token.content == "+" or self.next_token.content == "-":
            if self.next_token.content=="+":
                self.read("+")
                self.At()
                build_tree("+", 2)
            elif self.next_token.content=="-":
                self.read("-")
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
        # print("parsing in At", self.next_token)
        self.Af()
        while self.next_token.content == "*" or self.next_token.content == "/":
            if self.next_token.content=="*":
                self.read("*")
                self.Af()
                build_tree("*", 2)
            elif self.next_token.content=="/":
                self.read("/")
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
        # print("parsing in Af", self.next_token)
        self.Ap()
        if self.next_token.content == "**":
            self.read("**")
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
        # print("parsing in Ap", self.next_token)
        self.R()
        while self.next_token.content == "@":
            self.read("@")
            # check if the next token is an identifier
            if self.next_token.type == "<IDENTIFIER>":
                self.read(self.next_token.content)
                self.R()
                build_tree("@", 3)
            else:
                print(f"Error: Expected an identifier but got {self.next_token.content}")
                exit(1)
            
        # print("Returning from Ap")        

    def R(self):
        """
        R   -> R Rn    => 'gamma'
            -> Rn;
        -------------
        R -> Rn+
        """
        # print("parsing in R", self.next_token)
        self.Rn()
        while self.next_token.type in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"] or self.next_token.content in ["true", "false","nil", "(", "dummy"]: # check if the next token is in the first set of Rn
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
        # print("parsing in Rn", self.next_token)
        if self.next_token.content == "true":
            self.read("true")
            build_tree("true", 0)
        elif self.next_token.content == "false":
            self.read("false")
            build_tree("false", 0)
        elif self.next_token.content == "nil":
            self.read("nil")
            build_tree("nil", 0)
        elif self.next_token.content == "dummy":
            self.read("dummy")
            build_tree("dummy", 0)
        elif self.next_token.content == "(":
            self.read("(")
            self.E()
            self.read(")")
        # for other Identifier tokens
        elif self.next_token.type == "<IDENTIFIER>":
            val = self.next_token.content
            self.read(self.next_token.content)
            build_tree("id :"+ val, 0)
        elif self.next_token.type == "<INTEGER>":
            val = self.next_token.content
            self.read(self.next_token.content)
            build_tree("int :"+ val, 0)
        elif self.next_token.type == "<STRING>":
            val = self.next_token.content
            self.read(self.next_token.content)
            build_tree("str :"+ val, 0)
        else:
            print(f"Error: Expected an identifier, integer, string, 'true', 'false', 'nil', '(', or 'dummy' but got {self.next_token.content}")
            exit(1)
        # print("Returning from Rn")

    def D(self):
        """
        D   -> Da 'within' D    => 'within'
            -> Da;
        """
        # print("parsing in D", self.next_token)
        self.Da()
        if self.next_token.content == "within":
            self.read("within")
            self.D()
            build_tree("within", 2)
        # print("Returning from D")

    def Da(self):
        """
        Da  -> Dr ('and' Da)+    => 'and'
            -> Dr;
        """
        # print("parsing in Da", self.next_token)
        self.Dr()
        n=0
        while self.next_token.content == "and":
            self.read("and")
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
        # print("parsing in Dr", self.next_token)
        if self.next_token.content == "rec":
            self.read("rec")
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
        # print("parsing in Db", self.next_token)
        if self.next_token.content == "(":
            self.read("(")
            self.D()
            self.read(")")


        elif self.next_token.type == "<IDENTIFIER>":
            val = self.next_token.content
            self.read(self.next_token.content)
            build_tree(val,0)

            if self.next_token.content=="," or self.next_token.content == "=":  #checking if this should go through vl
                self.Vl()
                self.read("=")
                self.E()
                build_tree("=", 2)
            
            else: # going through Vb path
                n=0
                self.Vb()
                n+=1
                while self.next_token.type == "<IDENTIFIER>" or self.next_token.type == "(":  # check if the next token is in the first set of Vb
                    self.read(self.next_token.content)
                    self.Vb()
                    n+=1
                self.read("=")
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
        # print("parsing in Vb", self.next_token)
        if self.next_token.type == "<IDENTIFIER>":
            val = self.next_token.content
            # print(self.next_token)
            self.read(self.next_token.content)
            build_tree(val, 0)
        elif self.next_token.content == "(":
            self.read("(")
            if self.next_token.content == ")":
                self.read(")")
                build_tree("()", 0)
            elif self.next_token.type == "<IDENTIFIER>": #first set of Vl
                val = self.next_token.content
                self.read(self.next_token.content)
                build_tree(val,0)
                self.Vl()
                self.read(")")
        else:
            print(f"Error: Expected an identifier or  '(' but got {self.next_token.content}")
            exit(1)
        # print("Returning from Vb")

    def Vl(self):
        """
        Vl  -> <identifier> (',' <identifier>)*    => ','?
        """ 
        # print("parsing in Vl", self.next_token)
        n=0
        while self.next_token.content == ",":
            self.read(",")
            if self.next_token.type == "<IDENTIFIER>":
                val = self.next_token.content
                self.read(self.next_token.content)
                build_tree(val,0)
                n+=1
            else:
                print("Error from Vl")
        if n>0:
            build_tree(",", n+1) 
        # print("Returning from Vl")



prog_file = input()
tokens = screen(prog_file)

'''
LE = LexicalAnalyser(prog_file)
tokens = LE.lexical_analyser()

for token in tokens:
    print(token[0], token[1])
    '''
P = Parser(tokens)
#P.stripDel()
P.E()
print_tree()