import random
import ctypes
import defaultvalues
#from copy import deepcopy
# TODO: line number
# TODO: bug_line_numbers
'''
This is a header file for the random buggy program program
'''
# constants from defaultvalues (keep all of the constants in one file)
LEADING_ZEROS=defaultvalues.LEADING_ZEROS
NUM_FUNCTIONS=defaultvalues.NUM_FUNCTIONS
MAX_GLOBALS=defaultvalues.MAX_GLOBALS
MIN_NUM_BUGS=defaultvalues.MIN_NUM_BUGS
MAX_RECURSION=defaultvalues.MAX_RECURSION
PERCENT_BRANCH_VARIABLE=defaultvalues.PERCENT_BRANCH_VARIABLE
MAX_BRANCH_VARIABLES=defaultvalues.MAX_BRANCH_VARIABLES
PERCENT_BRANCH_EXPRESSION=defaultvalues.PERCENT_BRANCH_EXPRESSION
MAX_BRANCH_EXPRESSIONS=defaultvalues.MAX_BRANCH_EXPRESSIONS
MAX_FXN_VARIABLES=defaultvalues.MAX_FXN_VARIABLES
PERCENT_FXN_VARIABLES=defaultvalues.PERCENT_FXN_VARIABLES
MAX_FXN_EXPRESSIONS=defaultvalues.MAX_FXN_EXPRESSIONS
PERCENT_FXN_EXPRESSIONS=defaultvalues.PERCENT_FXN_EXPRESSIONS
MAX_NUM_OPERANDS=defaultvalues.MAX_NUM_OPERANDS
PRE_POST_CHANCE=defaultvalues.PRE_POST_CHANCE
LEADING_ZEROS=defaultvalues.LEADING_ZEROS
MAX_NUM_FXN_ARGS=defaultvalues.MAX_NUM_FXN_ARGS
MAX_WORDS_RANDOM_STRING=defaultvalues.MAX_WORDS_RANDOM_STRING
MAX_LETTERS_RANDOM_STRING_WORD=defaultvalues.MAX_LETTERS_RANDOM_STRING_WORD
MAX_BUFF_LENGTH=defaultvalues.MAX_BUFF_LENGTH

# GLOBAL VARIABLES
num_bugs = 0 # the number of bugs in the program
bug_line_numbers=[] # a list of the line numbers that contain bugs

# varCounts is a list of the counts of all of the different types of variables in the program
# in order the types are char, double, float, int, long, short
varCounts=[0,0,0,0,0,0]

# availableFxns is a list of functions that are available
availableFxns=[]

'''
randomVariableType() returns the text of a random type for a variable
INPUTS: Nothing
OUTPUTS: A string of an appropriate variable type.
'''
def randomVariableType():
  types=["char","double","float", "int", "long", "short"]
  #TODO pointers and strings
  sign=["signed","unsigned"]
  kind=["static", "volatile", "register"]
  return random.choice(types)

'''
variableNameGenerator()
INPUTS:varCounts, varType
varCounts is a list of the counts of each type of variable
type is a string of the type of the variable
OUTPUTS: A string of a valid standardized variable name
varCounts is updated for the new name
'''
def variableNameGenerator(varType):
  global varCounts
  # find the type
  types=["char","double","float", "int", "long", "short"]
  typeIndex=types.index(varType)
  # get the count
  count=varCounts[typeIndex]
  # name the variable
  name=varType+"Var"+str(count).zfill(LEADING_ZEROS)
  # update varCounts
  varCounts[typeIndex]=count+1
  return name

'''
variable()
INPUTS: The global variable varCounts is a list of integers representing the number of each type of variable.
varCounts looks like [#charVariables, #doubleVariables, #floatVariables,  #intVariables, #longVariables, #shortVariables].
Each sublist of scope is a list of the additional variables for the local scope (scope gets appended for loops and function calls).
Each sublist of that local scope is a variable of the form ["name", "varType"]; this sublist gets appended when variables are created.
OUTPUTS: a list of the form ["name", "variableType"]
'''
def variable(isBuff=0):
  #global varCounts
  if not isBuff:
    isBuff=random.choice([True, False])
  types=["char","double","float", "int", "long", "short"]
  varType=random.choice(types)
  name=variableNameGenerator(varType)
  if isBuff:
    length=random.randint(2, MAX_BUFF_LENGTH)
    var = [name, varType, length]
  else:
    var = [name, varType]
  return var

