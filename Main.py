from Scanner import scan
from Parser import parse
import tree_flattner
from cse_machine import evaluate
from Standardizer import standardize_tree
from DataStructures import node
from DataStructures import print_tree
from DataStructures import Lambda
from DataStructures import delta
from DataStructures import id
from DataStructures import gamma
from DataStructures import delta

def main():
    # input_file = input('Enter the file name: ')
    input_file = "Python/PL_Project/abcd.txt"
    tokens = scan(input_file)
    for token in tokens:
        print(token)
    
    AST = parse(tokens)
    print("\n\n\nAbstract Syntax Tree: \n")
    print_tree(AST)
    
    ST = standardize_tree(AST)
    print("\n\n\nStandardized Tree: \n")
    print_tree(ST)
    
    control_structures=tree_flattner.CS(ST)
    i=0
    print("\n")
    for cs in control_structures:
        print("Control Structure ",i)
        i+=1
        cs.print_stack()
    print("\n")
    print ("STARTING EVALUATION")
    answer=evaluate(control_structures)
    print(f"output is  {answer.items[0].value}")
        
main()