from src.standardizer import standardize
from src.node import *
from src.environment import Environment

control_structures = []
count = 0
control = []
stack = []
environments = [Environment(0, None)]
current_environment = 0
builtInFunctions = ["Order", "Print", "print", "Conc", "Stern", "Stem", "Isinteger", "Istruthvalue", "Isstring", "Istuple", "Isfunction", "ItoS"]
print_present = False


def generate_control_structure(root, i):
    global count
    
    while(len(control_structures) <= i):
        control_structures.append([])

    # When lambda is encountered, we need to generate a new control structure.
    if (root.value == "lambda"):
        count += 1
        left_child = root.children[0]
        if (left_child.value == ","):
            temp = "lambda" + "_" + str(count) + "_"
            for child in left_child.children:
                temp += child.value[4:-1] + ","
            temp = temp[:-1]
            control_structures[i].append(temp)
        else:
            temp = "lambda" + "_" + str(count) + "_" + left_child.value[4:-1]
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

    elif (root.value == "tau"):
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
    
def built_in(function, argument):
    global print_present
    
    # The Order function returns the length of a tuple.  
    if (function == "Order"):
        order = len(argument)
        stack.append(order)

    # The Print function prints the output to the command prompt.
    elif (function == "Print" or function == "print"):
        # We should print the output only when the 'Print' function is called in the program.
        print_present = True
        
        # If there are escape characters in the string, we need to format it properly.
        if type(argument) == str:
            if "\\n" in argument:
                argument = argument.replace("\\n", "\n")
            if "\\t" in argument:
                argument = argument.replace("\\t", "\t")

        stack.append(argument)

    # The Conc function concatenates two strings.
    elif (function == "Conc"):
        stack_symbol = stack.pop()
        control.pop()
        temp = argument + stack_symbol
        stack.append(temp)

    # The Stern function returns the string without the first letter.
    elif (function == "Stern"):
        stack.append(argument[1:])

    # The Stem function returns the first letter of the given string.
    elif (function == "Stem"):
        stack.append(argument[0])

    # The Isinteger function checks if the given argument is an integer.
    elif (function == "Isinteger"):
        if (type(argument) == int):
            stack.append(True)
        else:
            stack.append(False)

    # The Istruthvalue function checks if the given argument is a boolean value.               
    elif (function == "Istruthvalue"):
        if (type(argument) == bool):
            stack.append(True)
        else:
            stack.append(False)

    # The Isstring function checks if the given argument is a string.
    elif (function == "Isstring"):
        if (type(argument) == str):
            stack.append(True)
        else:
            stack.append(False)

    # The Istuple function checks if the given argument is a tuple.
    elif (function == "Istuple"):
        if (type(argument) == tuple):
            stack.append(True)
        else:
            stack.append(False)

    # The Isfunction function checks if the given argument is a built-in function.
    elif (function == "Isfunction"):
        if (argument in builtInFunctions):
            return True
        else:
            False
    
    # The ItoS function converts integers to strings.        
    elif (function == "ItoS"):
        if (type(argument) == int):
            stack.append(str(argument))
        else:
            print("Error: ItoS function can only accept integers.")
            exit()

