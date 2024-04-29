from ds_tokenizer import *

keywords = [
    "let",
    "in",
 #   "Print",         ## Is this a keyword?
    "where",
    "rec"
]

characters = []

def screen1(file_name):
 #   token_list = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                for character in line:
                    characters.append(character)
            la = LexicalAnalyser(file_name)
            token_list = la.lexical_analyser()
            characters.clear()
    except FileNotFoundError:
        print("File not found.")
        exit(1)
    except Exception as e:
        print("An error occurred:", e)
        exit(1)

    # This forward loop check doesn't remove consequent <DELETE> tokens
    ''' 
    for token in token_list:
        if token.type == "<IDENTIFIER>":
            if token.content in keywords:
                token.make_keyword()

        # Handled the case of removing the last element of the token_list        
        if (token.type == "<DELETE>" or token.content == "\n") and token_list.index(token)!=len(token_list)-1:
            removing_index = token_list.index(token)
            
            token_list[removing_index - 1].next_type = token_list[removing_index + 1].type
            token_list[removing_index + 1].previous_type = token_list[removing_index - 1].type
            
            token_list.remove(token)

        elif (token.type == "<DELETE>" or token.content == "\n") and token.is_last_token==True:
            last_index = token_list.index(token)

            token_list[last_index-1].make_last_token()
            token_list[last_index-1].next_type = None

            token_list.remove(token)
    '''
    
    # Iterate through token list in reverse order. This reverse iteration will correctly handle the consequent <DELETE>s
    for i in range(len(token_list) - 1, -1, -1):
        token = token_list[i]
        
        if token.type == "<IDENTIFIER>" and token.content in keywords:
            token.make_keyword()
        
        if token.type == "<DELETE>" or token.content == "\n":
            '''
            if i < len(token_list) - 1:
                token_list[i + 1].previous_type = token.previous_type
            
            if i > 0:
                token_list[i - 1].next_type = token.next_type
            '''
            token_list.remove(token)

    return token_list