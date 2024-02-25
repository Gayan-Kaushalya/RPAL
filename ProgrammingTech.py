#from tokenizer import word_tokenize
import tokenizer,re
#nltk.download('punkt') 

input_program = input()

tokens = tokenizer.wordpunct_tokenize(input_program)
print(tokens)

keywords = "let"


# Categorizing the tokens

for token in tokens:
    if re.match(r"^[a-zA-Z0-9_]*$", token):
        if token in keywords:
            print(token, "is a keyword")
        else:
            print(token, "is an identifier")
            
            
            # findall