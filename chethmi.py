from enum import Enum
from typing import List, Dict, Union
from xmlrpc.client import boolean
from biops import *

# Define the ObjectType enumeration
class ObjectType(Enum):
    LAMBDA = 1
    IDENTIFIER = 2
    INTEGER = 3
    STRING = 4
    GAMMA = 5
    OPERATOR = 6
    BETA = 7
    EETA = 8
    DELTA = 9
    TAU = 10
    ENV = 11
    LIST = 12
    BOOLEAN = 13


# Check if a string is an operator
def is_operator(label: str) -> bool:
    # Implement your logic for checking if label is an operator
    pass


class CSENode:
    def _init_(self, node_type: ObjectType, node_value: str = "", cs_index: int = 0, env: int = 0,
                 bound_variables: List[str] = None, list_elements: List['CSENode'] = None):
        self.node_type = node_type
        self.node_value = node_value
        self.cs_index = cs_index
        self.env = env
        self.bound_variables = bound_variables if bound_variables is not None else []
        self.list_elements = list_elements if list_elements is not None else []
        self.is_single_bound_var = not bound_variables

    def set_env(self, new_env: int) -> None:
        self.env = new_env


class ControlStructure:
    def _init_(self, cs_index: int):
        self.cs_index = cs_index
        self.nodes = []

    def add_node(self, node: CSENode) -> None:
        self.nodes.append(node)

    def pop_last_node(self) -> None:
        self.nodes.pop()

    def return_last_node(self) -> CSENode:
        return self.nodes.pop()

    def add_new_cs(self, cs: 'ControlStructure') -> None:
        self.nodes.extend(cs.nodes)


# Define built-in functions
built_in_functions = ["Print", "print", "Order", "Y*", "Conc", "Stem", "Stern", "Isinteger", "Isstring", "Istuple",
                      "Isempty", "dummy", "ItoS"]

class Stack:
    def _init_(self):
        self.nodes = []

    def add_node(self, node: 'CSENode') -> None:
        self.nodes.append(node)

    def pop_last_node(self) -> None:
        self.nodes.pop()

    def return_last_node(self) -> 'CSENode':
        return self.nodes.pop()

    def length(self) -> int:
        return len(self.nodes)


class Env:
    def _init_(self, parent_env=None):
        self.variables = {}
        self.lambdas = {}
        self.lists = {}
        self.parent_env = parent_env

    def add_variable(self, identifier: str, value: 'CSENode') -> None:
        self.variables[identifier] = value

    def add_variables(self, identifiers: List[str], values: List['CSENode']) -> None:
        for identifier, value in zip(identifiers, values):
            self.variables[identifier] = value

    def add_list(self, identifier: str, list_elements: List['CSENode']) -> None:
        self.lists[identifier] = list_elements

    def add_lambda(self, identifier: str, lambda_node: 'CSENode') -> None:
        if lambda_node.node_type == ObjectType.LAMBDA:
            if lambda_node.is_single_bound_var:
                self.lambdas[identifier] = CSENode(ObjectType.LAMBDA, lambda_node.node_value, lambda_node.cs_index, lambda_node.env)
            else:
                self.lambdas[identifier] = CSENode(ObjectType.LAMBDA, lambda_node.cs_index, lambda_node.bound_variables, lambda_node.env)
        elif lambda_node.node_type == ObjectType.EETA:
            if lambda_node.is_single_bound_var:
                self.lambdas[identifier] = CSENode(ObjectType.EETA, lambda_node.node_value, lambda_node.cs_index, lambda_node.env)
            else:
                self.lambdas[identifier] = CSENode(ObjectType.EETA, lambda_node.cs_index, lambda_node.bound_variables, lambda_node.env)
        else:
            raise RuntimeError("Invalid lambda node type")

    def find_variable(self, identifier: str) -> 'CSENode':
        if identifier in self.variables:
            return self.variables[identifier]
        elif self.parent_env is not None:
            return self.parent_env.find_variable(identifier)
        else:
            raise RuntimeError("Identifier: " + identifier + " not found")

    def find_lambda(self, identifier: str) -> 'CSENode':
        if identifier in self.lambdas:
            return self.lambdas[identifier]
        elif self.parent_env is not None:
            return self.parent_env.find_lambda(identifier)
        else:
            raise RuntimeError("Identifier: " + identifier + " not found")

    def find_list(self, identifier: str) -> List['CSENode']:
        if identifier in self.lists:
            return self.lists[identifier]
        elif self.parent_env is not None:
            return self.parent_env.find_list(identifier)
        else:
            raise RuntimeError("Identifier: " + identifier + " not found")

