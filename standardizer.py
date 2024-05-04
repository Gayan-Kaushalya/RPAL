
from rpal_parser import *



def standardize(node):
    for child in node.children:
        standardize(child)

    if node.value == "let" and node.children[0].value == "=":
        child_0 = node.children[0]
        child_1 = node.children[1]

        node.children[1] = child_0.children[1]
        node.children[0].children[1] = child_1
        node.children[0].value = "lambda"
        node.value = "gamma"

    elif node.value == "where" and node.children[1].value == "=":
        child_0 = node.children[0] #p
        child_1 = node.children[1] #=

        node.children[0] = child_1.children[1]
        node.children[1].children[1] = child_0
        node.children[1].value = "lambda"
        node.children[0], node.children[1] = node.children[1], node.children[0]
        node.value = "gamma"

    elif node.value == "function_form":
        expression = node.children.pop()

        currentNode = node
        for i in range(len(node.children) - 1):
            lambdaNode = AST_Node("lambda")
            child = node.children.pop(1)
            lambdaNode.addChild(child)
            currentNode.addChild(lambdaNode)
            currentNode = lambdaNode

        currentNode.addChild(expression)

        node.value = "="

    elif node.value == "gamma" and len(node.children) > 2:
        expression = node.children.pop()

        currentNode = node
        for i in range(len(node.children) - 1):
            lambdaNode = AST_Node("lambda")
            child = node.children.pop(1)
            lambdaNode.addChild(child)
            currentNode.addChild(lambdaNode)
            currentNode = lambdaNode

        currentNode.addChild(expression)

    elif node.value == "within" and node.children[0].value == node.children[1].value == "=":
        child_0 = node.children[1].children[0]
        child_1 = AST_Node("gamma")

        child_1.addChild(AST_Node("lambda"))
        child_1.addChild(node.children[0].children[1])
        child_1.children[0].addChild(node.children[0].children[0])
        child_1.children[0].addChild(node.children[1].children[1])

        node.children[0] = child_0
        node.children[1] = child_1

        node.value = "="

    elif node.value == "@":
        expression = node.children.pop(0)
        identifier = node.children[0]

        gammaNode = AST_Node("gamma")
        gammaNode.addChild(identifier)
        gammaNode.addChild(expression)

        node.children[0] = gammaNode

        node.value = "gamma"

    elif node.value == "and":
        child_0 = AST_Node(",")
        child_1 = AST_Node("tau")

        for child in node.children:
            child_0.addChild(child.children[0])
            child_1.addChild(child.children[1])

        node.children.clear()

        node.addChild(child_0)
        node.addChild(child_1)

        node.value = "="

    elif node.value == "rec":
        temp = node.children.pop()
        temp.value = "lambda"

        gammaNode = AST_Node("gamma")
        gammaNode.addChild(AST_Node("<Y*>"))
        gammaNode.addChild(temp)

        node.addChild(temp.children[0])
        node.addChild(gammaNode)

        node.value = "="

    return node

prog_file = input()

ast = parse(prog_file)
st = standardize(ast)

preorder_traversal(st)