def apply_rules():
    op = ["+", "-", "*", "/", "**", "gr", "ge", "ls", "le", "eq", "ne", "or", "&", "aug"]
    uop = ["neg", "not"]

    global control
    global current_environment

    while(len(control) > 0):
     
        symbol = control.pop()

        # Rule 1
        if (symbol[0] == "<" and symbol[-1] == ">"):
            stack.append(lookup(symbol))

        # Rule 2
        elif (symbol[0:6] == "lambda"):
            stack.append(symbol+"_"+str(current_environment))

        # Rule 4
        elif (symbol == "gamma"):
            stack_symbol_1 = stack.pop()
            stack_symbol_2 = stack.pop()

            if (type(stack_symbol_1) == str and stack_symbol_1[0:6] == "lambda"):
                current_environment = len(environments)
                lambda_data = stack_symbol_1.split("_")
                
                # In some cases, there may be prases like 'lambda_2_Rec_F_0'. We need to handle this case.
                if (len(lambda_data) > 4):
                    temp = "_".join(lambda_data[2:-1])
                    lambda_data = [lambda_data[0], lambda_data[1], temp, lambda_data[-1]]
                
                lambda_number = int(lambda_data[1])
                bounded_variable = lambda_data[2]
                parent_environment_number = int(lambda_data[3])

                parent = environments[parent_environment_number]
                child = Environment(current_environment, parent)
                parent.add_child(child)
                environments.append(child)

                # Rule 11
                variable_list = bounded_variable.split(",")
                
                if (len(variable_list) > 1):
                    for i in range(len(variable_list)):
                        child.add_variable(variable_list[i], stack_symbol_2[i])
                else:
                    child.add_variable(bounded_variable, stack_symbol_2)

                stack.append(child.name)
                control.append(child.name)
                control += control_structures[int(lambda_number)]

            # Rule 10
            elif (type(stack_symbol_1) == tuple):
                stack.append(stack_symbol_1[stack_symbol_2-1])

            # Rule 12
            elif (stack_symbol_1 == "Y*"):
                temp = "eta" + stack_symbol_2[6:]
                stack.append(temp)

            # Rule 13
            elif (type(stack_symbol_1) == str and stack_symbol_1[0:3] == "eta"):
                temp = "lambda" + stack_symbol_1[3:]
                control.append("gamma")
                control.append("gamma")
                stack.append(stack_symbol_2)
                stack.append(stack_symbol_1)
                stack.append(temp)

            # Built-in functions
            elif stack_symbol_1 in builtInFunctions:
                built_in(stack_symbol_1, stack_symbol_2)
              
        # Rule 5
        elif (symbol[0:2] == "e_"):
            stack_symbol = stack.pop()
            stack.pop()
            
            if (current_environment != 0):
                for element in reversed(stack):
                    if (type(element) == str and element[0:2] == "e_"):
                        current_environment = int(element[2:])
                        break
            stack.append(stack_symbol)

        # Rule 6
        elif (symbol in op):
            rand_1 = stack.pop()
            rand_2 = stack.pop()
            if (symbol == "+"): 
                stack.append(rand_1 + rand_2)
            elif (symbol == "-"):
                stack.append(rand_1 - rand_2)
            elif (symbol == "*"):
                stack.append(rand_1 * rand_2)
            elif (symbol == "/"):
                stack.append(rand_1 // rand_2)
            elif (symbol == "**"):
                stack.append(rand_1 ** rand_2)
            elif (symbol == "gr"):
                stack.append(rand_1 > rand_2)
            elif (symbol == "ge"):
                stack.append(rand_1 >= rand_2)
            elif (symbol == "ls"):
                stack.append(rand_1 < rand_2)
            elif (symbol == "le"):
                stack.append(rand_1 <= rand_2)
            elif (symbol == "eq"):
                stack.append(rand_1 == rand_2)
            elif (symbol == "ne"):
                stack.append(rand_1 != rand_2)
            elif (symbol == "or"):
                stack.append(rand_1 or rand_2)
            elif (symbol == "&"):
                stack.append(rand_1 and rand_2)
            elif (symbol == "aug"):
                if (type(rand_2) == tuple):
                    stack.append(rand_1 + rand_2)
                else:
                    stack.append(rand_1 + (rand_2,))

        # Rule 7
        elif (symbol in uop):
            rand = stack.pop()
            if (symbol == "not"):
                stack.append(not rand)
            elif (symbol == "neg"):
                stack.append(-rand)

        # Rule 8
        elif (symbol == "beta"):
            B = stack.pop()
            delta_else = control.pop()
            delta_then = control.pop()
            if (B):
                control += control_structures[int(delta_then.split('_')[1])]
            else:
                control += control_structures[int(delta_else.split('_')[1])]

        # Rule 9
        elif (symbol[0:4] == "tau_"):
            n = int(symbol.split("_")[1])
            tau_list = []
            for i in range(n):
                tau_list.append(stack.pop())
            tau_tuple = tuple(tau_list)
            stack.append(tau_tuple)

        elif (symbol == "Y*"):
            stack.append(symbol)

    # Lambda expression becomes a lambda closure when its environment is determined.
    if type(stack[0]) == str and stack[0][:7] == "lambda_":
        lambda_info = stack[0].split("_")
        
        stack[0] = "[lambda closure: " + lambda_info[2] + ": " + lambda_info[1] + "]"
         
    if type(stack[0]) == tuple:
        # The rpal.exe program does not print the comma when there is only one element in the tuple.
        # Our code must emulate this behaviour.  
        if len(stack[0]) == 1:
            stack[0] = "(" + str(stack[0][0]) + ")"
        
        # The rpal.exe program does not print inverted commas when all the elements in the tuple are strings.
        # Our code must emulate this behaviour too. 
        else: 
            if all(type(element) == str for element in stack[0]):
                temp = "("
                for element in stack[0]:
                    temp += element + ", "
                temp = temp[:-2] + ")"
                stack[0] = temp
                
    # The rpal.exe program prints the boolean values in lowercase. Our code must emulate this behaviour.    
    if stack[0] == True or stack[0] == False:
        stack[0] = str(stack[0]).lower()

# This function is called from the myrpal.py file.
def get_result(file_name):
    global control

    st = standardize(file_name)
    
    generate_control_structure(st,0) 
    
    control.append(environments[0].name)
    control += control_structures[0]

    stack.append(environments[0].name)

    apply_rules()

    if print_present:
        print(stack[0])