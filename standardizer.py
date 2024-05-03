from rpal_parser import parse

def standardize(ast):
    # This function will standardize the AST.
    # The AST will be traversed and the standardization will be done in a bottom-up manner.
    if ast[0] == 'let':
        print("let")
        print(ast[1])
        print(ast[2])
        print(ast[3])


prog_file = input()

tree = parse(prog_file)
standardize(tree)