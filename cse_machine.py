from DataStructures import node
from DataStructures import stack
from DataStructures import Lambda
from DataStructures import delta
from DataStructures import tau
from DataStructures import environment
from DataStructures import gamma
from DataStructures import id
from DataStructures import int_value
from DataStructures import y_star
from DataStructures import eta
from DataStructures import string_value
from applicator import is_binary_operation
from applicator import is_unary_operation
from applicator import apply_binary_operation
from applicator import apply_unary_operation
from applicator import is_int_operation
import tree_flattner


cur_env_index=0

def extract_environment(control):
    result_env=None
    print("entered extract environment")
    for element in control.items:
        if (not isinstance(element,environment)):
            continue
        else:
            result_env=element
    
    return result_env

def lookup(current_element,current_environment,environment_list):
    if current_element.value in current_environment.value:
        return current_environment.value[current_element.value]
    else:
        if current_environment.parent == None:
            print(f"error variable {current_element.value} not found")
            return
        else:
            return lookup(current_element,environment_list[current_environment.parent],environment_list)
 

def evaluate (structures):
    print("entered evaluate")
    Stack=stack()
    environment_list={}
    control=stack()
    control_structures=structures
    primitive_environment=environment(0,{},None)
    environment_list[0]=primitive_environment
    Stack.push(primitive_environment)
    control.push(primitive_environment)
    control.items.extend(control_structures[0].items)
    environment_list[0]=primitive_environment

    

    control.print_stack()
    while not control.isEmpty():
        current_element=control.pop()
        if isinstance(current_element,Lambda):
            print(f"current element is lambda with index {current_element.index} and variable list {current_element.var_list}")
        elif isinstance(current_element,gamma):
            print(f"current element is gamma with index {current_element.index}")
        elif isinstance(current_element,environment):
            print(f"current element is environment with index {current_element.index}")
        elif isinstance(current_element,delta):
            print(f"current element is delta with index {current_element.index}")
        elif isinstance(current_element,tau):
            print(f"current element is tau with index {current_element.index}")
        elif isinstance(current_element,y_star):
            print(f"current element is y_star with value {current_element.value}")
        elif isinstance(current_element,eta):
            print(f"current element is eta with index {current_element.index} and variable list {current_element.var_list}")
        elif isinstance (current_element,string_value):
            print(f"current element is string with value { current_element.value}")
        else:
            print(f"current element is {current_element.value}")


        if isinstance(current_element,id):
            if (not is_binary_operation(current_element)) and (not is_unary_operation(current_element) and current_element.value != "$"):
                print("entered rule_1")
                rule_1(current_element,Stack,environment_list,control)
                print("exited rule_1")
            elif current_element.value == "$":
                print("entered rule_8")
                rule_8(current_element,Stack,environment_list,control,control_structures)
            else:
                print("entered rule_3")
                rule_3(current_element,Stack,environment_list,control)
                print("exited rule_3")
        elif isinstance(current_element,int_value):
            Stack.push(current_element)
        elif isinstance(current_element,string_value):
            Stack.push(current_element)
        elif isinstance(current_element,Lambda):
            print("entered rule_2")
            rule_2(current_element,Stack,environment_list,control)
            print("exited rule_2")
        elif isinstance(current_element,environment):
            print("entered rule_5")
            rule_5(current_element,Stack,environment_list,control)
            print("exited rule_5")
        elif isinstance(current_element,y_star):
            Stack.push(current_element)
            print ("pushed y_star object to the stack")

        elif isinstance(current_element,gamma):
            first_element=Stack.pop()
            second_element=Stack.pop()
            if isinstance(first_element,y_star):
                print("entered rule_12")
                rule_12(second_element,Stack,environment_list,control)
            elif isinstance(first_element,eta):
                Stack.push(second_element)
                print("entered rule_13")
                rule_13(first_element,Stack,environment_list,control)
            elif isinstance(first_element,Lambda):
                Stack.push(second_element)
                print("entered rule_4")
                rule_4(first_element,Stack,environment_list,control,control_structures)
                print("exited rule_4") 
            else:
                Stack.push(second_element)
                Stack.push(first_element)
    return Stack



            
def rule_1(current_element,Stack,environment_list,control):
    current_environment=extract_environment(control)
    print(f"current environment is {current_environment.index}")
    val=lookup(current_element,current_environment,environment_list)
    # if val == NULLL
    if not isinstance(val,eta):
        print(f"looked up value is {val.value} ")
    else:
        print(f"looked up value is eta object with index {val.index} and variable list {val.var_list}")
    Stack.push(val)

def rule_2(current_element,Stack,environment_list,control):
    current_environment=extract_environment(control)
    print(f"current environment is {current_environment.index}")
    current_element.E=current_environment.index
    Stack.push(current_element)

