#!/usr/bin/python3
import random
import sys
import getopt
from copy import deepcopy
import defaultvalues
from buggyClasses import *
from buggyHeader import *

lineNumber=1 # used to keep track of the written program's line number in vim
globalVariables=[] # a list of global variables

# pull values from defaultvalues.py
max_layers_of_tree=defaultvalues.MAX_LAYERS_OF_TREE
min_layers_of_tree=defaultvalues.MIN_LAYERS_OF_TREE
max_number_of_leafs_per_layer=defaultvalues.MAX_NUMBER_OF_LEAFS_PER_LAYER
min_number_of_leafs_per_layer=defaultvalues.MIN_NUMBER_OF_LEAFS_PER_LAYER
max_number_of_conditions_per_leaf=defaultvalues.MAX_NUMBER_OF_CONDITIONS_PER_LEAF
min_number_of_conditions_per_leaf=defaultvalues.MIN_NUMBER_OF_CONDITIONS_PER_LEAF
max_number_of_variables_per_leaf=defaultvalues.MAX_NUMBER_OF_VARIABLES_PER_LEAF
min_number_of_variables_per_leaf=defaultvalues.MIN_NUMBER_OF_VARIABLES_PER_LEAF
max_number_of_variables_per_fxn=defaultvalues.MAX_NUMBER_OF_VARIABLES_PER_FXN
min_number_of_variables_per_fxn=defaultvalues.MIN_NUMBER_OF_VARIABLES_PER_FXN
max_number_of_elements_per_leaf=defaultvalues.MAX_NUMBER_OF_ELEMENTS_PER_LEAF
min_number_of_elements_per_leaf=defaultvalues.MIN_NUMBER_OF_ELEMENTS_PER_LEAF
max_number_of_elements_per_fxn=defaultvalues.MAX_NUMBER_OF_ELEMENTS_PER_FXN
min_number_of_elements_per_fxn=defaultvalues.MIN_NUMBER_OF_ELEMENTS_PER_FXN
probability_of_if=defaultvalues.PROBABILITY_OF_IF
max_globals=defaultvalues.MAX_GLOBALS
num_functions=defaultvalues.NUM_FUNCTIONS
interestingness=defaultvalues.INTERESTINGNESS

try:
  # max layers, max leafs 
  opts, args = getopt.getopt(sys.argv[1:], "",["layers=", "leafs=", "leafConditions=", "leafVariables=", "fxnVariables=","ifProb=", "garbage=", "fxnGarbage=", "leafGarbage=", "gvars=", "fxns=", "bugs=", "int="])

except getopt.GetoptError as err:
  print(err)
  sys.exit(2)

for o, a in opts:
  if o in ("--layers"):
    max_layers_of_tree=int(a)
  
  elif o in ("--leafs"):
    max_number_of_leafs_per_layer=int(a)
  
  elif o in ("--leafVariables"):
    max_number_of_variables_per_leaf=int(a)

  elif o in ("--fxnVariables"):
    max_number_of_variables_per_fxn=int(a)

  elif o in ("--ifProb"):
    probability_of_if=float(a)

  elif o in ("--garbage"):
    max_number_of_elements_per_fxn=int(a)
    max_number_of_elements_per_leaf=int(a)

  elif o in ("--fxnGarbage"):
    max_number_of_elements_per_fxn=int(a)

  elif o in ("--leafGarbage"):
    max_number_of_elements_per_leaf=int(a)

  elif o in ("--gvars"):
    max_globals=int(a)

  elif o in ("--fxns"):
    num_functions=int(a)

  #TODO number of bugs
  elif o in ("--bugs"):
    pass

  elif o in ("--int"):
    interestingness=int(a)

print("#include<stdio.h>")
lineNumber+=1

# create global variables
for i in range(random.randint(0,max_globals)):
  var=variable()
  globalVariables.append(var)
if len(globalVariables)>0:
  print("// **********GLOBAL VARIABLES********** (lineNumber=" + str(lineNumber)+")")
  lineNumber+=1
  for var in globalVariables:
    print(declareVariableText(random.randint(0,1), var))
    lineNumber+=1

# create function declarations
print("// **********FUNCTION DECLARATIONS********** (lineNumber=" + str(lineNumber)+")")
lineNumber+=1

for i in range(num_functions):
  createFxnMeta(randomFxnType())
for fxn in availableFxns:
  print(createFxnDeclarationText(fxn))
  lineNumber+=1

#print(availableFxns)

print("void dumpStdin();")
lineNumber+=1

'''
create a bunch of functions
'''
for fxn in availableFxns:
  function=Fxn(fxn, deepcopy(globalVariables), availableFxns, lineNumber, 
    max_layers_of_tree,
    min_layers_of_tree,
    max_number_of_leafs_per_layer,
    min_number_of_leafs_per_layer,
    max_number_of_conditions_per_leaf,
    min_number_of_conditions_per_leaf,
    max_number_of_variables_per_leaf,
    min_number_of_variables_per_leaf,
    max_number_of_variables_per_fxn,
    min_number_of_variables_per_fxn,
    max_number_of_elements_per_leaf,
    min_number_of_elements_per_leaf,
    max_number_of_elements_per_fxn,
    min_number_of_elements_per_fxn,
    probability_of_if)
  print(function)
  lineNumber=function.lineNumber

# dump stdin fxn for getting multiple inputs from user
dumpStdinFxnText='''void dumpStdin()
  {
    char dummy;
    do
      {
        dummy = getchar();
      }while ( (dummy != '\\n') && (dummy != EOF) );
  }'''
print(dumpStdinFxnText)
lineNumber+=8
'''
create the main() function
'''
fxn=["main", "int", "foo", "bar"] # main is special
mainFxn=Fxn(fxn, deepcopy(globalVariables), availableFxns, lineNumber,
    max_layers_of_tree,
    min_layers_of_tree,
    max_number_of_leafs_per_layer,
    min_number_of_leafs_per_layer,
    max_number_of_conditions_per_leaf,
    min_number_of_conditions_per_leaf,
    max_number_of_variables_per_leaf,
    min_number_of_variables_per_leaf,
    max_number_of_variables_per_fxn,
    min_number_of_variables_per_fxn,
    max_number_of_elements_per_leaf,
    min_number_of_elements_per_leaf,
    max_number_of_elements_per_fxn,
    min_number_of_elements_per_fxn,
    probability_of_if,
    interestingness)

print(mainFxn)
