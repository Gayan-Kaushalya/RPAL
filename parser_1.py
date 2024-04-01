import lexical_analyzer 
import screener2


'''
class ASTNode:
    def _init_(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []
'''
def parse_program(tokens):
    # Parse the program starting from the root rule
    return parse_E(tokens)

def parse_E(tokens):
    # Implementation for parsing E rule
    # E -> 'let' D 'in' E => 'let'
    if tokens and tokens[0].content == 'let':
        tokens.pop(0)  # Consume 'let'
        parse_D(tokens)
        if tokens and tokens[0].content == 'in':
            tokens.pop(0)  # Consume 'in'
        else:
            # Handle error: Expected 'in' after 'let D'
            print("Syntax_Error : Expected 'in' after 'let D'")
            return None
    elif tokens and tokens[0].content == 'fn':
        # E -> 'fn' Vb+ '.' E => 'lambda'
        tokens.pop(0)  # Consume 'fn'
        while True:
            parse_Vb(tokens)
            if not tokens or (tokens[0].content != '(' and tokens[0].type != 'IDENTIFIER'):
                break
            tokens.pop(0)  # Consume ','
        if tokens and tokens[0].content == '.':
            tokens.pop(0)  # Consume '.'
            parse_E(tokens)
        else:
            # Handle error
            print("Syntax_Error : Expected '.' after 'fn Vb+'")
            return None
    # E -> Ew
    parse_Ew(tokens)

def parse_Ew(tokens):
    # Implementation for parsing Ew rule
    # Ew -> T 'where' Dr => 'where'
    #    | T
    parse_T(tokens)
    if tokens and tokens[0].content == 'where':
        tokens.pop(0)  # Consume 'where'
        parse_Dr(tokens)

def parse_T(tokens):
    # Implementation for parsing T rule
    # T -> Ta ( ',' Ta )+ => 'tau'
    #   | Ta
    parse_Ta(tokens)
    while tokens and tokens[0].content == ',':
        tokens.pop(0)  # Consume ','
        parse_Ta(tokens)

def parse_Ta(tokens):
    # Implementation for parsing Ta rule
    # Ta -> Ta 'aug' Tc => 'aug'
    #    | Tc
    parse_Tc(tokens)
    if tokens and tokens[0].content == 'aug':
        tokens.pop(0)  # Consume 'aug'
        parse_Tc(tokens)
    

def parse_Tc(tokens):
    # Implementation for parsing Tc rule
    # Tc -> B '->' Tc '|' Tc => '->'
    #    | B
    parse_B(tokens)
    if tokens and tokens[0].content == '->':
        tokens.pop(0)  # Consume '->'
        parse_Tc(tokens)
        if tokens and tokens[0].content == '|':
            tokens.pop(0)  # Consume '|'
            parse_Tc(tokens)
        else:
            # Handle error: Expected '|' after '->' Tc
            print("Syntax_Error : Expected '|' after '->' Tc")
            return None
    return None

def parse_B(tokens):
    # Implementation for parsing B rule
    # B -> B'or' Bt => 'or'
    #    | Bt
    parse_Bt(tokens)
    if tokens and tokens[0].content == 'or':
        tokens.pop(0)  # Consume 'or'
        parse_Bt(tokens)
    

def parse_Bt(tokens):
    # Implementation for parsing Bt rule# Example:
    # Bt -> Bt '&' Bs => '&'
    #    | Bs
    parse_Bs(tokens)
    if tokens and tokens[0].content == '&':
        tokens.pop(0)  # Consume '&'
        parse_Bs(tokens)

def parse_Bs(tokens):
    # Implementation for parsing Bs rule
    # Bs -> 'not' Bp => 'not'
    #    | Bp
    if tokens and tokens[0].content == 'not':
        tokens.pop(0)  # Consume 'not'
        parse_Bp(tokens)
    else:
        parse_Bp(tokens)

def parse_Bp(tokens):
    # Implementation for parsing Bp rule
    # Bp -> A ('gr' | '>') A => 'gr'
    #    | A
    parse_A(tokens)
    if tokens and tokens[0].content in ['gr', '>']:
        tokens.pop(0)  # Consume 'gr' or '>'
        parse_A(tokens)
    elif tokens and tokens[0].content in ['ge', '>=']:
        tokens.pop(0)
        parse_A(tokens)
    elif tokens and tokens[0].content in ['ls', '<']:
        tokens.pop(0)
        parse_A(tokens)
    elif tokens and tokens[0].content in ['le', '<=']:
        tokens.pop(0)
        parse_A(tokens)
    elif tokens and tokens[0].content in ['eq']:
        tokens.pop(0)
        parse_A(tokens)
    elif tokens and tokens[0].content in ['ne']:
        tokens.pop(0)
        parse_A(tokens)

def parse_A(tokens):
    # Implementation for parsing A rule
    # Example:
    # A -> A'+' At => '+'
    #    | A '-' At => '-'
    #    | '+' At
    #    | '-' At => 'neg'
    #    | At
    if tokens and tokens[0].content == '+':
        tokens.pop(0)  # Consume '+'
        parse_At(tokens)
    elif tokens and tokens[0].content == '-':
        tokens.pop(0)  # Consume '-'
        parse_At(tokens)
    else:
        parse_At(tokens)
    
def parse_At(tokens):
    # Implementation for parsing At rule
    # Example:
    # At -> At '' Af => ''
    #    | At '/' Af => '/'
    #    | Af
    parse_Af(tokens)
    if tokens and tokens[0].content in ['*', '/']:
        tokens.pop(0)  # Consume '*' or '/'
        parse_Af(tokens)

