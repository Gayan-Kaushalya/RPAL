from scanner import tokenize

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
    print(token)