'''
iteratorVariable()
INPUTS: The global variable varCounts is a list of integers representing the number of each type of variable.
varCounts looks like [#charVariables, #doubleVariables, #floatVariables, #intVariables, #longVariables, #shortVariables].
Each sublist of scope is a list of the additional variables for the local scope (scope gets appended for loops and function calls).
Each sublist of that local scope is a variable of the form ["name, "varType"]; this sublist gets appended when variables are created.
OUTPUTS: a list of the form ["name", "int"]
'''
def iteratorVariable():
  global varCounts
  varType="int"
  name=variableNameGenerator("int")
  var=[name, varType]
  return var

'''
getAppropriateValue returns an appropriate value given a variable type
INPUTS:varType is a string of the type of the variable
OUTPUTS: a string of the appropriate type (1, 1.0, etc... )
'''
def getAppropriateValue(varType):
  #types=["char","double","float", "int", "long", "short"]
  if varType=="char":
    #TODO edge cases
    # as a quick fix, we're going to trim the allowable values and modify the weird ones
    candidateValue=random.randint(32,126)
    appropriateValue="\'"+chr(candidateValue)+"\'"
    if chr(candidateValue)=="'": # single quote
      appropriateValue="\'\\\'\'"
    elif chr(candidateValue)=="\"": # double quote
      appropriateValue="\'\\\"\'"
    elif chr(candidateValue)=="\\": # backslash
      appropriateValue="\'\\\\\'"
  #TODO: do the rest of the types in ctypes  
  elif varType=="double":
    appropriateValue=random.randint(cSignedLowest(ctypes.c_double),cSignedMax(ctypes.c_double))
  
  elif varType=="float":
    appropriateValue=random.randint(cSignedLowest(ctypes.c_float),cSignedMax(ctypes.c_float))
  
  elif varType=="int":
    appropriateValue=random.randint(cSignedLowest(ctypes.c_int),cSignedMax(ctypes.c_int))
  
  elif varType=="long":
    appropriateValue=random.randint(cSignedLowest(ctypes.c_long),cSignedMax(ctypes.c_long))
  
  else : #varType=="short":
    appropriateValue=random.randint(cSignedLowest(ctypes.c_short),cSignedMax(ctypes.c_short))
  
  return str(appropriateValue)

'''
declareVariableText()
INPUTS: Initialize is an int 1 for initialize 0 for don't initialize
variable is a list of the form ["name", "variableType"]
OUTPUTS: The text to declare a variable.
'''
def declareVariableText(initialize, variable):
  varType=variable[1]
  varName=variable[0]
  if len(variable)==2:# not a buffer
    if initialize==1:
      appropriateValue=getAppropriateValue(variable[1])
      text=varType + " " + varName + "=" + str(appropriateValue) + ";"
    else: # not initialized
      text=varType + " " + varName + ";"
  else: # buffer
    #if initialize==1:
    #  appropriateValue=getAppropriateValue(variable[1])
    #  text=variable[1] + " " +variable[0] + "=" + str(appropriateValue) + ";"
    #else: # not initialized
    # initializing random buffers would be a mess in the randomly generated source
    buffLength=str(variable[2])
    text=varType + " " + varName + "[" + buffLength +"];"
  return text

'''
fxnNameGenerator creates a valid standardized name for functions.
INPUTS: The return type fo the function.
OUTPUTS: A standardized function name.
'''
def fxnNameGenerator(returnType):
  global availableFxns
  count=len(availableFxns)
  name=returnType+"Fxn"+str(count).zfill(LEADING_ZEROS)
  return name

'''
randomFxnType creates a valid function return type.
INPUTS: nothing.
OUTPUTS: A string of function return type.
'''
def randomFxnType():
  types=["char","double","float", "int", "long", "short", "void"]
  sign=["signed","unsigned"]
  kind=["static", "volatile", "register"]
  return random.choice(types)

