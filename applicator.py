

binary_operations=["+", "-", "/", "*", "**", "eq", "ne", "gr", "ge", "le",">", "<", ">=", "<=", "or", "&", "aug", "ls"]
unary_operations=["Print", "Isstring", "Isinteger", "Istruthvalue", "Isfunction", "Null","Istuple", "Order", "Stern", "Stem", "ItoS", "neg", "not"]

def is_binary_operation(op):
    return op.value in binary_operations

def is_unary_operation(op):
    return op.value in unary_operations

def apply_binary_operation(op, left, right):
    if op.value == "+":
        return str(left + right)
    elif op.value == "-":
        return str(left - right)
    elif op.value == "*":
        return str(left * right)
    elif op.value == "/":
        if right == 0:
            raise Exception("Division by zero")
        return str(left / right)
    elif op.value == "**":
        return str(left ** right)
    elif op.value == "eq":
        return str(left == right)
    elif op.value == "ne":
        return str(left != right)
    elif op.value == "gr":
        return str(left > right)
    elif op.value == "ge":
        return str(left >= right)
    elif op.value == "le":
        return str(left <= right)
    elif op.value == ">":
        return str(left > right)
    elif op.value == "<":
        return str(left < right)
    elif op.value == ">=":
        return str(left >= right)
    elif op.value == "<=":
        return str(left <= right)
    elif op.value == "or":
        return str(left or right)
    elif op.value == "&":
        return str(left and right)
    elif op.value == "aug":
        return str(left + right)
    elif op.value == "ls":
        return str(left < right)
    else:
        raise Exception("Unknown binary operator: " + op.value)
    
def apply_unary_operation(op, operand):
    if op.value == "Print":
        print(operand)
        return str(operand)
    elif op.value == "Isstring":
        return str(isinstance(operand, str))
    elif op.value == "Isinteger":
        return str(isinstance(operand, int))
    elif op.value == "Istruthvalue":
        if operand=="True" or operand=="False" :
            return "True"
        else:
            return "False"
    elif op.value == "Isfunction":
        return callable(operand)
    elif op.value == "Null":
        return operand == None
    elif op.value == "Istuple":
        return str(isinstance(operand, tuple))
    elif op.value == "Order":
        return str(len(operand))
    elif op.value == "Stern":
        return str(operand[1:])
    elif op.value == "Stem":
        return str(operand[0])
    elif op.value == "ItoS":
        return str(operand)
    elif op.value == "neg":
        return str(-operand)
    elif op.value == "not":
        return str(not operand)
    else:
        print(f"unknown operation    {op.value}")

def is_int_operation(op):
    return op in ["+", "-", "*", "/", "**", "eq", "ne", "gr", "ge", "le", ">", "<", ">=", "<=","ls"]


