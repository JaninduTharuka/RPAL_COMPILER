# Convert Abstract Syntax Tree to Standardized Tree

from DataStructures import node

UnaryOps = ["neg","not"]
BinaryOps = ["&","or","gr","ge","ls","le","eq","ne","+","-","*","/","**"]


def standardize_tree(Node):
    if len(Node.children) > 0:
        for i in range(len(Node.children)):
            standardize_tree(Node.children[i])
    standardize_Node(Node)
    return Node
    
def standardize_Node(Node):
    if Node.value == "let":
        standardize_let(Node)
    if Node.value == "where":
        standardize_where(Node)
    if Node.value == "fcn_form":
        standardize_fcn_form(Node)
    # if Node.value == "tau":
    #     standardize_tau(Node)
    if Node.value == "lambda":
        standardize_multi_parameter_functions(Node)
    if Node.value == "within":
        standardize_within(Node)
    # if Node.value in UnaryOps:
    #     standardize_unary_ops(Node)
    # if Node.value in BinaryOps:
    #     standardize_binary_ops(Node)
    if Node.value == "rec":
        standardize_rec(Node)
    


############################################################################################################
###########################################  Standardize Let  ##############################################
############################################################################################################

def standardize_let(Node):
    # Check for Errors
    if len(Node.children) != 2:
        print("Error: Expected 2 children in Let Node")
        return
    if Node.children[0].value != "=":
        print("Error: Expected '=' in left child of Let Node")
    
    E = Node.children[0].children[1]
    P = Node.children[1]
    
    Node.children[1] = E
    Node.children[0].children[1] = P
    
    Node.value = "gamma"
    Node.children[0].value = "lambda"
    

############################################################################################################
###########################################  Standardize Where  ############################################
############################################################################################################

def standardize_where(Node):
    # Check for Errors
    if len(Node.children) != 2:
        print("Error: Expected 2 children in Where Node")
        return
    if Node.children[1].value != "=":
        print("Error: Expected '=' in right child of Where Node")
    
    E = Node.children[1].children[1]
    P = Node.children[0]
    
    Node.children[0] = E
    Node.children[1].children[1] = P
    
    Node.value = "gamma"
    Node.children[1].value = "lambda"
    
    SwitchChildren(Node)
    

############################################################################################################
#####################################  Standardize Function Form  ##########################################
############################################################################################################

def standardize_fcn_form(Node):
    # Check for Errors
    if len(Node.children) < 3:
        print("Error: Expected at least 3 children in Function Form Node")
        return
    v = len(Node.children) - 2
    
    E = Node.children[-1]
    P = Node.children[0]
    set_V = Node.children[1:-1]
    
    Node.children = [P]
    Node.value = "="
    current = Node
    
    for i in range(v):
        current.children.append(node("lambda"))
        current.children[1].children.append(set_V[i])
        current = current.children[1]
    current.children.append(E)
    
    
# ############################################################################################################
# ##########################################  Standardize Tuples  ############################################
# ############################################################################################################
    
# def standardize_tau(Node):
#     # Check for Errors
#     if len(Node.children) < 2:
#         print("Error: Expected at least 2 children in Tau Node")
#         return

#     e = len(Node.children)
#     set_E = Node.children
    
#     Node.value = "gamma"
#     Node.children = []
#     current = Node
    
#     for i in range(1,e+1):
#         current.children.append(node("gamma"))
#         current.children.append(set_E[-i])
#         current.children[0].children.append(node("aug"))
#         current.children[0].children.append(node("gamma"))
#         current = current.children[0].children[1]
#     current.value = "nil"
    
    
############################################################################################################
#############################  Standardize Multi Parameter Functions  ######################################
############################################################################################################

def standardize_multi_parameter_functions(Node):
    # Check for Errors
    if len(Node.children) < 3:
        return
    
    v = len(Node.children) - 1
    E = Node.children[-1]
    V = Node.children[0:-1]
    
    current = Node
    current.children = []
    
    for i in range(v):
        current.children.append(V[i])
        current.children.append(node("lambda"))
        if i == v-1:
            current.children[1] = E
        current = current.children[1]



############################################################################################################
######################################### Standardize Within ###############################################
############################################################################################################

def standardize_within(Node):
    if len(Node.children) != 2:
        print("Error: Expected 2 children in Within Node")
        return
    if Node.children[0].value != "=" and Node.children[1].value != "=":
        print("Error: Expected '=' in children of Within Node")
        return
    
    X1 = Node.children[0].children[0]
    X2 = Node.children[1].children[0]
    E1 = Node.children[0].children[1]
    E2 = Node.children[1].children[1]
    
    Node.value = "="
    Node.children = [X2,node("gamma")]
    Node.children[1].children = [node("lambda"),E1]
    Node.children[1].children[0].children = [X1,E2]


# ############################################################################################################
# ######################################## Standardize Unary Ops #############################################
# ############################################################################################################

# def standardize_unary_ops(Node):
#     if len(Node.children) != 1:
#         print("Error: Expected 1 child in Unary Ops Node")
#         return
    
#     Uop = Node.value
#     E = Node.children[0]
    
#     Node.value = "gamma"
#     Node.children = [node(Uop),E]
    

# ############################################################################################################
# ######################################## Standardize Binary Ops ############################################
# ############################################################################################################

# def standardize_binary_ops(Node):
#     if len(Node.children) != 2:
#         print("Error: Expected 2 children in Binary Ops Node")
#         return
    
#     Bop = Node.value
#     E1 = Node.children[0]
#     E2 = Node.children[1]
    
#     Node.value = "gamma"
#     Node.children = [node("gamma"),E2]
#     Node.children[0].children = [node(Bop),E1]


def standardize_rec(Node):
    if (len(Node.children) != 1):
        print("rec node should have exactly 1 children")
        return
    if (Node.children[0].value != "="):
        print("The child of rec node should be '=' node")
        return
    
    X=Node.children[0].children[0]
    E=Node.children[0].children[1]
    Node.value="="
    Node.children=[]
    Node.children.append(X)
    Node.children.append(node("gamma"))
    Node.children[1].children.append(node("Y_star : Y"))
    Node.children[1].children.append(node("lambda"))
    Node.children[1].children[1].children.append(X)
    Node.children[1].children[1].children.append(E)








def SwitchChildren(Node):
    if len(Node.children) != 2:
        print("Error: Expected 2 children in SwitchChildren")
        return
    temp = Node.children[0]
    Node.children[0] = Node.children[1]
    Node.children[1] = temp
    return Node