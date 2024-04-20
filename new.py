# Alternate E finction
def E(self):
        n = 0
        token = self.tokens[0]
        if token.type == "KEYWORD" and token.value in ["let", "fn"]:      
            if token.value == "let":
                self.tokens.pop(0)
                self.D()
                if self.tokens[0].value != "in":
                    print("Parse error at E: 'in' Expected")
                    return
                self.tokens.pop(0)
                self.E()
                self.AST.append(Node("let", "let", 2))            
            else:
                self.tokens.pop(0)  
                while self.tokens[0].type == "identifier" or self.tokens[0].value == "(":       
                    self.Vb()
                    n += 1
                if self.tokens[0].value != ".":
                    print("Parse error at E: '.' Expected")
                    return
                self.tokens.pop(0)
                self.E()
                self.AST.append(Node("lambda_", "lambda", n + 1))                    
        else:
            self.Ew()