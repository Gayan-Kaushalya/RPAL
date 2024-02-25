import nltk   # Import the Natural Language Toolkit
import re     # Import the Regular Expression module

file_name = input("Enter the file name: ")
#input_program = open(file_name, "r").read()
#input_program = input("Enter the program: ")
input_program_tokens = nltk.wordpunct_tokenize(file_name)

print(input_program_tokens)

#RE_KEYWORD = r'(?P<KEYWORD>if|else|while|for|do|break|continue|return|switch|case|default|goto|auto|extern|register|static|typedef|const|volatile|inline|restrict|sizeof|alignof|_Alignas|_Alignof|_Atomic|_Bool|_Complex|_Generic|_Imaginary|_Noreturn|_Static_assert|_Thread_local)'
RE_IDENTIFIER = r'(?P<IDENTIFIER>[a-zA-Z][a-zA-Z0-9_]*)'
RE_INTEGER = r'(?P<INTEGER>[0-9]+)'
RE_OPERATORS = r'(?P<OPERATOR>[+\-<>&.@/:=~|$!#%^_[\]{}"\']+)'
#RE_OPERATORS = r'(?P<OPERATOR>[+-*<>&.@/:=~\|$!#%^[]{}\"\'?]+)'
#RE_STRING = r'(?P<STRING>\'\'\'(\\t|\\n|\\\\|\\\"|(|)|\;|\,|\'\'|[A-Za-z]|[0-9]|+|-|*|<|>|&|.|@|/|:|=|~|\||$|!|#|%|^|_|[|]|{|}|\"|\'|?])* \'\'\')'
#RE_STRING = r'(?P<STRING>(?:\'\'\'|\\t|\\n|\\\\|\\\"|\(|\)|\;|\,|\'\'|[A-Za-z]|[0-9]|[+\-*<>\.@/:=~\|\$!#%^_\[\]\{\}\"\'\?])*)'
RE_STRING = r"(?P<STRING>'(?:\\t|\\n|\\\\|\\\"|\\'|[();, A-Za-z0-9+\-<>\.@/:=~\|\$!#%^_\[\]\{\}\"\'\?\s])*')"
RE_SPACES = r'(?P<DELETE>[' '|ht|Eol]+)'
RE_COMMENT = r"(?P<DELETE>//(?:[;,\(\)\\\"[a-zA-Z][0-9]+|\+|\-|\*|<|>|&|\.|@|/|:|=|~|\||\$|!|#|%|\^|\[|\]|\{|\}|\"|\'])*Eol)"
#RE_COMMENT = r'(?P<DELETE>//[\"|(|)|\;|\,|\\| |ht|[a-zA-Z]|[0-9]|[+|-|*|<|>|&|.|@|/|:|=|~|\||$|!|#|%|^| |[|]|{|}|\"|\'|?]]*Eol)'
RE_PUNCTION1 = r'(?P<OPENBRACKET>\()'
RE_PUNCTION2 = r'(?P<CLOSEBRACKET>\))'
RE_PUNCTION3 = r'(?P<SEMICOLON>\;)'
RE_PUNCTION4 = r'(?P<COMMA>\,)'

for token in input_program_tokens:
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