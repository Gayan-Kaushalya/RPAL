from lexical_analyzer import tokenize

keywords = [
    "let",
    "in",
    "where",
    "rec",
    "fn" ,          
    "aug",
    "or",
    "not",
    "gr",
    "ge",
    "ls",
    "le",
    "eq",
    "ne",
    "true",
    "false",
    "nil",
    "dummy",
    "within",
    "and",
]

characters = []

def screen(file_name):
    token_list = []
    invalid_token_present = False
    invalid_token = None
    
    try:
        with open(file_name, 'r') as file:
            for line in file:
                for character in line:
                    characters.append(character)
            token_list = tokenize(characters)
            characters.clear()
    except FileNotFoundError:
        print("File not found.")
        exit(1)
    except Exception as e:
        print("An error occurred:", e)
        exit(1)
    
    # Iterate through token list in reverse order. This reverse iteration will correctly handle the consequent <DELETE>s
    for i in range(len(token_list) - 1, -1, -1):
        token = token_list[i]
        
        if token.type == "<IDENTIFIER>" and token.content in keywords:
            token.make_keyword()
        
        if token.type == "<DELETE>" or token.content == "\n":
            if i < len(token_list) - 1:
                token_list[i + 1].previous_type = token.previous_type
            
            if i > 0:
                token_list[i - 1].next_type = token.next_type
            
            token_list.remove(token)
            
        if token.type == "<INVALID>":
            if invalid_token_present == False:
                invalid_token = token
                
            invalid_token_present = True
        
    return token_list, invalid_token_present, invalid_token