def rule_3(current_element,Stack,environment_list,control):
    if is_binary_operation(current_element):
        print("entered rule_3 binary")
        left=Stack.pop()
        right=Stack.pop()
        if is_int_operation(current_element.value):
            if (not isinstance(left,int_value)) or (not isinstance(right,int_value)):
                print("error in rule 3 : binary integer operation should have integer operands")
                return
            else:
                left=int(left.value)
                right=int(right.value)
                print(f"left is {left} and right is {right} operation is {current_element.value}")
                result=apply_binary_operation(current_element,left,right)
                Stack.push(int_value(result))
        else:
            print(f"left is {left} and right is {right} operation is {current_element.value}")
            if (not isinstance(left,string_value)) or (not isinstance(right,string_value)):
                print("error in rule 3 : binary string operation should have integer operands")
                return           
            result=apply_binary_operation(current_element,left,right)
            Stack.push(string_value(result))
            print(f"result is {result} and pushed to the stack")
    else:
        print("entered rule_3 unary")
        operand=Stack.pop()
        print(f"operand is {operand} operation is {current_element.value}")
        if (current_element.value == "neg"):
            operand=int(operand.value)
            result=apply_unary_operation(current_element,operand)
            Stack.push(int_value(result))
        elif (current_element.value == "Isinteger"):
            operand=int(operand.value)
            result=apply_unary_operation(current_element,operand)
            Stack.push(id(result))
        else:
            if not(isinstance(operand,string_value)):
                print ("error unary string operation with not string type")
            operand=operand.value
            result=apply_unary_operation(current_element,operand)
            if(current_element.value in ["Isstring", "Istruthvalue", "Isfunction","Istuple"]):
                Stack.push(id(result))
            else:
                Stack.push(string_value(result))
        print(f"result is {result} and pushed to the stack")

def rule_4(current_element,Stack,environment_list,control,control_structures):
    global cur_env_index
    memory={}
    current_environment=extract_environment(control)
    print(f"current environment is {current_environment.index}")
    var_list=current_element.var_list.split(",")
    print(f"variable list is {var_list}")
    for var in var_list:
        value=Stack.pop()
        if (not isinstance(value,int_value)) and (not isinstance(value,eta)) and (not isinstance(value,string_value)):
            print(f"error  when assigning value {value} to variable {var}")
            return
        memory[var]=value
    new_environment=environment(cur_env_index+1,memory,current_element.E)
    cur_env_index+=1
    environment_list[cur_env_index+1]=new_environment
    print(f"new environment is {new_environment.index}")
    print(f"new environment value is ")
    for key in new_environment.value:
        if isinstance(new_environment.value[key],eta):
            print(f"{key} : eta object with index {new_environment.value[key].index} and variable list {new_environment.value[key].var_list}")
        else:    
            print(f"{key} : {new_environment.value[key].value}")
    print(f"new environment parent is {new_environment.parent}")
    Stack.push(new_environment)
    control.push(new_environment)
    control.items.extend(control_structures[current_element.index].items)
    print(f"control stack after pushing new environment")
    control.print_stack()

def rule_5(current_element,Stack,environment_list,control):
    value=Stack.pop()
    print(f"popped value from the stack is {value}")
    environment=Stack.pop()
    print(f"popped environment from the control is {environment.index}")
    print(f"current element is {current_element.index}")
    if current_element != environment:
        print("error in rule 5 environement missmatch")
        return
    Stack.push(value)

def rule_8(current_element,Stack,environment_list,control,control_structures):
    result=Stack.pop()  
    print(f"result of rule 8 is {result.value}")
    if (result.value != "True") and (result.value != "False"):
        print("error in rule 8  : at the top of the stack is not a boolean value")
        return 
    else:
        delta_else=control.pop()
        delta_then=control.pop()
        print(f"delta then is {delta_then.index} and delta else is {delta_else.index}")
        if ( not isinstance(delta_then,delta)) or (not isinstance(delta_else,delta)):
            print("error in rule 8 : delta then and delta else should be delta objects")
            return
        else:
            if result.value == "True":
                control.items.extend(control_structures[delta_then.index].items)
            else:
                control.items.extend(control_structures[delta_else.index].items)


def rule_12(current_element,Stack,environment_list,control):
    if not isinstance(current_element,Lambda):
        print("error in rule 12 : top of the stack should be lamda object")
        return
    else:
        eta_object=eta(current_element.index,current_element.var_list,current_element.E)
        print(f"created eta object is  index{eta_object.index} and environment {eta_object.E} and variable list is {eta_object.var_list}")
        Stack.push(eta_object)

def rule_13(current_element,Stack,environment_list,control):
    lambda_object=Lambda(current_element.index,current_element.var_list,current_element.E)
    print(f"created lambda object is {lambda_object.index} and variable list is {lambda_object.var_list}")
    Stack.push(current_element)
    Stack.push(lambda_object)
    control.push(gamma(0))
    control.push(gamma(0))

    


