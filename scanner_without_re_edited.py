letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'
underscore = '_'
operators = '+-*<>&.@/:=~|$!#%^_[]{}\"\'?'
punctuation = '();,'
newline = '\n'

token_names = []
tokens = []
characters = []


def tokenize(characters):  
    i = 0
    current_token = ''
    
    try:
        while i < len(characters):
            # Separating identifiers
            if characters[i] in letters:
                current_token += characters[i]
                i += 1
                
                while i < len(characters) and (characters[i] in letters or characters[i] in digits or characters[i] == underscore):
                    current_token += characters[i]
                    i += 1
                    
                tokens.append(current_token)
                token_names.append('<IDENTIFIER>')
                
                current_token = ''
                
            # Separating integers    
            elif characters[i] in digits:
                current_token += characters[i]
                i += 1
                
                # We have to detect invalid tokens such as 123a
                while i < len(characters): 
                    if characters[i] in digits:
                        current_token += characters[i]
                        i += 1
                    if characters[i] in letters:
                        current_token += characters[i]
                        i += 1
                    else:
                        break
                    
                    
                tokens.append(current_token)
                
                # If the token only has digits, we classify it as an integer. Otherwise, we classify it as an invalid token.
                try:
                    current_token = int(current_token)
                except:
                    token_names.append('<INVALID>')
                    
                else:
                    token_names.append('<INTEGER>')
                
                current_token = ''
                
            # Separating comments
            # Comments should start with // and end with Eol.
            elif characters[i] == '/' and characters[i+1] == '/':
                current_token += characters[i]
                current_token += characters[i+1]
                i += 2
                
                while i < len(characters) and characters[i] != '\n':
                    current_token += characters[i]
                    i += 1
                    
                tokens.append(current_token)
                token_names.append('<DELETE>')
                
                current_token = ''
                
            # Separating strings
            # Stings should start with '' and end with ''.  
            elif characters[i] == "'" and characters[i+1] == "'":
                current_token += characters[i]
                current_token += characters[i+1]
                i += 2
                
                while i < len(characters):
                    if characters[i] == "'" and characters[i+1] == "'":
                        current_token += characters[i]
                        current_token += characters[i+1]
                        i += 2
                        break
                    else:
                        #####The strings can contain only a set of characters. That should be checked
                        current_token += characters[i]
                        i += 1
                        
                tokens.append(current_token)
                token_names.append('<STRING>')
                
                current_token = ''  
            
            # Separating puntuation
            elif characters[i] in punctuation:
                current_token += characters[i]
                tokens.append(current_token)
                token_names.append('<PUNCT>')
                
                current_token = '' 
                
                i += 1
                
            # Separating spaces
            # Multiple spaces should be considered as one space.
            elif characters[i] == ' ' or characters[i] == '\t':
                current_token += characters[i]
                i += 1
                
                while i < len(characters) and (characters[i] == ' ' or characters[i] == '\t'):
                    current_token += characters[i]
                    i += 1
                    
                tokens.append(current_token)
                token_names.append('<DELETE>')
                
                current_token = ''
                
            # Separating newlines
            elif characters[i] == '\n':
                tokens.append(newline)
                token_names.append('<DELETE>')
                
                i += 1
                
            # Separating operators
            # While doing this we should be careful about the case of '' and //.
            elif characters[i] in operators:
                while i < len(characters) and characters[i] in operators:
                    if characters[i] == '/':
                        if characters[i+1] == '/':
                            tokens.append(current_token)
                            token_names.append('<OPERATOR>')
                            current_token = ''
                            break
                        
                    if characters[i] == "'":
                        if characters[i+1] == "'":
                            tokens.append(current_token)
                            token_names.append('<OPERATOR>')
                            current_token = ''
                            break
                    
                    current_token += characters[i]
                    i += 1
                    
                tokens.append(current_token)
                token_names.append('<OPERATOR>')
                
                current_token = ''

            ## What is this? How does this work?
            else:
                print(f"Invalid token: {characters[i]} at position {i}")
                i += 1
                  
    except IndexError:
        pass

try:
    with open(input(), 'r') as file:
        # rest of your code
        for line in file:
            for character in line:
                characters.append(character)
            tokenize(line)
            characters.clear()
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print("An error occurred:", e)

#Create a list of tuples with the tokens and their names
token_list = [(tokens[i], token_names[i]) for i in range(len(tokens))]
for x in token_list:
    print("'"+x[0]+"'"+':'+x[1])