'''
createFxnMeta returns a list [name, rtnType, argType1, argType2, ...]
INPUTS: a return type string
OUTPUTS: a list of function characteristics (fxnMeta)
'''
def createFxnMeta(rtnType):
  global availableFxns
  fxnMeta=[]
  rtnType=randomFxnType()
  name=fxnNameGenerator(rtnType)
  fxnMeta.append(name)
  fxnMeta.append(rtnType)
  args = []
  numberOfArgs=random.randint(0,MAX_NUM_FXN_ARGS)
  for i in range(numberOfArgs):
    fxnMeta.append(randomVariableType())
  # update availableFxns
  availableFxns.append(fxnMeta)
  return fxnMeta

'''
createFxnDeclarationText creates the text of a function declaration.
INPUTS: fxnMeta is a list of strings of the form ["name", "return type", arg type 1, arg type 2, ...] where the argument types are optional.
OUTPUTS: a string of syntactically correct function text.
'''
def createFxnDeclarationText(fxnMeta):
  returnType=fxnMeta[1]
  name=fxnMeta[0]
  fxnText=""
  fxnText=fxnText+str(returnType)+" "+str(name)+" ("
  i=0;
  for arg in fxnMeta[2:]:
    fxnText=fxnText+str(arg)+" funcVar"+str(i)+", "
    i+=1;
  if(len(fxnMeta[2:])>0): #if the function has arguments
    fxnText=fxnText[:-2]
  fxnText=fxnText+");"
  return fxnText

'''
createFxnCallText creates the text to call a function.
INPUTS: fxnMeta is a list of strings of the form ["name", "return type", arg type 1, arg type 2, ...] where the argument types are optional.
recursionLevel is an integer of the level of recursion when the function is called.
OUTPUTS: a syntactically correct string for calling a function.
'''
def createFxnCallText(fxnMeta, variables, recursionLevel=0):
  #TODO: what if variables is empty?
  callText=""
  fxnName=fxnMeta[0]
  callText=fxnName+"("
  for arg in fxnMeta[2:]:
    callText=callText+getRelevantSource(arg, variables, recursionLevel+1)+", "
  if len(fxnMeta[2:])>0:
    callText=callText[:-2]
  callText=callText+")"
  return callText

'''
getRelevantSource returns a relevant value (or value source like a function return) given a type.
INPUTS: sourceType is a string of the source type
recursionLevel is an integer of the level of recursion when the function is called.
OUTPUTS:
'''
def getRelevantSource(sourceType, variables, recursionLevel=0):
  # TODO: return relevant buffer?
  potentialSources=[]

  if isinstance(sourceType, list): # if the source is a list, then the requester wants a buffer
    if len(variables)>0: # if variables isn't empty
      #gather potential sources from variables
      for var in variables:
        if var[1]==sourceType: # variable type
          if len(var)==3: # buffer
            potentialSources.append(var[0])
    else: # variables is empty
      # what do i do if variables is empty?
      # nothing. move on. if everything comes up empty, something will be created at the end
      # TODO create something at the end if potentialSources is empty
      pass

  else: # if the source isn't a list, then the requester DOESN'T want a buffer
    if len(variables)>0:
      #gather potential sources from variables
      for var in variables:
        if var[1]==sourceType: # variable type
          if len(var)==3: # buffer
            bufLen=var[2]
            elementFromBuffer=str(random.randint(0, bufLen-1))
            bufString=var[0]+ " [" + elementFromBuffer + "]"
            potentialSources.append(bufString)
          else:
            potentialSources.append(var[0])
    
#    if len(availableFxns)>0:
#      #gather appropriate sources from available functions
#      if recursionLevel <= MAX_RECURSION:
#        for fxnMeta in availableFxns:
#          if fxnMeta[1]==sourceType: # function return type
#            # TODO: do not call self
#            if 
#            potentialSources.append(createFxnCallText(fxnMeta, variables, recursionLevel+1))

    #generate appropriate values
    potentialSources.append(getAppropriateValue(sourceType))

  #randomly decide source
  return random.choice(potentialSources) 

