from screener1 import screen1

file = input()
token_list = screen1(file)
#print(len(token_list))

with open("output1.txt", "w") as file:
    for token in token_list:
        file.write(f"{token.content} {token.type}\n")    
        