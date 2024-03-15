letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'
underscore = '_'
operators = '+-*<>&.@/:=~|$!#%^_[]{}\"\'?'
punctuation = '();,'
newline = '\n'

tokens = []
characters = []


def tokenize(line):  
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
                
                current_token = ''
                
            # Separating integers    
            elif characters[i] in digits:
                current_token += characters[i]
                i += 1
                
                while i < len(characters) and characters[i] in digits:
                    current_token += characters[i]
                    i += 1
                    
                tokens.append(current_token)
                
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
                        current_token += characters[i]
                        i += 1
                        
                tokens.append(current_token)
                
                current_token = ''  
            
            # Separating puntuation
            elif characters[i] in punctuation:
                current_token += characters[i]
                tokens.append(current_token)
                
                current_token = ''
                
                i += 1
                
            # Separating spaces
            # Multiple spaces should be considered as one space.
            elif characters[i] == ' ' or characters[i] == '\t':
                current_token += characters[i]
                i += 1
                
                while i < len(characters) and (characters[i] == ' ' or characters[i] == '\t'):
                    i += 1
                    
                tokens.append(current_token)
                
                current_token = ''
                
            # Separating newlines
            elif characters[i] == '\n':
                tokens.append(newline)
                
                i += 1
                
            # Separating operators
            # While doing this we should be careful about the case of '' and //.
            elif characters[i] in operators:
                while i < len(characters) and characters[i] in operators:
                    if characters[i] == '/':
                        if characters[i+1] == '/':
                            tokens.append(current_token)
                            current_token = ''
                            break
                        
                    if characters[i] == "'":
                        if characters[i+1] == "'":
                            tokens.append(current_token)
                            current_token = ''
                            break
                    
                            
                
                    current_token += characters[i]
                    i += 1
                    
                tokens.append(current_token)
                
                current_token = ''
                  
    except IndexError:
        pass
    
    
with open(input(), 'r') as file:
    for line in file:
        for character in line:
            characters.append(character)
        tokenize(line)
        characters.clear()
        
print(tokens)  