def parse_Af(tokens):
    # Implementation for parsing Af rule
    # Example:
    # Af -> Ap '' Af => ''
    #    | Ap
    parse_Ap(tokens)
    if tokens and tokens[0].content == '':
        tokens.pop(0)  # Consume ''
        parse_Af(tokens)

def parse_Ap(tokens):
    # Implementation for parsing Ap rule
    # Example:
    # Ap -> Ap '@' '<IDENTIFIER>' R => '@'
    #    | R
    parse_R(tokens)
    if tokens and tokens[0].content == '@':
        tokens.pop(0)  # Consume '@'
        if tokens and tokens[0].type == 'IDENTIFIER':
            tokens.pop(0)  # Consume '<IDENTIFIER>'
            parse_R(tokens)
        

def parse_R(tokens):
    # Implementation for parsing R rule
    # Example:
    # R -> RRn => 'gamma'
    #    | Rn\
    parse_Rn(tokens)
    while (tokens and tokens[0].content in ['true', 'false', 'nil', '(', '<IDENTIFIER>', '<INTEGER>', '<STRING>']):
        parse_Rn(tokens)
    

def parse_Rn(tokens):
    # Implementation for parsing Rn rule
    # Example:
    # Rn -> '<IDENTIFIER>'
    #    | '<INTEGER>'
    #    | '<STRING>'
    #    | 'true' => 'true'
    #    | 'false' => 'false'
    #    | 'nil' => 'nil'
    #    | '(' E ')'
    if tokens and tokens[0].type in ['IDENTIFIER', 'INTEGER', 'STRING']:
        tokens.pop(0)  # Consume token
    elif tokens and tokens[0].content in ['true', 'false', 'nil','dummy']:
        tokens.pop(0)  # Consume token
    elif tokens and tokens[0].content == '(':
        tokens.pop(0)  # Consume '('
        parse_E(tokens)
        if tokens and tokens[0].content == ')':
            tokens.pop(0)  # Consume ')'
        else:
            # Handle error: Expected ')' after expression
            pass
    else:
        # Handle error: Expected token
        pass

def parse_D(tokens):
    # Implementation for parsing D rule
    # Example:
    # D -> Da 'within' D => 'within'
    #    | Da
    parse_Da(tokens)
    if tokens and tokens[0].content == 'within':
        tokens.pop(0)  # Consume 'within'
        parse_D(tokens)

def parse_Da(tokens):
    # Implementation for parsing Da rule
    # Example:
    # Da -> Dr ('and' Dr)+ => 'and'
    #    | Dr
    parse_Dr(tokens)
    while tokens and tokens[0].content == 'and':
        tokens.pop(0)  # Consume 'and'
        parse_Dr(tokens)

def parse_Dr(tokens):
    # Implementation for parsing Dr rule
    # Example:
    # Dr -> 'rec' Db => 'rec'
    #    | Db
    if tokens and tokens[0].content == 'rec':
        tokens.pop(0)  # Consume 'rec'
        parse_Db(tokens)

def parse_Db(tokens):
    # Implementation for parsing Db rule
    # Example:
    # Db -> Vl '=' E => '='
    #    | '<IDENTIFIER>' Vb+ '=' E => 'fcn_form'
    #    | '(' D ')'
    if tokens and tokens[0].content == '(':
        tokens.pop(0)  # Consume '('
        parse_D(tokens)
        if tokens and tokens[0].content == ')':
            tokens.pop(0)  # Consume ')'
        else:
            # Handle error: Expected ')' after definition
            pass
    elif tokens and tokens[0].type == 'IDENTIFIER':
        tokens.pop(0)  # Consume '<IDENTIFIER>'
        while True:
            parse_Vb(tokens)
            if not tokens or (tokens[0].content != '(' and tokens[0].type != 'IDENTIFIER'):
                break
            tokens.pop(0)  # Consume ','
        if tokens and tokens[0].content == '=':
            tokens.pop(0)  # Consume '='
            parse_E(tokens)
        else:
            # Handle error: Expected '=' after '<IDENTIFIER> Vb+'
            pass
    else:
        parse_Vl(tokens)
        if tokens and tokens[0].content == '=':
            tokens.pop(0)  # Consume '='
            parse_E(tokens)

def parse_Vb(tokens):
    # Implementation for parsing Vb rule
    # Example:
    # Vb -> '<IDENTIFIER>' Vb+
    #    | '(' Vl ')' Vb+
    #    | '(' ')' => '()'
    if tokens and tokens[0].content == '(':
        tokens.pop(0)  # Consume '('
        if tokens and tokens[0].content == ')':
            tokens.pop(0)  # Consume ')'
        else:
            parse_Vl(tokens)
            if tokens and tokens[0].content == ')':
                tokens.pop(0)  # Consume ')'
            else:
                # Handle error: Expected ')' after Vl
                pass
    elif tokens and tokens[0].type == 'IDENTIFIER':
        tokens.pop(0)  # Consume '<IDENTIFIER>'
    else:
        # Handle error: Expected '<IDENTIFIER>' or '('
        pass

def parse_Vl(tokens):
    # Implementation for parsing Vl rule
    # Example:
    # Vl -> '<IDENTIFIER>' list ','
    if tokens and tokens[0].type == 'IDENTIFIER':
        tokens.pop(0)  # Consume '<IDENTIFIER>'
    else:
        # Handle error: Expected '<IDENTIFIER>' after '('
        pass


file_name = input()
tokens = screen(file_name)
ast = parse_program(tokens)