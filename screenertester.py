from screener import screen
file = input()
token_list = screen(file)
#print(len(token_list))

with open("output.txt", "w") as file:
    for token in token_list:
        file.write(f"{token.content} {token.type}\n")
        