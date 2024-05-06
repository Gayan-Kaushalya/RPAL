from standardizer import standardize
from node import *

class EnvironmentNode(object):
    def __init__(self, number, parent):
        self.name = "e_" + str(number)
        self.variables = {}
        self.children = []
        self.parent = parent
    def addChild(self, node):
        self.children.append(node)
        node.variables.update(self.variables)
    def addVariable(self, key, value):
        self.variables[key] = value

controlStructures = []
count = 0
control = []
stack = []
environments = [EnvironmentNode(0, None)]
currentEnvironment = 0
builtInFunctions = ["Order", "Print", "print", "Conc", "Stern", "Stem", "Isinteger", "Istruthvalue", "Isstring", "Istuple", "Isfunction"]


def generateControlStructure(root, i):
    global controlStructures
    global count
    
    while(len(controlStructures) <= i):
        controlStructures.append([])

    if (root.value == "lambda"):
        count += 1
        leftChild = root.children[0]
        if(leftChild.value == ","):
            temp = "lambda" + "_" + str(count) + "_"
            for child in leftChild.children:
                temp += child.value[4:-1] + ","
            temp = temp[:-1]
            controlStructures[i].append(temp)
        else:
            temp = "lambda" + "_" + str(count) + "_" + leftChild.value[4:-1]
            controlStructures[i].append(temp)

        for child in root.children[1:]:
            generateControlStructure(child, count)

    elif (root.value == "->"):
        count += 1
        temp = "delta" + "_" + str(count)
        controlStructures[i].append(temp)
        generateControlStructure(root.children[1], count)
        count += 1
        temp = "delta" + "_" + str(count)
        controlStructures[i].append(temp)
        generateControlStructure(root.children[2], count)
        controlStructures[i].append("beta")
        generateControlStructure(root.children[0], i)

    elif(root.value == "tau"):
        n = len(root.children)
        temp = "tau" + "_" + str(n)
        controlStructures[i].append(temp)
        for child in root.children:
            generateControlStructure(child, i)

    else:
        controlStructures[i].append(root.value)
        for child in root.children:
            generateControlStructure(child, i)





def lookup(name):
    global environments
    global builtInFunctions
    global stack
    if(name.startswith("INT", 1)):
        return int(name[5:-1])
    elif(name.startswith("STR", 1)):
        return name[5:-1].strip("'")
    elif(name.startswith("ID", 1)):
        variable = name[4:-1]
        if (variable in builtInFunctions):
            return variable
        else:
            value = environments[currentEnvironment].variables[variable]
            return value
    elif(name.startswith("Y*", 1)):
        return "Y*"
    elif(name.startswith("nil", 1)):
        return ()
    elif(name.startswith("true", 1)):
        return True
    elif(name.startswith("false", 1)):
        return False