'''
randomConstant
'''
def randomConstant(rndType=None):
  types=["char","double","float", "int", "long", "short"]
  if rndType==None:
    rndType=random.choice(types)
  randConst=str(getAppropriateValue(rndType))
  return randConst
'''
makeCondition
INPUTS:
OUTPUTS:
'''
def makeCondition(variables, availableFxns):
  condition="1"
  if (len(variables)>0) and (len(availableFxns)>0):
    # choose 2 variables, a relationalOperator, 2 functionCalls, and a constant
    relationalOperators=["==", "!=", ">", "<", ">=", "<="]
    operator=random.choice(relationalOperators)
    condVar1=random.choice(variables)
    condVar2=random.choice(variables)
    funcMeta1=random.choice(availableFxns)
    funcCall1=createFxnCallText(funcMeta1, variables)
    funcMeta2=random.choice(availableFxns)
    funcCall2=createFxnCallText(funcMeta2, variables)

    # choose what kind of condition you want to return
    choice = random.choice(["vrf", "v", "vrv", "vrc", "f", "frf", "frc", "c"])

    if choice=="vrf" and funcMeta1[1]!="void":
      if len(condVar1)>2: # if condVar1 is a buffer
        randomElement=str(random.randint(0,condVar1[2]-1))
        varName1=condVar1[0]+"["+randomElement+"]"
      else: # condVar1 is NOT a buffer
        varName1=condVar1[0]
      condition=varName1+" "+operator+" "+funcCall1
    
    elif choice=="v":
      if len(condVar1)>2: # if condVar1 is a buffer
        randomElement=str(random.randint(0,condVar1[2]-1))
        varName1=condVar1[0]+"["+randomElement+"]"
      else: # condVar1 is NOT a buffer
        varName1=condVar1[0]
      condition=varName1
   
    elif choice=="vrv":
      if len(condVar1)>2: # if condVar1 is a buffer
        randomElement=str(random.randint(0,condVar1[2]-1))
        varName1=condVar1[0]+"["+randomElement+"]"
      else: # condVar1 is NOT a buffer
        varName1=condVar1[0]
      if len(condVar2)>2: # if condVar2 is a buffer
        randomElement=str(random.randint(0,condVar2[2]-1))
        varName2=condVar2[0]+"["+randomElement+"]"
      else: # condVar2 is NOT a buffer
        varName2=condVar2[0]
      condition=varName1+" "+operator+" "+varName2
  
    elif choice=="vrc":
      if len(condVar1)>2: # if condVar1 is a buffer
        randomElement=str(random.randint(0,condVar1[2]-1))
        varName1=condVar1[0]+"["+randomElement+"]"
      else: # condVar1 is NOT a buffer
        varName1=condVar1[0]
      condition=varName1+" "+operator+" "+randomConstant(condVar1[1])
 
    elif choice=="f" and funcMeta1[1]!="void":
      condition=funcCall1

    elif choice=="frf" and funcMeta1[1]!="void" and funcMeta2[1]!="void":
      condition=funcCall1+" "+operator+" "+funcCall2

    elif choice=="frc" and funcMeta1[1]!="void":
      condition=funcCall1+" "+operator+" "+randomConstant(funcCall1[1])

    else: # c
      condition=randomConstant()
   
    pass

  elif (len(variables)>0):
    # choose 2 variables, a relationalOperator, and a constant
    relationalOperators=["==", "!=", ">", "<", ">=", "<="]
    operator=random.choice(relationalOperators)
    condVar1=random.choice(variables)
    condVar2=random.choice(variables)

    # choose what kind of condition you want to return
    choice = random.choice(["v", "vrv", "vrc"])
   
    if choice=="v":
      if len(condVar1)>2: # if condVar1 is a buffer
        randomElement=str(random.randint(0,condVar1[2]-1))
        varName1=condVar1[0]+"["+randomElement+"]"
      else: # condVar1 is NOT a buffer
        varName1=condVar1[0]
      condition=varName1
    
    elif choice=="vrv":
      if len(condVar1)>2: # if condVar1 is a buffer
        randomElement=str(random.randint(0,condVar1[2]-1))
        varName1=condVar1[0]+"["+randomElement+"]"
      else: # condVar1 is NOT a buffer
        varName1=condVar1[0]
      if len(condVar2)>2: # if condVar2 is a buffer
        randomElement=str(random.randint(0,condVar2[2]-1))
        varName2=condVar2[0]+"["+randomElement+"]"
      else: # condVar2 is NOT a buffer
        varName2=condVar2[0]
      condition=varName1+" "+operator+" "+varName2

    else:# choice=="vrc":
      if len(condVar1)>2: # if condVar1 is a buffer
        randomElement=str(random.randint(0,condVar1[2]-1))
        varName1=condVar1[0]+"["+randomElement+"]"
      else: # condVar1 is NOT a buffer
        varName1=condVar1[0]
      condition=varName1+" "+operator+" "+randomConstant(condVar1[1])

  elif (len(availableFxns)>0):
    # choose a constant, a relationalOperator, and 2 functionCalls
    relationalOperators=["==", "!=", ">", "<", ">=", "<="]
    operator=random.choice(relationalOperators)
    funcMeta1=random.choice(availableFxns)
    funcCall1=createFxnCallText(funcMeta1, variables)
    funcMeta2=random.choice(availableFxns)
    funcCall2=createFxnCallText(funcMeta2, variables)

    # choose what kind of condition you want to return
    choice = random.choice(["f", "frf", "frc"])

    if choice=="f":
      condition=funcCall1

    elif choice=="frf":
      condition=funcCall1+" "+operator+" "+funcCall2

    else: # if choice=="frc":
      condition=funcCall1+" "+operator+" "+randomConstant()

  else: # neither
    condition=randomConstant()

  return condition

