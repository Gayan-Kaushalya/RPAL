
from rpal_parser import *



def standardize(root):
    for child in root.children:
        standardize(child)

    if root.value == "let" and root.children[0].value == "=":
        child_0 = root.children[0]
        child_1 = root.children[1]

        root.children[1] = child_0.children[1]
        root.children[0].children[1] = child_1
        root.children[0].value = "lambda"
        root.value = "gamma"

    elif root.value == "where" and root.children[1].value == "=":
        child_0 = root.children[0] #p
        child_1 = root.children[1] #=

        root.children[0] = child_1.children[1]
        root.children[1].children[1] = child_0
        root.children[1].value = "lambda"
        root.children[0], root.children[1] = root.children[1], root.children[0]
        root.value = "gamma"

    elif root.value == "function_form":
        expression = root.children.pop()

        currentNode = root
        for i in range(len(root.children) - 1):
            lambdaNode = Node("lambda")
            child = root.children.pop(1)
            lambdaNode.children.append(child)
            currentNode.children.append(lambdaNode)
            currentNode = lambdaNode

        currentNode.children.append(expression)

        root.value = "="

    elif root.value == "gamma" and len(root.children) > 2:
        expression = root.children.pop()

        currentNode = root
        for i in range(len(root.children) - 1):
            lambdaNode = Node("lambda")
            child = root.children.pop(1)
            lambdaNode.children.append(child)
            currentNode.children.append(lambdaNode)
            currentNode = lambdaNode

        currentNode.children.append(expression)

    elif root.value == "within" and root.children[0].value == root.children[1].value == "=":
        child_0 = root.children[1].children[0]
        child_1 = Node("gamma")

        child_1.children.append(Node("lambda"))
        child_1.children.append(root.children[0].children[1])
        child_1.children[0].children.append(root.children[0].children[0])
        child_1.children[0].children.append(root.children[1].children[1])

        root.children[0] = child_0
        root.children[1] = child_1

        root.value = "="

    elif root.value == "@":
        expression = root.children.pop(0)
        identifier = root.children[0]

        gammaNode = Node("gamma")
        gammaNode.children.append(identifier)
        gammaNode.children.append(expression)

        root.children[0] = gammaNode

        root.value = "gamma"

    elif root.value == "and":
        child_0 = Node(",")
        child_1 = Node("tau")

        for child in root.children:
            child_0.children.append(child.children[0])
            child_1.children.append(child.children[1])

        root.children.clear()

        root.children.append(child_0)
        root.children.append(child_1)

        root.value = "="

    elif root.value == "rec":
        temp = root.children.pop()
        temp.value = "lambda"

        gammaNode = Node("gamma")
        gammaNode.children.append(Node("<Y*>"))
        gammaNode.children.append(temp)

        root.children.append(temp.children[0])
        root.children.append(gammaNode)

        root.value = "="

    return root

prog_file = input()

ast = parse(prog_file)
st = standardize(ast)

preorder_traversal(st)