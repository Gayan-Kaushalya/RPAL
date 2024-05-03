from rpal_token import Token

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'
underscore = '_'
operators = '+-*<>&.@/:=~|$!#%^_[]{}\"\'?'
punctuation = '();,'
newline = '\n'


# Must check whether we can remove the following three lines.
token_names = []
tokens = []
characters = []
line_numbers = []


def tokenize(characters):  
    i = 0
    current_token = ''
    line_number = 1
    
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
                line_numbers.append(line_number)
                
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
                line_numbers.append(line_number)
                
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
                line_numbers.append(line_number)
                
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
                line_numbers.append(line_number)
                
                current_token = ''  
            
            # Separating puntuation
            elif characters[i] in punctuation:
                current_token += characters[i]
                tokens.append(current_token)
                token_names.append(current_token)
                line_numbers.append(line_number)
                
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
                line_numbers.append(line_number)
                
                current_token = ''
                
            # Separating newlines
            elif characters[i] == '\n':
                tokens.append(newline)
                token_names.append('<DELETE>')
                line_numbers.append(line_number)
                line_number += 1
                
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
                            line_numbers.append(line_number)
                            break
                        
                    if characters[i] == "'":
                        if characters[i+1] == "'":
                            tokens.append(current_token)
                            token_names.append('<OPERATOR>')
                            current_token = ''
                            line_numbers.append(line_number)
                            break
                    
                    current_token += characters[i]
                    i += 1
                    
                tokens.append(current_token)
                token_names.append('<OPERATOR>')
                line_numbers.append(line_number)
                
                current_token = ''

            ## What is this? How does this work? identifier starting with __
            else:
                print(f"Invalid token: {characters[i]} at position {i}")
                i += 1
                  
    except IndexError:
        pass
    
    number_of_tokens = len(tokens)

    for i in range(number_of_tokens):
        if i == 0:
            tokens[i] = Token(tokens[i], token_names[i], line_numbers[i], None, token_names[i+1])
            tokens[i].make_first_token()
        elif i == number_of_tokens - 1:
            
            # We have to handle cases where last token is the newline character.
            if tokens[i] == '\n':
                tokens[i - 1].make_last_token()
                tokens.remove(tokens[i])
                token_names.remove(token_names[i])
                line_numbers.remove(line_numbers[i])
            else:
                tokens[i] = Token(tokens[i], token_names[i], line_numbers[i], token_names[i-1], None)
                tokens[i].make_last_token()

        else:
            tokens[i] = Token(tokens[i], token_names[i], line_numbers[i], token_names[i-1], token_names[i+1])
            
    return tokens  