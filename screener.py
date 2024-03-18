from scanner import tokenize

keywords = [
    "let",
    "in",
    "Print"
]

characters = []

try:
    with open(input(), 'r') as file:
        # rest of your code
        for line in file:
            for character in line:
                characters.append(character)
        token_list = tokenize(characters)
        characters.clear()
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print("An error occurred:", e)
    
for token in token_list:
    if token.type == "<IDENTIFIER>":
        if token.content in keywords:
            token.make_keyword()
            
    if token.type == "<DELETE>" or token.content == "\n":
        removing_index = token_list.index(token)
        
        token_list[removing_index - 1].next_token_type = token_list[removing_index + 1].type
        token_list[removing_index + 1].previous_token_type = token_list[removing_index - 1].type
        
        token_list.remove(token)
        
for token in token_list:
    print(token)