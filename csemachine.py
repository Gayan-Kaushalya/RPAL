from standardizer import standardize
from node import *

class Environment(object):
    def __init__(self, number, parent_environment):
        self.name = "e_" + str(number)
        self.variables = {}
        self.children = []
        self.parent_environment = parent_environment
    def add_child(self, node):
        self.children.append(node)
        node.variables.update(self.variables)
    def add_variable(self, key, value):
        self.variables[key] = value

control_structures = []
count = 0                  # This is the control structure number.
control = []
stack = []
environments = [Environment(0, None)]
current_environment = 0
builtInFunctions = ["Order", "Print", "print", "Conc", "Stern", "Stem", "Isinteger", "Istruthvalue", "Isstring", "Istuple", "Isfunction"]


def generate_control_structure(root, i):
    # We need to keep track of the control structure number.
    global count
    
    while(len(control_structures) <= i):
        control_structures.append([])

    # When we encounter a lambda, we have to we have to create a new environment.
    if (root.value == "lambda"):
        count += 1
        left_child = root.children[0]
        
        # If the lambda has multiple arguments, we need to handle them differently.
        if (left_child.value == ","):
            temp = "lambda" + "_" + str(count) + "_"
            for child in left_child.children:
                temp += child.value[4:-1] + ","
            temp = temp[:-1]
            control_structures[i].append(temp)
        else:
            temp = "lambda" + "_" + str(count) + "_" + left_child.value[4:-1]
        #    print(temp)
          #  temp = "[lambda closure: " + left_child.value[4:-1] + "]"
            control_structures[i].append(temp)

        for child in root.children[1:]:
            generate_control_structure(child, count)

    elif (root.value == "->"):
        count += 1
        temp = "delta" + "_" + str(count)
        control_structures[i].append(temp)
        generate_control_structure(root.children[1], count)
        count += 1
        temp = "delta" + "_" + str(count)
        control_structures[i].append(temp)
        generate_control_structure(root.children[2], count)
        control_structures[i].append("beta")
        generate_control_structure(root.children[0], i)

    elif(root.value == "tau"):
        n = len(root.children)
        temp = "tau" + "_" + str(n)
        control_structures[i].append(temp)
        for child in root.children:
            generate_control_structure(child, i)

    else:
        control_structures[i].append(root.value)
        for child in root.children:
            generate_control_structure(child, i)





def lookup(name):
    if name[1:4] == "INT":
        return int(name[5:-1])
    
    elif name[1:4] == "STR":
        return name[5:-1].strip("'")
    
    elif name[1:3] == "ID":
        variable = name[4:-1]
        
        if (variable in builtInFunctions):
            return variable
        else:
            try:
                value = environments[current_environment].variables[variable]
            except KeyError:
                print("Undeclared Identifier: " + variable)
                exit(1)
            else:
                return value
            
    elif name[1:3] == "Y*":
        return "Y*"
    
    elif name[1:4] == "nil":
        return ()
    
    elif name[1:5] == "true":
        return True
    
    elif name[1:6] == "false":
        return False
    

def applyRules():
    op = ["+", "-", "*", "/", "**", "gr", "ge","ls", "le", "eq", "ne", "or", "&", "aug"]
    uop = ["neg","not"]

    global control
    global current_environment
    


    while (len(control) > 0):  
        symbol = control.pop()
   #     print(symbol)

        #Rule 1
        if (symbol[0] == "<" and symbol[-1] == ">"):
   #         print(symbol)
            stack.append(lookup(symbol))

        #Rule 2
        elif (symbol.startswith("lambda")):
            stack.append(symbol+"_"+str(current_environment))

        #Rule 4
        elif(symbol == "gamma"):
            stack_symbol_1 = stack.pop()
            stack_symbol_2 = stack.pop()

############# watch for this
            if stack_symbol_1[:6] == "lambda":
                current_environment = len(environments)
                
                lambda_info = stack_symbol_1.split("_")
                lambda_number = int(lambda_info[1])            #
                bounded_variable = lambda_info[2]              # Variable bouonded to lambda
                environment_number = int(lambda_info[3])       #

                parent_environment = environments[environment_number]
                child = Environment(current_environment, parent_environment)
                parent_environment.add_child(child)
                environments.append(child)

                #Rule 11
                variable_list = bounded_variable.split(",")
                
                if (len(variable_list) > 1):
                    for i in range(len(variable_list)):
                        child.add_variable(variable_list[i], stack_symbol_2[i])
                else:
                    child.add_variable(bounded_variable, stack_symbol_2)
                    
       #         print(child.variables)

                stack.append(child.name)
                control.append(child.name)
                control += control_structures[int(lambda_number)]

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
        elif (symbol.startswith("e_")):
            stack_symbol = stack.pop()
            stack.pop()
            
            if(current_environment != 0):
                for element in reversed(stack):
                    if(type(element) == str and element.startswith("e_")):
                        current_environment = int(element[2:])
                        break
            stack.append(stack_symbol)

        #Rule 6
        elif(symbol in op):
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
        elif(symbol in uop):
            rand = stack.pop()
            if(symbol == "not"):
                stack.append(not rand)
            elif(symbol == "-"):
                stack.append(-rand)

        #Rule 8
        elif(symbol == "beta"):
            B = stack.pop()
            delta_else = control.pop()
            delta_then = control.pop()
            if(B):
                control += control_structures[int(delta_then.split('_')[1])]
            else:
                control += control_structures[int(delta_else.split('_')[1])]

        #Rule 9
        elif(symbol.startswith("tau_")):
            n = int(symbol.split("_")[1])
            tau_list = []
            for i in range(n):
                tau_list.append(stack.pop())
            tau_tuple = tuple(tau_list)
            stack.append(tau_tuple)

        elif(symbol == "Y*"):
            stack.append(symbol)

    # Lambda expression becomes a lambda closure when its environment is determined.
    if stack[0][:7] == "lambda_":
        lambda_info = stack[0].split("_")
        
        stack[0] = "[lambda closure: " + lambda_info[2] + ": " + lambda_info[1] + "]"

def get_result(file_name):
    global control

    st = standardize(file_name)
    
    generate_control_structure(st,0) 
 #   print(control_structures)
   # print(environments)
    control.append(environments[0].name)
 #   print(environments[0].name)
    control += control_structures[0]
  #  print(control)

    stack.append(environments[0].name)

    applyRules()

    print(stack[0])