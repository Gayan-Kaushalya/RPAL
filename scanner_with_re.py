import re

RE_IDENTIFIER = r'[a-zA-Z][a-zA-Z0-9_]*'
RE_INTEGER = r"\b\d+\b"
RE_OPERATORS = r'[+\-<>&.@/:=~|$!#%^_[\]{}"\'\\]+'
RE_STRING = r"(?P<STRING>'(?:\\t|\\n|\\\\|\\\"|\\'|[();, A-Za-z0-9+\-<>\.@/:=~\|\$!#%^_\[\]\{\}\"\'\?\s])*')"
RE_SPACES = r'(?P<DELETE>[" "|\n]+)'
RE_COMMENT = r"^//(.*?)$"

RE_PUNCTION1 = r'(?P<OPENBRACKET>\()'
RE_PUNCTION2 = r'(?P<CLOSEBRACKET>\))'
RE_PUNCTION3 = r'(?P<SEMICOLON>\;)'
RE_PUNCTION4 = r'(?P<COMMA>\,)'


# Your input string
input_file = input("Enter the file name: ")

with open(input_file, 'r') as file:
    for line in file:
        input_string = line

        # Split the string using regular expression
        result_list = re.findall('\s+|\w+|[+\-<>&.@/:=~|$!#%^_[\]{}"\'\\\\]+', input_string)

        if ('//') in result_list:
            #get the first index of '\\\\'
            index = result_list.index('//')
            print(index)
           
            #concatenate all the elements from index to end of the list
            token = ''
            for x in result_list[index:]:
                token = token + x
            
            result_list = result_list[:index]
            result_list.append(token)
            
        if "''" in result_list:
            index = result_list.index("''")
            token = ''
            flag = True
            for x in result_list[index:]:
                token = token + x
                
                if x == "''":
                    flag = not flag
                if flag:
                    break
                
            result_list = result_list[:index]
            result_list.append(token)
            

        # Output the result list
        print(result_list)



        #RE_OPERATORS = r'(?P<OPERATOR>[+-*<>&.@/:=~\|$!#%^[]{}\"\'?]+)'
        #RE_STRING = r'(?P<STRING>\'\'\'(\\t|\\n|\\\\|\\\"|(|)|\;|\,|\'\'|[A-Za-z]|[0-9]|+|-||<|>|&|.|@|/|:|=|~|\||$|!|#|%|^|_|[|]|{|}|\"|\'|?]) \'\'\')'
        #RE_STRING = r'(?P<STRING>(?:\'\'\'|\\t|\\n|\\\\|\\\"|\(|\)|\;|\,|\'\'|[A-Za-z]|[0-9]|[+\-<>\.@/:=~\|\$!#%^_\[\]\{\}\"\'\?]))'
        #RE_COMMENT = r'(?P<DELETE>//[\"|(|)|\;|\,|\\| |ht|[a-zA-Z]|[0-9]|[+|-|*|<|>|&|.|@|/|:|=|~|\||$|!|#|%|^| |[|]|{|}|\"|\'|?]]*Eol)'


        for token in result_list:
            if re.match(RE_IDENTIFIER, token):
                print(f"<IDENTIFIER>: {token}")
            elif re.match(RE_INTEGER, token):
                print(f"<INTEGER>: {token}")
            elif re.match(RE_COMMENT, token):
                print(f"<DELETE>: {token}")
            elif re.match(RE_STRING, token):
                print(f"<STRING>: {token}")
            elif re.match(RE_OPERATORS, token):
                print(f"<OPERATOR>: {token}")
            
            elif re.match(RE_SPACES, token):
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