from rpal_parser import parse

prog_file = input()

tree = parse(prog_file)

for child in tree.children:
    print(child.value)