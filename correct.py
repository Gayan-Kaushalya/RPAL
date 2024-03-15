# Creating a token class
class Token:
    def __init__(self, token, token_type):
        self.token = token
        self.token_type = token_type
        
    def __str__(self):
        return f"<{self.token_type}>: {self.token}"
    
    def __repr__(self):
        return f"<{self.token_type}>: {self.token}"
    
    def __eq__(self, other):
        return self.token == other.token and self.token_type == other.token_type
    
    def __ne__(self, other):
        return self.token != other.token or self.token_type != other.token_type
    
    def __hash__(self):
        return hash((self.token, self.token_type))
    
    def __lt__(self, other):
        return self.token < other.token
    
    def __le__(self, other):
        return self.token <= other.token
    
    def __gt__(self, other):
        return self.token > other.token
    
    def __ge__(self, other):
        return self.token >= other.token
    
    def __len__(self):
        return len(self.token)
    
    def __getitem__(self, index):
        return self.token[index]
    
    def __add__(self, other):
        return self.token + other.token
    
    def __radd__(self, other):
        return other.token + self.token
    
    def __mul__(self, other):
        return self.token * other
    
    def __rmul__(self, other):
        return other * self.token
    
    def __contains__(self, item):
        return item in self.token
    
    def __iter__(self):
        return iter(self.token)
    
    def __reversed__(self):
        return reversed(self.token)
    
    def __copy__(self):
        return Token(self.token, self.token_type)
    
   # def __deepcopy__(self, memo):
   #     return Token(copy.deepcopy(self.token, memo), self.token_type)
    
    def __bool__(self):
        return bool(self.token)
    
    def __format__(self, format_spec):
        return format(self.token, format_spec)
    
    def __index__(self):
        return self.token.index()
    
    
    
# Function to separate the tokens without using regular expressions
def tokenize(line):
    tokens = []
    token = ''
    i = 0
    while i < len(line):
        if line[i] in [' ', '\t']:
            if token:
                tokens.append(Token(token, 'UNKNOWN'))
                token = ''
            i += 1
        elif line[i] in ['+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '~', '|', '$', '!', '#', '%', '^', '_', '[', ']', '{', '}', '"', "'", '\\']:
            if token:
                tokens.append(Token(token, 'UNKNOWN'))
                token = ''
            tokens.append(Token(line[i], 'OPERATOR'))
            i += 1
        elif line[i] == '(':
            if token:
                tokens.append(Token(token, 'UNKNOWN'))
                token = ''
            if line[i:i+3] == '///':
                i += 3
                while line[i:i+3] != '///':
                    token += line[i]
                    i += 1
                token += '///'
                tokens.append(Token(token, 'STRING'))
                token = ''
                i += 3
            else:
                tokens.append(Token(line[i], 'UNKNOWN'))
                i += 1
        elif line[i] == "'":
            if token:
                tokens.append(Token(token, 'UNKNOWN'))
                token = ''
            if line[i:i+3] == "'''":
                i += 3
                while line[i:i+3] != "'''":
                    token += line[i]
                    i += 1
                token += "'''"
                tokens.append(Token(token, 'STRING'))
                token = ''
                i += 3
            else:
                tokens.append(Token(line[i], 'UNKNOWN'))
                i += 1
        else:
            token += line[i]
            i += 1
    if token:
        tokens.append(Token(token, 'UNKNOWN'))
    return tokens
    

# Reading the input file
input_file = input()
with open(input_file, 'r') as file:
    for line in input_file:
        tokens = tokenize(line)
        for token in tokens:
            print(token)
            
            