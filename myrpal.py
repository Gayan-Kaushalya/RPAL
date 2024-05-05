# Description: This file is the main file that will be run to execute the program. It will take in the command line arguments and execute the program accordingly.
# You cannot run this file in the IDE. You must run it in the terminal.


from rpal_parser import parse
from node import preorder_traversal
from standardizer import standardize
from csemachine import *
import sys




if __name__ == "__main__":
    arguments = sys.argv
    
    if len(arguments) < 2:
        print("Wrong command. Make sure the command is in the following format. \n ./myrpal.py [-l] [-ast] [-st] [-noout] filename")
        sys.exit(1)
        
    else:
        if len(arguments) == 2:
            file_name = arguments[1]
            get_result(file_name)
            
        else:
            switches = arguments[1 : -1]

            # If '-l' is in the switches, we must print the file as it is.
            if "-l" in switches:
                file_name = arguments[-1]
                
                with open(file_name, "r") as file:
                    print(file.read())
                    
                print()
                
            # If '-ast' is in the switches, we must print the abstract syntax tree.
            if "-ast" in switches:
                file_name = arguments[-1]
                ast = parse(file_name)
                preorder_traversal(ast)
                
                print()
            
            else:
                print("Wrong command. Make sure the command is in the following format. \n ./myrpal.py [-l] [-ast] [-st] [-noout] filename")
                sys.exit(1)