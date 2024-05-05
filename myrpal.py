from csemachine import *
import sys

def runProgram(file_name):
    global st
    st = standardize(file_name)

if __name__ == "__main__":
    fileName = sys.argv[1]
    get_result(fileName)