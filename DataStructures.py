class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'
    
    
    
# class node:
#     def __init__(self,value):
#         self.value = value
#         self.left = None
#         self.right = None
# def print_tree(root, level=0, prefix="Root: "):
#     if root is not None:
#         print(" " * (level * 4) + prefix + str(root.value))
#         if root.left is not None or root.right is not None:
#             print_tree(root.left, level + 1, "L--- ")
#             print_tree(root.right, level + 1, "R--- ")
            
class node:
    def __init__(self,value):
        self.value = value
        self.children = []
def print_tree(root, level=0):
    if root is not None:
        print("." * (level * 1) + str(root.value))
        for child in root.children:
            print_tree(child, level + 1)
        
class stack:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def top(self):
        return self.items[-1]
    def push(self,value):
        self.items.append(value)
    def pop(self):
        if self.isEmpty():
            print('Stack is empty')
            return
        return self.items.pop()
    def print_stack(self):
        for item in self.items:
            if isinstance(item,id):
                print(f"Id object with value {item.value}")
            elif isinstance(item,int_value):
                print(f"Int object with value {item.value}")
            elif isinstance(item,gamma):
                print(f"Gamma object with index {item.index}")
            elif isinstance(item,Lambda):
                print(f"Lambda object with index {item.index} and variable list ")
                print(item.var_list)
                print("end of list")
            elif isinstance(item,delta):
                print(f"Delta object with index {item.index}")
            elif isinstance(item,tau):
                print(f"Tau object with index {item.index}")
            elif isinstance(item,y_star):
                print(f"Y_star object with value {item.value}")
            elif isinstance(item,eta):
                print(f"Eta object with index {item.index} and variable list ")
                print(item.var_list)
                print("end of list")
            elif isinstance(item,string_value):
                print(f" string object with  value {item.value}")
            elif isinstance(item,environment):
                print(f"Environment object with index {item.index} and value ")
                for key in item.value:
                    if not isinstance(item.value[key],eta):
                        print(f"{key} : {item.value[key].value}")
                    else:
                        print(f"{key} : eta object with index {item.value[key].index} and variable list ")
                        print(item.value[key].var_list)
                print("end of list")
                
    
class id:
    def __init__(self, value):
        self.value= value
        
class string_value:
    def __init__(self, value):
        self.value= value

class int_value:
    def __init__(self, value):
        self.value= value

class gamma:
    def __init__(self, index):
        self.index=0   

        
class Lambda:
    def __init__(self, index , var_list, E):
        self.index = index
        self.var_list = var_list
        self.E = E

class delta:
    def __init__(self, index ):
        self.index=index

class tau:
    def __init__(self, index ):
        self.index=index

class y_star:
    def __init__(self, value ):
        self.value=value

class eta:
    def __init__(self, index,var_list,E): 
        self.index=index
        self.var_list=var_list
        self.E=E

class environment:
    def __init__(self, index, value, parent):
        self.index=index
        self.parent=parent
        self.value=value