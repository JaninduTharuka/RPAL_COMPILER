from DataStructures import node
from DataStructures import stack
from DataStructures import Lambda
from DataStructures import delta
from DataStructures import tau
from DataStructures import id
from DataStructures import int_value
from DataStructures import gamma
from DataStructures import delta
from DataStructures import y_star
from DataStructures import string_value

def CS (ST):
    control_structures=[]
    current_cs=stack()
    Stack=stack()
    control_structures.append(current_cs)
    tree_flattner(ST,control_structures,current_cs)
    return control_structures

def extract_string(string):
    # Split the string by colon and get the second part
    extracted_string = string.split(":")[-1].strip()
    extracted_type = string.split(":")[0].strip()
    return extracted_type,extracted_string

def tree_flattner(Node,control_structures,current_cs):
    if (Node.value == "lambda"):
        print(f"started lamda   {Node.value}")
        flatter_lambda(Node,control_structures,current_cs)
        print(f"ended lamda   {Node.value}")

    elif (Node.value == "->"):
        print("started arrow")
        flatter_arrow(Node,control_structures,current_cs)
        print("ended arrow")

    elif (Node.value == "tau"):
        print("started tau")
        flatter_tau(Node,control_structures,current_cs)
        print("ended tau")

    else:
        print("entered else")
        if (Node.value == "gamma") or Node.value in ("or" , "&" , "gr" , "ge" , "ls" , "le" , "eq" , "ne" , "+" , "-" , "*" , "/" , "**"," not" , "neg"):
            if Node.value == "gamma":
                current_cs.push(gamma(0))
            else:
                current_cs.push(id(Node.value))
                print(f"pushed id object   {Node.value}")

        else:
            category,value=extract_string(str(Node.value))
            print(f"category is {category} and value is {value}")
            if (category == "INTEGER"):
                current_cs.push(int_value(value))
                print(f"pushed int object   {value}")
            elif (category == "IDENTIFIER"):
                current_cs.push(id(value))
                print(f"pushed id object {value}")
            elif (category == "Y_star"):
                current_cs.push(y_star(value))
                print(f"pushed y_star object {value}")
            elif(category == "STRING"):
                current_cs.push(string_value(value))
                print(f"pushed string object with value {value}")
    for child in Node.children:
            tree_flattner(child,control_structures,current_cs)

def flatter_lambda(Node,control_structures,current_cs):
    if (Node.children[0].value == ","):
        var_list=[]
        for child in Node.children[0].children:
            var_list.append(child.value.value)
        string=",".join(var_list)
        Node.children[0].value="IDENTIFIER : "+string
        Node.children[0].children=[]
    
    category,value=extract_string(str(Node.children[0].value))
    lamda=Lambda(len(control_structures),value,-1)
    current_cs.push(lamda)
    print(f"pushed lambda object with index {len(control_structures)} and variable list {value}")

    new_cs=stack()
    control_structures.append(new_cs)

    for child in Node.children[1:]:
        tree_flattner(child,control_structures,new_cs)
    
    Node.children=[]
    
def flatter_arrow(Node,control_structures,current_cs):
    print("started flatter arrow")
    
    delta_then=delta(len(control_structures))
    current_cs.push(delta_then)
    then_cs=stack()
    control_structures.append(then_cs)
    tree_flattner(Node.children[1],control_structures,then_cs)
    
    delta_else=delta(len(control_structures))
    current_cs.push(delta_else)
    else_cs=stack()
    control_structures.append(else_cs)
    tree_flattner(Node.children[2],control_structures,else_cs)

    current_cs.push(id("$"))
    tree_flattner(Node.children[0],control_structures,current_cs)
    Node.children=[]
    print("ended flatter arrow")

def flatter_tau(Node,control_structures,current_cs):
    print("started flatter tau")
    tau_object=tau(len(Node.children))
    current_cs.push(tau_object)
    for child in Node.children:
        tree_flattner(child,control_structures,current_cs)
    Node.children=[]
    print("ended flatter tau")






    

    