def applyRules():
    binop = ["+", "-", "*", "/", "**", "gr", "ge","ls", "le", "eq", "ne", "or", "&", "aug"]
    unop = ["neg","not"]

    global control
    global stack
    global environments
    global currentEnvironment

    while(len(control) > 0):  

        symbol = control.pop()

        #Rule 1
        if(symbol.startswith("<") and symbol.endswith(">")):
            stack.append(lookup(symbol))

        #Rule 2
        elif(symbol.startswith("lambda")):
            stack.append(symbol+"_"+str(currentEnvironment))

        #Rule 4
        elif(symbol == "gamma"):
            stack_symbol_1 = stack.pop()
            stack_symbol_2 = stack.pop()

            if(type(stack_symbol_1) == str and stack_symbol_1.startswith("lambda")):
                currentEnvironment = len(environments)
                lambdaData = stack_symbol_1.split("_")

                parent = environments[int(lambdaData[3])]
                child = EnvironmentNode(currentEnvironment, parent)
                parent.addChild(child)
                environments.append(child)

                #Rule 11
                variablesList = lambdaData[2].split(",")
                if(len(variablesList)>1):
                    for i in range(len(variablesList)):
                        child.addVariable(variablesList[i],stack_symbol_2[i])
                else:
                    child.addVariable(lambdaData[2],stack_symbol_2)

                stack.append(child.name)
                control.append(child.name)
                control += controlStructures[int(lambdaData[1])]

            #Rule 10
            elif(type(stack_symbol_1) == tuple):
                stack.append(stack_symbol_1[stack_symbol_2-1])

            #Rule 12
            elif(stack_symbol_1 == "Y*"):
                temp = "eta" + stack_symbol_2[6:]
                stack.append(temp)

            #Rule 13
            elif(type(stack_symbol_1) == str and stack_symbol_1.startswith("eta")):
                temp = "lambda" + stack_symbol_1[3:]
                control.append("gamma")
                control.append("gamma")
                stack.append(stack_symbol_2)
                stack.append(stack_symbol_1)
                stack.append(temp)

            #built in
            elif(stack_symbol_1 == "Order"):
                order = len(stack_symbol_2)
                stack.append(order)

            elif(stack_symbol_1 == "Print" or stack_symbol_1 == "print"):
                # If there are escape characters in the string, we need to format it properly.
                if type(stack_symbol_2) == str:
                    if "\\n" in stack_symbol_2:
                        stack_symbol_2 = stack_symbol_2.replace("\\n", "\n")
                    if "\\t" in stack_symbol_2:
                        stack_symbol_2 = stack_symbol_2.replace("\\t", "\t")
 
              #  print(stack_symbol_2)
                stack.append(stack_symbol_2)

            elif(stack_symbol_1 == "Conc"):
                stack_symbol_3 = stack.pop()
                control.pop()
                temp = stack_symbol_2 + stack_symbol_3
                stack.append(temp)

            elif(stack_symbol_1 == "Stern"):
                stack.append(stack_symbol_2[1:])

            elif(stack_symbol_1 == "Stem"):
                stack.append(stack_symbol_2[0])

            elif(stack_symbol_1 == "Isinteger"):
                if(type(stack_symbol_2) == int):
                    stack.append(True)
                else:
                    stack.append(False)
                
            elif(stack_symbol_1 == "Istruthvalue"):
                if(type(stack_symbol_2) == bool):
                    stack.append(True)
                else:
                    stack.append(False)

            elif(stack_symbol_1 == "Isstring"):
                if(type(stack_symbol_2) == str):
                    stack.append(True)
                else:
                    stack.append(False)

            elif(stack_symbol_1 == "Istuple"):
                if(type(stack_symbol_2) == tuple):
                    stack.append(True)
                else:
                    stack.append(False)

            elif(stack_symbol_1 == "Isfunction"):
                if(stack_symbol_2 in builtInFunctions):
                    return True
                else:
                    False

        #Rule 5
        elif(symbol.startswith("e_")):
            stack_symbol = stack.pop()
            stack.pop()
            if(currentEnvironment != 0):
                for element in reversed(stack):
                    if(type(element) == str and element.startswith("e_")):
                        currentEnvironment = int(element[2:])
                        break
            stack.append(stack_symbol)

        #Rule 6
        elif(symbol in binop):
            rand_1 = stack.pop()
            rand_2 = stack.pop()
            if(symbol == "+"):
                stack.append(rand_1+rand_2)
            elif(symbol == "-"):
                stack.append(rand_1-rand_2)
            elif(symbol == "*"):
                stack.append(rand_1*rand_2)
            elif(symbol == "/"):
                stack.append(rand_1//rand_2)
            elif(symbol == "**"):
                stack.append(rand_1**rand_2)
            elif(symbol == "gr"):
                stack.append(rand_1 > rand_2)
            elif(symbol == "ge"):
                stack.append(rand_1 >= rand_2)
            elif(symbol == "ls"):
                stack.append(rand_1 < rand_2)
            elif(symbol == "le"):
                stack.append(rand_1 <= rand_2)
            elif(symbol == "eq"):
                stack.append(rand_1 == rand_2)
            elif(symbol == "ne"):
                stack.append(rand_1 != rand_2)
            elif(symbol == "or"):
                stack.append(rand_1 or rand_2)
            elif(symbol == "&"):
                stack.append(rand_1 and rand_2)
            elif(symbol == "aug"):
                if(type(rand_2) == tuple):
                    stack.append(rand_1 + rand_2)
                else:
                    stack.append(rand_1+(rand_2,))

        #Rule 7
        elif(symbol in unop):
            rand = stack.pop()
            if(symbol == "not"):
                stack.append(not rand)
            elif(symbol == "-"):
                stack.append(-rand)

        #Rule 8
        elif(symbol == "beta"):
            B = stack.pop()
            deltaElse = control.pop()
            deltaThen = control.pop()
            if(B):
                control += controlStructures[int(deltaThen.split('_')[1])]
            else:
                control += controlStructures[int(deltaElse.split('_')[1])]

        #Rule 9
        elif(symbol.startswith("tau_")):
            n = int(symbol.split("_")[1])
            tauList = []
            for i in range(n):
                tauList.append(stack.pop())
            tauTuple = tuple(tauList)
            stack.append(tauTuple)

        elif(symbol == "Y*"):
            stack.append(symbol)


def get_result(file_name):
    global control

    st = standardize(file_name)
    
    generateControlStructure(st,0) 

    control.append(environments[0].name)
    control += controlStructures[0]

    stack.append(environments[0].name)

    applyRules()

    print(stack[0])