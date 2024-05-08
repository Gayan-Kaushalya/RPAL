from src.rpal_parser import *

prog_file = input()

tree = parse(prog_file)
print_tree(tree)