'''
nonBranchingElement creates an assignment, calls a function, prints something, or gets input from the user.
Assignments are just operations where the result is stored in memory.
INPUTS:
OUTPUTS:
'''
def nonBranchingElement(variables, potentialFxns, isFxn):
  # isFxn means is this a function other than main()
  #TODO: don't need a double list here.
  while (1):
    elements=[]# elements is a list of lines for the non-branching element
    elementText=""
    choice=random.choice(["assignment","call a function","print","get input"])
    if choice=="assignment":
      if len(variables)==0:
        continue
      elementText=elementText + operation(variables) + ";"
      elements=[[elementText]]
      return elements
    elif choice=="call a function":
      if not isFxn:
        if len(potentialFxns)==0:
          continue
        # choose a function
        chosenFunction=random.choice(potentialFxns)
        # call the function
        elementText=elementText + createFxnCallText(chosenFunction, variables) + ";"
        elements=[[elementText]]
        return elements
      else:
        pass
    elif choice=="print": 
      elementText="fprintf(stdout, \""+randomString()+"\");"
      elements=[[elementText]]
      return elements
    else: # get user input
      if len(variables)==0:
        continue
      inputVariable=random.choice(variables)
      elements=[getUserInput(inputVariable)]
      return elements

'''
randomString returns a random string
'''
def randomString():
  #MAX_WORDS_RANDOM_STRING=10 # the number of words in a random string
  #MAX_LETTERS_RANDOM_STRING_WORD=10 # the number of letters in a random string word
  randomSentence=""
  letters=[]
  # numbers
  #for i in range(48,57+1): # these are ascii values
  #  letters.append(chr(i))
  # lowercase letters
  for i in range(65,90+1):
    letters.append(chr(i))
  # uppercase letters
  for i in range(97,122+1):
    letters.append(chr(i))

  for word in range(random.randint(1,MAX_WORDS_RANDOM_STRING+1)):
    randomWord=""
    for letter in range(random.randint(1,MAX_LETTERS_RANDOM_STRING_WORD+1)):
      randomLetter=random.choice(letters)
      randomWord=randomWord+randomLetter
    randomSentence=randomSentence+randomWord+" "
  randomSentence=randomSentence[:-1]# get rid of the last space character
  punctuation=[".",":","?","|",">", "#", "$", ">>"]
  randomSentence=randomSentence+random.choice(punctuation)
  return randomSentence

