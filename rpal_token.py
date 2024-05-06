class Token:
    def __init__(self, content, type, line):
        self.content = content
        self.type = type
        self.line = line
        self.is_first_token = False
        self.is_last_token = False
        
    def __str__(self):
        return f"{self.content} : {self.type}"
    
    def make_first_token(self):
        self.is_first_token = True
        
    def make_last_token(self):
        self.is_last_token = True
        
    def make_keyword(self):
        self.type = "<KEYWORD>"