from rpal_parser import parse

class ST_Node:
    def __init__(self, name, left = None, right = None):
        self.name = str(name)
        self.left = left
        self.right = right 


    def __str__(self):
        return self.value
    
def standardize_let(x, p, e):
    # This function will standardize the let node.
    # The let node will be converted to a lambda node.
    # The lambda node will be converted to a gamma node.
    lambda_node = ST_Node("lambda", x, p)
    gammma_node = ST_Node("gamma", lambda_node, e)
    return gammma_node

def standardize_where(x, p, e):
    # This function will standardize the where node.
    # The where node will be converted to a lambda node.
    # The lambda node will be converted to a gamma node.
    lambda_node = ST_Node("lambda", x, p)
    gammma_node = ST_Node("gamma", lambda_node, e)          ## not sure about the order of the arguments
    return gammma_node

def standardize_tau(e_list):
    # This function will standardize the tau node.
    # The tau node will be converted to a gamma node.
    # The gamma node will be converted to a gamma node.
    nil_node = ST_Node("nil")
    
    for e in e_list:
        gamma_node = ST_Node("gamma", ST_Node("aug"), nil_node)
        nil_node = ST_Node("gamma", gamma_node, e)
    
    return gamma_node

#def standardize_if(b, t, e):
def standardize_op(op, e1, e2):
    # This function will standardize the op node.
    # The op node will be converted to a gamma node.
    # The gamma node will be converted to a gamma node.
    gamma_node2 = ST_Node("gamma", ST_Node(op), e1)
    gamma_node1 = ST_Node("gamma", gamma_node2, e2)
    return gamma_node1

def standardize_fcn_form(p, v_list, e):
    # This function will standardize the fcn_form node.
    # The fcn_form node will be converted to a lambda node.
    # The lambda node will be converted to a gamma node.
    lambda_node = ST_Node("lambda", v_list[-1], e)
    
    for v in v_list[:-1:-1]:
        lambda_node = ST_Node("lambda", v, lambda_node)
    
    return ST_Node("=", p, lambda_node)


def standardize_lambda_ve(v_list, e):
    lambda_node = e
    
    for v in v_list[::-1]:
        lambda_node = ST_Node("lambda", v, lambda_node)
        
    return lambda_node

def standardize_within(x1, x2, e1, e2):
    # This function will standardize the within node.
    # The within node will be converted to a lambda node.
    # The lambda node will be converted to a gamma node.
    lambda_node = ST_Node("lambda", x1, e2)
    gamma_node = ST_Node("gamma", lambda_node, e1)
    
    return ST_Node("=", x2, gamma_node)

def standardize_rec(x, e):
    # This function will standardize the rec node.
    # The rec node will be converted to a gamma node.
    # The gamma node will be converted to a gamma node.
    lambda_node = ST_Node("lambda", x, e)
    gamma_node = ST_Node("gamma", "Y*", lambda_node)
    
    

def standardize(root):
    # This function will standardize the AST.
    # The AST will be traversed and the standardization will be done in a bottom-up manner.
    if root is None:
        return None
    
    # WE must go until a leaf node is reached


prog_file = input()

tree = parse(prog_file)
standardize(tree)