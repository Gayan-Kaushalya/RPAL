import re

# Your input string
input_string = input()

# Split the string using regular expression
result_list = re.findall('\s+|\w+|[+\-<>&.@/:=~|$!#%^_[\]{}"\'\\\\]+', input_string)

# Output the result list
print(result_list)


RE_IDENTIFIER = r'(?P<IDENTIFIER>[a-zA-Z][a-zA-Z0-9_]*)'
#RE_INTEGER = r'(?P<INTEGER>[0-9]+!\D+)'
RE_INTEGER = r'(?P<INTEGER>[0-9]+)(?![a-zA-Z])'
RE_OPERATORS = r'(?P<OPERATOR>[+\-<>&.@/:=~|$!#%^_[\]{}"\'\\]+)'

RE_STRING = r"(?P<STRING>'(?:\\t|\\n|\\\\|\\\"|\\'|[();, A-Za-z0-9+\-<>\.@/:=~\|\$!#%^_\[\]\{\}\"\'\?\s])*')"
RE_SPACES = r'(?P<DELETE>[" "|ht|Eol]+)'
RE_COMMENT = r"(?P<DELETE>//(?:[;,\(\)\\\"[a-zA-Z][0-9]+|\+|\-|\*|<|>|&|\.|@|/|:|=|~|\||\$|!|#|%|\^|\[|\]|\{|\}|\"|\'])*Eol)"

RE_PUNCTION1 = r'(?P<OPENBRACKET>\()'
RE_PUNCTION2 = r'(?P<CLOSEBRACKET>\))'
RE_PUNCTION3 = r'(?P<SEMICOLON>\;)'
RE_PUNCTION4 = r'(?P<COMMA>\,)'

#RE_OPERATORS = r'(?P<OPERATOR>[+-*<>&.@/:=~\|$!#%^[]{}\"\'?]+)'
#RE_STRING = r'(?P<STRING>\'\'\'(\\t|\\n|\\\\|\\\"|(|)|\;|\,|\'\'|[A-Za-z]|[0-9]|+|-|*|<|>|&|.|@|/|:|=|~|\||$|!|#|%|^|_|[|]|{|}|\"|\'|?])* \'\'\')'
#RE_STRING = r'(?P<STRING>(?:\'\'\'|\\t|\\n|\\\\|\\\"|\(|\)|\;|\,|\'\'|[A-Za-z]|[0-9]|[+\-*<>\.@/:=~\|\$!#%^_\[\]\{\}\"\'\?])*)'
#RE_COMMENT = r'(?P<DELETE>//[\"|(|)|\;|\,|\\| |ht|[a-zA-Z]|[0-9]|[+|-|*|<|>|&|.|@|/|:|=|~|\||$|!|#|%|^| |[|]|{|}|\"|\'|?]]*Eol)'


for token in result_list:
    if re.match(RE_IDENTIFIER, token):
        print(f"<IDENTIFIER>: {token}")
    elif re.match(RE_INTEGER, token):
        print(f"<INTEGER>: {token}")
    elif re.match(RE_OPERATORS, token):
        print(f"<OPERATOR>: {token}")
    elif re.match(RE_STRING, token):
        print(f"<STRING>: {token}")
    elif re.match(RE_SPACES, token):
        print(f"<DELETE>: {token}")
    elif re.match(RE_COMMENT, token):
        print(f"<DELETE>: {token}")
    elif re.match(RE_PUNCTION1, token):
        print(f"< ( >: {token}")
    elif re.match(RE_PUNCTION2, token):
        print(f"< ) >: {token}")
    elif re.match(RE_PUNCTION3, token):
        print(f"< ; >: {token}")
    elif re.match(RE_PUNCTION4, token):
        print(f"< , >: {token}")
    else:
        print(f"<INVALID>: {token}")
        
    
    
print(input_string)