'''
operation combines operands and operators to form an operation
INPUTS: 
OUTPUTS:
'''
def operation(variables):
  global availableFxns
  operationText=""
#  variableTypes=["char","double","float", "int", "long", "short"]
#  arithmeticOperators=["+", "-", "*", "/", "%"]
#  relationalOperators=["==", "!=", ">", "<", ">=", "<="]
#  logicalOperators=["&&", "||", "!"]
#  bitwiseOperators=["&","|", "^", "~", "<<", ">>"]
#  assignmentOperators=["=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "^=", "|="]
#  unaryOperators=["++","--"]
  #operatorList=["+", "-", "*", "/", "+", "-", "*", "/", "%","&","|", "^", "~", "<<", ">>"]
#  operatorList=[]
  varList=[]
 
  # TODO implement ! and ~ operations
  numVars=random.randint(1,MAX_NUM_OPERANDS) # this is wrong (i don't need to roll variables, i need to choose rolled variables)
  for i in range(numVars):
    varList.append(random.choice(variables))

  if numVars==1: # unary operation
    variableName=varList[0][0]
    variableType=varList[0][1]
    
    if len(varList[0])>2: #if the chosen variable is a buffer
      # use an element from the buffer, rather than the pointer to the buffer
      bufferLength=varList[0][2]
      randomElement=str(random.randint(0,bufferLength-1))
      variableName=variableName+"["+randomElement+"]"
    
    # use a prefix or postfix unary operator
    choice=random.choice(["prefix","postfix"])
    if choice=="prefix":
      operationText=operationText+random.choice(["++","--"])+variableName
    else: # choice=="postfix"
      operationText=operationText+variableName+random.choice(["++","--"])

    return operationText

  else: # assignment operation
    if (varList[0][1]=="double") or (varList[0][1]=="float"):# is the 0th variable a double or a float?
      availableAssignmentOperators=["=", "+=", "-=", "*=", "/="]
      availableRelationalOperators=["==", "!=", ">", "<", ">=", "<="]
      availableOperators=["+", "-", "*", "/", "&&", "||"]
      castFloatsAndDoubles=False

    else: # 0th variable is neither a double or a float
      availableAssignmentOperators=["=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "^=", "|="]
      availableRelationalOperators=["==", "!=", ">", "<", ">=", "<="]
      availableOperators=["+", "-", "*", "/", "%", "&&", "||", "&","|", "^", "<<", ">>"]
      castFloatsAndDoubles=True

  # choose an assignmentOperator
  assignmentOperator=random.choice(availableAssignmentOperators)
  
  # update the operationText for the first variable
  if len(varList[0])>2: # is the first variable a buffer?
    randomElement=str(random.randint(0,varList[0][2]))
    firstVariableName=varList[0][0]+"["+randomElement+"]"
  else:
    firstVariableName=varList[0][0]

  operationText=operationText+firstVariableName+" "+ assignmentOperator
  
  # for the remanining variables 
  for chosenVariable in varList[1:]:
    chosenVariableName=chosenVariable[0]
    if len(chosenVariable)>2: # buffer
      randomElement=str(random.randint(0,chosenVariable[2]))
      chosenVariableName=chosenVariableName+"["+randomElement+"]"
    chosenVariableType=chosenVariable[1]
    chosenOperator=random.choice(availableOperators)
    if (castFloatsAndDoubles): # first variable was neither a float nor a double
      if (chosenVariableType=="float") or (chosenVariableType=="double"):
        operationText=operationText+" (long)"+chosenVariableName+" "+chosenOperator 

    else: # first variable was either a float or a double
      if (chosenVariableType=="float") or (chosenVariableType=="double"):
        operationText=operationText+" "+chosenVariableName+" "+chosenOperator 

  # remove last operator
  operationText=operationText.split()[:-1]
  operationText=" ".join(operationText)

  return operationText
#def operation(variables):
#  #TODO: some operators can only be used with certain operands
#  #      so, choose a variable, choose an appropriate operator
#  #      and then, if applicable, choose the next variable
#  #TODO: create a flow chart and redo this function more neatly
#  global availableFxns
#  operationText=""
#  #arithmeticOperators=["+", "-", "*", "/", "%"]#, ++, --
#  #relationalOperators=["==", "!=", ">", "<", ">=", "<="] # relational operators are used to test conditions
#  #logicalOperators=["&&", "||", "!"]#, ?: # i don't want to program for a ternary operator edge case
#  #bitwiseOperators=["&","|", "^", "~", "<<", ">>"]
#  assignmentOperators=["=", "+=", "-=", "*=", "/="]#, "%=", "<<=", ">>=", "&=", "^=", "|="] TODO
#  unaryOperators=["++","--"]
#  operatorList=["+", "-", "*", "/", "+", "-", "*", "/"]#, "%","&","|", "^", "~", "<<", ">>"] TODO
#  # decide if unary operation
#  unaryChoice=random.randint(0,1)
#  # if so, increment or decrement a variable
#  if unaryChoice:
#    # choose increment or decrement
#    operationText=operationText+random.choice(unaryOperators)
#    # choose a variable
#    operationText=operationText+random.choice(variables)[0]
#    return operationText
#
#  # otherwise, choose a number of operands (number of operators =n-1, where n is the number of operands)
#  else:
#    numOperands=random.randint(3,MAX_NUM_OPERANDS)
#    numOperators=numOperands-2
#  # combine the operators and operands (alternate operand operator operand operator ...)
#  # each operand has a chance to have a pre- or post-fixed increment or decrement operator
#  #TODO: make it possible to use valid function returns as right-hand operands
#  #TODO: make a function that returns an appropriate source (variable, function return, whatever)
#    operationText=operationText+random.choice(variables)[0]+random.choice(assignmentOperators) #A=
#    for i in range(numOperands-2): # skip first and last A=B+C+D+E to get B+ C+ D+ pattern
#      affix=0
#      prefix=0
#      #if random.randint(1,100)>PRE_POST_CHANCE: # will there be a pre- or post-fix unary operation?
#      #  affix=1
#        #if random.randint(0,1): # if so, will it be pre- or postfix?
#        #  prefix=1
#      #if affix==1 and prefix==1:
#      #  operationText=operationText+random.choice(unaryOperators)
#      operationText=operationText+random.choice(variables)[0]
#      operationText=operationText+random.choice(operatorList)
#      #if affix==1 and prefix==0:
#      #  operationText=operationText+random.choice(unaryOperators)
#  # add last operand
#    operationText=operationText+random.choice(variables)[0]
#  return operationText

#'''
#assignment() creates an assignment statement
#INPUTS:
#OUTPUTS:
#'''
#def assignment():
#  pass

'''
getUserInput takes input from a user
this should be as non-buggy as possible (we will have a different function for bugs)
INPUT: variable is a list of the form ["name", "type"] 
OUTPUT: text that will get user input
'''
def getUserInput(variable):
  userInputLines=[]
  # prompt the user?
  if (random.randint(0,1)):
    userPrompt="fprintf(stdout, \""+randomString()+"\");"
    userInputLines.append(userPrompt)
  # determine variable type
  varType=variable[1]
  #TODO: strings
  if varType=="char":
    varToken="%c"
    inputLength="1"
  elif varType=="double":
    varToken="%ld"
    inputLength="1"
  elif varType=="float":
    varToken="%f"
    inputLength="1"
  elif varType=="int":
    varToken="%d"
    inputLength="1"
  elif varType=="long":
    varToken="%d"
    inputLength="1"
  else:# varType=="short":
    varToken="%hu"
    inputLength="1"
  # use scanf to get input from user
  userInputLines.append("scanf(\""+varToken+"\", &"+variable[0]+");")
  userInputLines.append("dumpStdin();")
  return userInputLines

def cSignedMax(cType):
  bits = ctypes.sizeof(cType) * 8
  maxValue=(2**(bits-1))-1
  return maxValue

def cSignedLowest(cType):
  bits = ctypes.sizeof(cType) * 8
  lowestValue=-(2**(bits-1))
  return lowestValue

def cUnsignedMax(cType):
  bits = ctypes.sizeof(cType) * 8
  maxValue=(2**bits)-1
  return maxValue