class CSE:
    def _init_(self):
        self.next_env = 0
        self.nextCS = -1
        self.controlStructures = []
        self.cse_machine = ControlStructure(-1)
        self.stack = Stack()
        self.env_stack = []
        self.envs = {}

    def createCS(self, root, current_cs=None, currentCSIndex=-1):
        if current_cs is None:
            current_cs = self.controlStructures[self.nextCS]
            self.nextCS += 1

        if root.getLabel() == "lambda":
            if root.getChildren()[0].getLabel() == ",":
                vars = [child.getValue() for child in root.getChildren()[0].getChildren()]
                lambda_node = CSENode(ObjectType.LAMBDA, self.nextCS, vars)
            else:
                var = root.getChildren()[0].getValue()
                lambda_node = CSENode(ObjectType.LAMBDA, var, self.nextCS)

            current_cs.addNode(lambda_node)

            newCS = ControlStructure(self.nextCS)
            self.controlStructures.append(newCS)
            self.nextCS += 1
            self.createCS(root.getChildren()[1], newCS, self.nextCS)

        elif root.getLabel() == "tau":
            tau = CSENode(ObjectType.TAU, str(len(root.getChildren())))
            current_cs.addNode(tau)

            for child in root.getChildren():
                self.createCS(child, current_cs, currentCSIndex)

        elif root.getLabel() == "->":
            thenCSIndex = self.nextCS
            elseCSIndex = self.nextCS + 1

            current_cs.addNode(CSENode(ObjectType.DELTA, str(thenCSIndex)))
            current_cs.addNode(CSENode(ObjectType.DELTA, str(elseCSIndex)))
            current_cs.addNode(CSENode(ObjectType.BETA, ""))

            thenCS = ControlStructure(thenCSIndex)
            self.controlStructures.append(thenCS)
            self.nextCS += 1
            self.createCS(root.getChildren()[1], thenCS, thenCSIndex)

            elseCS = ControlStructure(elseCSIndex)
            self.controlStructures.append(elseCS)
            self.nextCS += 1
            self.createCS(root.getChildren()[2], elseCS, elseCSIndex)

            self.createCS(root.getChildren()[0], current_cs, currentCSIndex)

        elif is_operator(root.getLabel()):
            current_cs.addNode(CSENode(ObjectType.OPERATOR, root.getLabel()))

            for child in root.getChildren():
                self.createCS(child, current_cs, currentCSIndex)

        elif root.getLabel() == "gamma":
            current_cs.addNode(CSENode(ObjectType.GAMMA, ""))

            for child in root.getChildren():
                self.createCS(child, current_cs, currentCSIndex)

        elif root.getLabel() in ["identifier", "integer", "string"]:
            value = root.getValue()
            type_label = root.getLabel()

            type_map = {"identifier": ObjectType.IDENTIFIER, "integer": ObjectType.INTEGER, "string": ObjectType.STRING}

            if type_label in type_map:
                current_cs.addNode(CSENode(type_map[type_label], value))
            else:
                raise RuntimeError("Invalid leaf type: " + type_label)
        else:
            raise RuntimeError("Invalid node type: " + root.getLabel() + " Value: " + root.getValue())

    def evaluate(self):
        e0 = CSENode(ObjectType.ENV, "0")
        self.cse_machine.addNode(e0)
        self.stack.addNode(e0)
        self.env_stack.append(self.next_env)
        self.envs[0] = Env(None)

        self.cse_machine.addNewCS(self.controlStructures[0])

        top = self.cse_machine.returnLastNode()

        while top.get_NodeType() != ObjectType.ENV or top.get_nodeValue() != "0":
            if top.get_NodeType() == ObjectType.INTEGER or top.get_NodeType() == ObjectType.STRING:
                self.stack.addNode(top)
                top = self.cse_machine.returnLastNode()
            elif top.get_NodeType() == ObjectType.IDENTIFIER:
                value = None
                value_l = None
                list_val = None

                try:
                    value = self.envs[self.env_stack[-1]].findVariable(top.get_nodeValue())
                    self.stack.addNode(CSENode(value.get_NodeType(), value.get_nodeValue()))
                except RuntimeError:
                    try:
                        value_l = self.envs[self.env_stack[-1]].findLambda(top.get_nodeValue())
                        self.stack.addNode(value_l)
                    except RuntimeError:
                        try:
                            list_val = self.envs[self.env_stack[-1]].findList(top.get_nodeValue())
                            self.stack.addNode(CSENode(ObjectType.LIST, list_val))
                        except RuntimeError:
                            if top.get_nodeValue() in built_in_functions:
                                self.stack.addNode(top)
                            elif top.get_nodeValue() == "nil":
                                self.stack.addNode(CSENode(ObjectType.LIST, []))
                            else:
                                raise RuntimeError("Variable not found: " + top.get_nodeValue())

                top = self.cse_machine.returnLastNode()
            elif top.get_NodeType() == ObjectType.LAMBDA:
                current_env = self.env_stack[-1]
                self.stack.addNode(top.set_ENV(current_env))

                top = self.cse_machine.returnLastNode()
            elif top.get_NodeType() == ObjectType.GAMMA:
                top_of_stack = self.stack.returnLastNode()

                if top_of_stack.get_NodeType() == ObjectType.LAMBDA:
                    new_env = Env(self.envs[top_of_stack.get_ENV()])
                    self.envs[self.next_env] = new_env
                    value = self.stack.returnLastNode()

                    if value.get_NodeType() == ObjectType.LAMBDA or value.get_NodeType() == ObjectType.EETA:
                        new_env.add_Lambda(top_of_stack.get_nodeValue(), value)
                    elif value.get_NodeType() == ObjectType.STRING or value.get_NodeType() == ObjectType.INTEGER:
                        new_env.add_variable(top_of_stack.get_nodeValue(), value)
                    elif value.get_NodeType() == ObjectType.LIST and not top_of_stack.get_IsSingleBoundVar():
                        var_list = top_of_stack.get_varList()
                        list_items = value.get_ListElements()
                        temp_list = []
                        var_count = 0
                        list_element_count = 0
                        creating_list = False

                        for i in list_items:
                            if creating_list:
                                temp_list.append(i)
                                list_element_count -= 1

                                if list_element_count == 0:
                                    new_env.add_List(var_list[var_count], temp_list)
                                    temp_list = []
                                    var_count += 1
                                    creating_list = False
                            else:
                                if i.get_NodeType() == ObjectType.LIST:
                                    list_element_count = int(i.get_nodeValue())
                                    if list_element_count == 0:
                                        new_env.add_List(var_list[var_count], temp_list)
                                        temp_list = []
                                        var_count += 1
                                    else:
                                        creating_list = True
                                elif i.get_NodeType() == ObjectType.LAMBDA:
                                    new_env.add_Lambda(var_list[var_count], i)
                                    var_count += 1
                                else:
                                    new_env.add_variable(var_list[var_count], i)
                                    var_count += 1

                        if creating_list:
                            new_env.add_List(var_list[var_count], temp_list)

                    elif value.get_NodeType() == ObjectType.LIST:
                        new_env.add_List(top_of_stack.get_nodeValue(), value.get_ListElements())
                    
                    self.env_stack.append(self.next_env - 1)
                    env_obj = CSENode(ObjectType.ENV, str(self.next_env - 1))
                    self.cse_machine.addNode(env_obj)
                    self.stack.addNode(env_obj)
                    self.cse_machine.addNewCS(self.controlStructures[top_of_stack.get_CSIndex()])
                elif top_of_stack.get_NodeType() == ObjectType.IDENTIFIER:
                    identifier = top_of_stack.get_nodeValue()

                    if identifier == "Print" or identifier == "print":
                        value = self.stack.returnLastNode()
                        list_elements = value.get_ListElements()

                        if value.get_NodeType() == ObjectType.LIST:
                            print("(", end="")
                            count_stack = []

                            for i in range(len(value.get_ListElements())):
                                if list_elements[i].get_NodeType() == ObjectType.LIST:
                                    count_stack.append(int(list_elements[i].get_nodeValue()))
                                    print("(", end="")
                                else:
                                    print(list_elements[i].get_nodeValue(), end="")

                                    if count_stack:
                                        for j in range(len(count_stack)):
                                            count_stack[j] -= 1

                                        if count_stack[-1] == 0:
                                            if i != len(value.get_ListElements()) - 1:
                                                print("), ", end="")
                                            else:
                                                print(")")
                                            count_stack.pop()
                                        else:
                                            if i != len(value.get_ListElements()) - 1:
                                                print(", ", end="")
                                    else:
                                        if i != len(value.get_ListElements()) - 1:
                                            print(", ", end="")
                            print(")")
                        elif value.get_NodeType() == ObjectType.ENV or value.get_nodeValue() == "dummy":
                            print("dummy")
                        elif value.get_NodeType() == ObjectType.LAMBDA:
                            print("[lambda closure: ", end="")
                            print(value.get_nodeValue(), end="")
                            print(": ", end="")
                            print(value.get_CSIndex(), end="")
                            print("]")
                        else:
                            print(value.get_nodeValue())
                    elif identifier == "Isinteger":
                        value = self.stack.returnLastNode()
                        if value.get_NodeType() == ObjectType.INTEGER:
                            self.stack.addNode(CSENode(ObjectType.BOOLEAN, "true"))
                        else:
                            self.stack.addNode(CSENode(ObjectType.BOOLEAN, "false"))
                    elif identifier == "Isstring":
                        value = self.stack.returnLastNode()
                        if value.get_NodeType() == ObjectType.STRING:
                            self.stack.addNode(CSENode(ObjectType.BOOLEAN, "true"))
                        else:
                            self.stack.addNode(CSENode(ObjectType.BOOLEAN, "false"))
                    elif identifier == "Isempty":
                        value = self.stack.returnLastNode()
                        if value.get_NodeType() == ObjectType.LIST:
                            if not value.get_ListElements():
                                self.stack.addNode(CSENode(ObjectType.BOOLEAN, "true"))
                            else:
                                self.stack.addNode(CSENode(ObjectType.BOOLEAN, "false"))
                        else:
                            raise RuntimeError("Invalid type for IsEmpty: " + value.get_nodeValue())
                    elif identifier == "Istuple":
                        value = self.stack.returnLastNode()
                        if value.get_NodeType() == ObjectType.LIST:
                            self.stack.addNode(CSENode(ObjectType.BOOLEAN, "true"))
                        else:
                            self.stack.addNode(CSENode(ObjectType.BOOLEAN, "false"))
                    elif identifier == "Order":
                        value = self.stack.returnLastNode()
                        if value.get_NodeType() == ObjectType.LIST:
                            count = 0
                            list_elem_skip = 0

                            for i in value.get_ListElements():
                                if i.get_NodeType() == ObjectType.LIST and list_elem_skip == 0:
                                    list_elem_skip = int(i.get_nodeValue())
                                    count += 1
                                elif list_elem_skip == 0:
                                    count += 1
                                else:
                                    list_elem_skip -= 1

                            self.stack.addNode(CSENode(ObjectType.INTEGER, str(count)))
                        else:
                            raise RuntimeError("Invalid type for Order: " + value.get_nodeValue())
                    elif identifier == "Conc":
                        first_arg = self.stack.returnLastNode()
                        second_arg = self.stack.returnLastNode()
                        self.cse_machine.popLastNode()

                        if first_arg.get_NodeType() == ObjectType.STRING and \
                                (second_arg.get_NodeType() == ObjectType.STRING or
                                second_arg.get_NodeType() == ObjectType.INTEGER):
                            self.stack.addNode(CSENode(ObjectType.STRING,
                                                    first_arg.get_nodeValue() + second_arg.get_nodeValue()))
                        else:
                            raise RuntimeError("Invalid type for Conc: " + first_arg.get_nodeValue())
                    elif identifier == "Stem":
                        arg = self.stack.returnLastNode()

                        if arg.get_NodeType() == ObjectType.STRING:
                            self.stack.addNode(CSENode(ObjectType.STRING, arg.get_nodeValue()[0]))
                        else:
                            raise RuntimeError("Invalid type for Stem: " + top_of_stack.get_nodeValue())
                    elif identifier == "Stern":
                        arg = self.stack.returnLastNode()

                        if arg.get_NodeType() == ObjectType.STRING:
                            self.stack.addNode(CSENode(ObjectType.STRING, arg.get_nodeValue()[1:]))
                        else:
                            raise RuntimeError("Invalid type for Stern: " + top_of_stack.get_nodeValue())
                    elif identifier == "Y*":
                        lambda_node = self.stack.returnLastNode()

                        if lambda_node.get_NodeType() == ObjectType.LAMBDA:
                            if lambda_node.get_IsSingleBoundVar():
                                self.stack.addNode(
                                    CSENode(ObjectType.EETA, lambda_node.get_nodeValue(), lambda_node.get_CSIndex(),
                                            lambda_node.get_ENV()))
                            else:
                                self.stack.addNode(
                                    CSENode(ObjectType.EETA, lambda_node.get_CSIndex(), lambda_node.get_varList(),
                                            lambda_node.get_ENV()))
                        else:
                            raise RuntimeError("Invalid type for Y*: " + lambda_node.get_nodeValue())
                    elif identifier == "ItoS":
                        arg = self.stack.returnLastNode()

                        if arg.get_NodeType() == ObjectType.INTEGER:
                            self.stack.addNode(CSENode(ObjectType.STRING, arg.get_nodeValue()))
                        else:
                            raise RuntimeError("Invalid type for ItoS: " + arg.get_nodeValue())
                    else:
                        raise RuntimeError("Unknown built-in function: " + identifier)
                elif top_of_stack.get_NodeType() == ObjectType.EETA:
                    self.stack.addNode(top_of_stack)

                    if top_of_stack.get_IsSingleBoundVar():
                        self.stack.addNode(
                            CSENode(ObjectType.LAMBDA, top_of_stack.get_nodeValue(), top_of_stack.get_CSIndex(),
                                    top_of_stack.get_ENV()))
                    else:
                        self.stack.addNode(
                            CSENode(ObjectType.LAMBDA, top_of_stack.get_CSIndex(), top_of_stack.get_varList(),
                                    top_of_stack.get_ENV()))

                    self.cse_machine.addNode(CSENode(ObjectType.GAMMA, ""))
                    self.cse_machine.addNode(CSENode(ObjectType.GAMMA, ""))
                elif top_of_stack.get_NodeType() == ObjectType.LIST:
                    second_arg = self.stack.returnLastNode()

                    if second_arg.get_NodeType() == ObjectType.INTEGER:
                        index = int(second_arg.get_nodeValue())
                        current_index = 0
                        list_element_pos = 0
                        list_elem_skip = 0
                        is_list = False

                        for i in top_of_stack.get_ListElements():
                            if i.get_NodeType() == ObjectType.LIST and list_elem_skip == 0:
                                list_elem_skip = int(i.get_nodeValue())
                                current_index += 1

                                if index == current_index:
                                    is_list = True
                                    break
                            elif list_elem_skip == 0:
                                current_index += 1

                                if index == current_index:
                                    break
                            else:
                                list_elem_skip -= 1
                            list_element_pos += 1

                        list_elements = []

                        if is_list:
                            length = int(top_of_stack.get_ListElements()[list_element_pos].get_nodeValue())

                            for i in range(length):
                                list_elements.append(top_of_stack.get_ListElements()[list_element_pos + i + 1])

                            self.stack.addNode(CSENode(ObjectType.LIST, list_elements))
                        else:
                            self.stack.addNode(top_of_stack.get_ListElements()[list_element_pos])
                    else:
                        raise RuntimeError("Invalid type for Index: " + second_arg.get_nodeValue())
                top = self.cse_machine.returnLastNode()
            elif top.get_NodeType() == ObjectType.ENV:
                env_nodes = []
                st_node = self.stack.returnLastNode()

                while st_node.get_NodeType() != ObjectType.ENV:
                    env_nodes.append(st_node)
                    st_node = self.stack.returnLastNode()

                for node in reversed(env_nodes):
                    self.stack.addNode(node)

                self.env_stack.pop()

                top = self.cse_machine.returnLastNode()
            elif top.get_NodeType() == ObjectType.OPERATOR:
                biop = top.get_nodeValue()
                val_1 = self.stack.returnLastNode()
                val_2 = self.stack.returnLastNode()

                if biop in ["+", "-", "/", "*"]:
                    self.stack.addNode(CSENode(ObjectType.INTEGER, op(biop, val_1.get_nodeValue(), val_2.get_nodeValue())))
                elif biop == "neg":
                    self.stack.addNode(val_2)
                    self.stack.addNode(CSENode(ObjectType.INTEGER, unop(biop, val_1.get_nodeValue())))
                elif biop == "not":
                    self.stack.addNode(val_2)
                    self.stack.addNode(CSENode(ObjectType.BOOLEAN, unop(biop, val_1.get_nodeValue())))
                elif biop == "aug":
                    if val_1.get_NodeType() == ObjectType.LIST:
                        if val_2.get_NodeType() == ObjectType.LIST:
                            elem_1 = val_1.get_ListElements()
                            elem_2 = val_2.get_ListElements()

                            elem_1.append(CSENode(ObjectType.LIST, str(len(elem_2))))

                            for element in elem_2:
                                elem_1.append(element)

                            self.stack.addNode(CSENode(ObjectType.LIST, elem_1))
                        elif val_2.get_NodeType() in [ObjectType.INTEGER, ObjectType.BOOLEAN, ObjectType.STRING]:
                            elem_1 = val_1.get_ListElements()
                            elem_1.append(CSENode(val_2.get_NodeType(), val_2.get_nodeValue()))
                            self.stack.addNode(CSENode(ObjectType.LIST, elem_1))
                        else:
                            raise RuntimeError("Invalid type for aug: " + val_2.get_nodeValue())
                else:
                    self.stack.addNode(CSENode(ObjectType.BOOLEAN, booleanops(biop, val_1.get_nodeValue(), val_2.get_nodeValue())))
                top = self.cse_machine.returnLastNode()
            elif top.get_NodeType() == ObjectType.TAU:
                new_elem = []
                tau_size = int(top.get_nodeValue())

                for _ in range(tau_size):
                    node = self.stack.returnLastNode()

                    if node.get_NodeType() == ObjectType.LIST:
                        elem_1 = node.get_ListElements()
                        new_elem.append(CSENode(ObjectType.LIST, str(len(elem_1))))

                        for element in elem_1:
                            new_elem.append(element)
                    else:
                        new_elem.append(node)

                self.stack.addNode(CSENode(ObjectType.LIST, new_elem))

                top = self.cse_machine.returnLastNode()
            elif top.get_NodeType() == ObjectType.BETA:
                node = self.stack.returnLastNode()

                if node.get_NodeType() == ObjectType.BOOLEAN:
                    if node.get_nodeValue() == "true":
                        self.cse_machine.popLastNode()
                        true_node = self.cse_machine.returnLastNode()

                        if true_node.get_NodeType() == ObjectType.DELTA:
                            self.cse_machine.addNewCS(ControlStructure[int(true_node.get_nodeValue())])
                        else:
                            raise RuntimeError("Invalid type for beta: " + true_node.get_nodeValue())
                    else:
                        false_node = self.cse_machine.returnLastNode()
                        self.cse_machine.popLastNode()

                        if false_node.get_NodeType() == ObjectType.DELTA:
                            self.cse_machine.addNewCS(ControlStructure[int(false_node.get_nodeValue())])
                        else:
                            raise RuntimeError("Invalid type for beta: " + false_node.get_nodeValue())
                elif node.get_NodeType() == ObjectType.INTEGER:
                    if node.get_nodeValue() != "0":
                        self.cse_machine.popLastNode()
                        true_node = self.cse_machine.returnLastNode()

                        if true_node.get_NodeType() == ObjectType.DELTA:
                            self.cse_machine.addNewCS(ControlStructure[int(true_node.get_nodeValue())])
                        else:
                            raise RuntimeError("Invalid type for beta: " + true_node.get_nodeValue())
                    else:
                        false_node = self.cse_machine.returnLastNode()
                        self.cse_machine.popLastNode()

                        if false_node.get_NodeType() == ObjectType.DELTA:
                            self.cse_machine.addNewCS(ControlStructure[int(false_node.get_nodeValue())])
                        else:
                            raise RuntimeError("Invalid type for beta: " + false_node.get_nodeValue())
                else:
                    raise RuntimeError("Invalid type for beta: " + node.get_nodeValue())
                top = self.cse_machine.returnLastNode()


    def nextChar(self):
        return self.text[self.index]

    def parseAlpha(self):
        string = ""

        while self.nextChar().isalpha():
            string += self.nextChar()
            self.index += 1

        return string

    def parseNum(self):
        string = ""

        while self.nextChar().isdigit():
            string += self.nextChar()
            self.index += 1

        return string

    def parseExpression(self):
        if self.nextChar() == " ":
            self.index += 1

        if self.nextChar() == "(":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            if self.nextChar().isdigit() or self.nextChar() == "-":
                num = ""
                if self.nextChar() == "-":
                    self.index += 1
                    num = "-" + self.parseNum()
                else:
                    num = self.parseNum()

                if self.nextChar() == " ":
                    self.index += 1

                self.index += 1

                if self.nextChar() == " ":
                    self.index += 1

                if self.nextChar() == ")":
                    self.index += 1

                    return num
                elif self.nextChar().isdigit() or self.nextChar() == "-":
                    num_2 = ""
                    if self.nextChar() == "-":
                        self.index += 1
                        num_2 = "-" + self.parseNum()
                    else:
                        num_2 = self.parseNum()

                    if self.nextChar() == " ":
                        self.index += 1

                    self.index += 1

                    if self.nextChar() == " ":
                        self.index += 1

                    if self.nextChar() == ")":
                        self.index += 1

                        return "(" + num + " + " + num_2 + ")"
                    else:
                        raise RuntimeError("Invalid input")
                elif self.nextChar().isalpha():
                    id = self.parseAlpha()

                    if self.nextChar() == " ":
                        self.index += 1

                    if self.nextChar() == " ":
                        self.index += 1

                    if self.nextChar() == ")":
                        self.index += 1

                        return "(" + num + " + " + id + ")"
                    else:
                        raise RuntimeError("Invalid input")
                else:
                    raise RuntimeError("Invalid input")
            elif self.nextChar().isalpha():
                id = self.parseAlpha()

                if self.nextChar() == " ":
                    self.index += 1

                if self.nextChar() == " ":
                    self.index += 1

                if self.nextChar() == ")":
                    self.index += 1

                    return id
                elif self.nextChar().isalpha():
                    id_2 = self.parseAlpha()

                    if self.nextChar() == " ":
                        self.index += 1

                    self.index += 1

                    if self.nextChar() == " ":
                        self.index += 1

                    if self.nextChar() == ")":
                        self.index += 1

                        return "(" + id + " + " + id_2 + ")"
                    else:
                        raise RuntimeError("Invalid input")
                elif self.nextChar().isdigit() or self.nextChar() == "-":
                    num = ""
                    if self.nextChar() == "-":
                        self.index += 1
                        num = "-" + self.parseNum()
                    else:
                        num = self.parseNum()

                    if self.nextChar() == " ":
                        self.index += 1

                    self.index += 1

                    if self.nextChar() == " ":
                        self.index += 1

                    if self.nextChar() == ")":
                        self.index += 1

                        return "(" + id + " + " + num + ")"
                    else:
                        raise RuntimeError("Invalid input")
                else:
                    raise RuntimeError("Invalid input")
            elif self.nextChar() == "-":
                self.index += 1

                num = self.parseNum()

                if self.nextChar() == " ":
                    self.index += 1

                self.index += 1

                if self.nextChar() == " ":
                    self.index += 1

                if self.nextChar() == ")":
                    self.index += 1

                    return num
                elif self.nextChar().isdigit() or self.nextChar() == "-":
                    num_2 = ""
                    if self.nextChar() == "-":
                        self.index += 1
                        num_2 = "-" + self.parseNum()
                    else:
                        num_2 = self.parseNum()

                    if self.nextChar() == " ":
                        self.index += 1

                    self.index += 1

                    if self.nextChar() == " ":
                        self.index += 1

                    if self.nextChar() == ")":
                        self.index += 1

                        return "(" + num + " + " + num_2 + ")"
                    else:
                        raise RuntimeError("Invalid input")
                elif self.nextChar().isalpha():
                    id = self.parseAlpha()

                    if self.nextChar() == " ":
                        self.index += 1

                    if self.nextChar() == " ":
                        self.index += 1

                    if self.nextChar() == ")":
                        self.index += 1

                        return "(" + num + " + " + id + ")"
                    else:
                        raise RuntimeError("Invalid input")
                else:
                    raise RuntimeError("Invalid input")
            else:
                raise RuntimeError("Invalid input")
        elif self.nextChar() == "\"":
            string = ""
            self.index += 1

            while self.nextChar() != "\"":
                string += self.nextChar()
                self.index += 1

            self.index += 1

            return string
        else:
            raise RuntimeError("Invalid input")

    def parseOperator(self):
        if self.nextChar() == " ":
            self.index += 1

        if self.nextChar() == "+":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "+"
        elif self.nextChar() == "-":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "-"
        elif self.nextChar() == "/":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "/"
        elif self.nextChar() == "*":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "*"
        else:
            raise RuntimeError("Invalid input")

    def parseUnary(self):
        if self.nextChar() == " ":
            self.index += 1

        if self.nextChar() == "+":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "+"
        elif self.nextChar() == "-":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "-"
        else:
            raise RuntimeError("Invalid input")

    def parseNot(self):
        if self.nextChar() == " ":
            self.index += 1

        if self.nextChar() == "!":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "not"
        else:
            raise RuntimeError("Invalid input")

    def parseAug(self):
        if self.nextChar() == " ":
            self.index += 1

        if self.nextChar() == "#":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "aug"
        else:
            raise RuntimeError("Invalid input")

    def parseBoolOp(self):
        if self.nextChar() == " ":
            self.index += 1

        if self.nextChar() == "&":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "&"
        elif self.nextChar() == "|":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "|"
        else:
            raise RuntimeError("Invalid input")

    def parseGamma(self):
        if self.nextChar() == " ":
            self.index += 1

        if self.nextChar() == "@":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "@"
        else:
            raise RuntimeError("Invalid input")

    def parseBeta(self):
        if self.nextChar() == " ":
            self.index += 1

        if self.nextChar() == "<":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "<"
        else:
            raise RuntimeError("Invalid input")

    def parseDelta(self):
        if self.nextChar() == " ":
            self.index += 1

        if self.nextChar() == "=":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "="
        else:
            raise RuntimeError("Invalid input")

    def parseTau(self):
        if self.nextChar() == " ":
            self.index += 1

        if self.nextChar() == "$":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "$"
        else:
            raise RuntimeError("Invalid input")

    def parseEeta(self):
        if self.nextChar() == " ":
            self.index += 1

        if self.nextChar() == "^":
            self.index += 1

            if self.nextChar() == " ":
                self.index += 1

            return "^"
        else:
            raise RuntimeError("Invalid input")

    def parse(self, text):
        self.text = text
        self.index = 0
        while self.index < len(self.text):
            if self.nextChar().isdigit() or (self.nextChar() == "-" and self.text[self.index + 1].isdigit()):
                num = self.parseExpression()
                self.stack.addNode(CSENode(ObjectType.INTEGER, num))
            elif self.nextChar().isalpha():
                id = self.parseAlpha()
                self.stack.addNode(CSENode(ObjectType.IDENTIFIER, id))
            elif self.nextChar() == "\"":
                string = self.parseExpression()
                self.stack.addNode(CSENode(ObjectType.STRING, string))
            elif self.nextChar() == "(":
                self.index += 1
                self.parse()
            elif self.nextChar() == "+" or self.nextChar() == "-" or self.nextChar() == "/" or \
                    self.nextChar() == "*":
                op = self.parseOperator()
                self.stack.addNode(CSENode(ObjectType.OPERATOR, op))
            elif self.nextChar() == "&" or self.nextChar() == "|":
                op = self.parseBoolOp()
                self.stack.addNode(CSENode(ObjectType.OPERATOR, op))
            elif self.nextChar() == "@":
                op = self.parseGamma()
                self.stack.addNode(CSENode(ObjectType.OPERATOR, op))
            elif self.nextChar() == "<":
                op = self.parseBeta()
                self.stack.addNode(CSENode(ObjectType.OPERATOR, op))
            elif self.nextChar() == "=":
                op = self.parseDelta()
                self.stack.addNode(CSENode(ObjectType.OPERATOR, op))
            elif self.nextChar() == "$":
                op = self.parseTau()
                self.stack.addNode(CSENode(ObjectType.OPERATOR, op))
            elif self.nextChar() == "^":
                op = self.parseEeta()
                self.stack.addNode(CSENode(ObjectType.OPERATOR, op))
            elif self.nextChar() == "!":
                op = self.parseNot()
                self.stack.addNode(CSENode(ObjectType.OPERATOR, op))
            elif self.nextChar() == "#":
                op = self.parseAug()
                self.stack.addNode(CSENode(ObjectType.OPERATOR, op))
            elif self.nextChar() == " ":
                self.index += 1
            else:
                raise RuntimeError("Invalid input")
        self.cse_machine.addNewCS(ControlStructure[int(self.cse_machine.returnLastNode().get_nodeValue())])


def testCSEMachine():
    cse_machine = CSE()
    cse_machine.parse("((3+4) * 5) + 2")
    cse_machine.execute()
    cse_machine.parse("((3+4) & 5) | 2")
    cse_machine.execute()
    cse_machine.parse("3+4+5")
    cse_machine.execute()
    cse_machine.parse("((3+4+5)=3)")
    cse_machine.execute()
    cse_machine.parse("(\"hello\"+\" \"+\"world\")")
    cse_machine.execute()
    cse_machine.parse("(\"hello\"+\" world\")")
    cse_machine.execute()
    cse_machine.parse("(\"hello\"+\" \"+\"world\"+\"!\")")
    cse_machine.execute()
    cse_machine.parse("!(3+4+5)")
    cse_machine.execute()
    cse_machine.parse("(\"hello\"=\"world\")")
    cse_machine.execute()
    cse_machine.parse("3 + (((4 + 5) + 6) + 7)")
    cse_machine.execute()
    cse_machine.parse("5+6*7")
    cse_machine.execute()
    cse_machine.parse("(5+6)*7")
    cse_machine.execute()
    cse_machine.parse("5+(6*7)")
    cse_machine.execute()
    cse_machine.parse("((3+4)*5)+2")
    cse_machine.execute()
    cse_machine.parse("((3 + 4) + 5) + 6")
    cse_machine.execute()
    cse_machine.parse("3+(4+(5+6))")
    cse_machine.execute()
    cse_machine.parse("1<2")
    cse_machine.execute()
    cse_machine.parse("1<2<3")
    cse_machine.execute()
    cse_machine.parse("2<3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3")
    cse_machine.execute()
    cse_machine.parse("1<2 & 3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3 & 3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3 | 3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & (2<3 | 3<2)")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3 | 3<2")
    cse_machine.execute()
    cse_machine.parse("(1<2 & 2<3) | 3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & (2<3 | 3<2) | 3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3 | (3<2 | 2<1)")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3 | 3<2 | 2<1")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (2+1)=3)")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (1+2)=2)")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (1+2)=2 | (2+1)=3)")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (1+2)=2 | (1+2)=1)")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (1+2)=2 | (1+2)=1 | (2+1)=3)")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (1+2)=2 | (1+2)=1 | (2+1)=3 | (1+1)=2)")
    cse_machine.execute()
    cse_machine.parse("1<2")
    cse_machine.execute()
    cse_machine.parse("1<2<3")
    cse_machine.execute()
    cse_machine.parse("2<3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3")
    cse_machine.execute()
    cse_machine.parse("1<2 & 3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3 & 3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3 | 3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & (2<3 | 3<2)")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3 | 3<2")
    cse_machine.execute()
    cse_machine.parse("(1<2 & 2<3) | 3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & (2<3 | 3<2) | 3<2")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3 | (3<2 | 2<1)")
    cse_machine.execute()
    cse_machine.parse("1<2 & 2<3 | 3<2 | 2<1")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (2+1)=3)")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (1+2)=2)")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (1+2)=2 | (2+1)=3)")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (1+2)=2 | (1+2)=1)")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (1+2)=2 | (1+2)=1 | (2+1)=3)")
    cse_machine.execute()
    cse_machine.parse("((1+2)=3 | (1+2)=2 | (1+2)=1 | (2+1)=3 | (1+1)=2)")
    cse_machine.execute()


# testCSEMachine()

def is_operator(label):
    operators_ = ["+", "-", "/", "*", "aug", "neg", "not", "eq", "gr", "ge", "ls", "le", "ne", "or", "&"]
    return label in operators_