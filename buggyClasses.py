import random
from copy import deepcopy
from buggyHeader import *
from defaultvalues import *
TROUBLESHOOTING=False
'''
Fxn class
'''
class Fxn:
  def __init__(self, fxnMeta, globalVariables, potentialFxns, lineNumber,
  max_layers_of_tree=MAX_LAYERS_OF_TREE,
  min_layers_of_tree=MIN_LAYERS_OF_TREE,
  max_number_of_leafs_per_layer=MAX_NUMBER_OF_LEAFS_PER_LAYER,
  min_number_of_leafs_per_layer=MIN_NUMBER_OF_LEAFS_PER_LAYER,
  max_number_of_conditions_per_leaf=MAX_NUMBER_OF_CONDITIONS_PER_LEAF,
  min_number_of_conditions_per_leaf=MIN_NUMBER_OF_CONDITIONS_PER_LEAF,
  max_number_of_variables_per_leaf=MAX_NUMBER_OF_VARIABLES_PER_LEAF,
  min_number_of_variables_per_leaf=MIN_NUMBER_OF_VARIABLES_PER_LEAF,
  max_number_of_variables_per_fxn=MAX_NUMBER_OF_VARIABLES_PER_FXN,
  min_number_of_variables_per_fxn=MIN_NUMBER_OF_VARIABLES_PER_FXN,
  max_number_of_elements_per_leaf=MAX_NUMBER_OF_ELEMENTS_PER_LEAF,
  min_number_of_elements_per_leaf=MIN_NUMBER_OF_ELEMENTS_PER_LEAF,
  max_number_of_elements_per_fxn=MAX_NUMBER_OF_ELEMENTS_PER_FXN,
  min_number_of_elements_per_fxn=MIN_NUMBER_OF_ELEMENTS_PER_FXN,
  probability_of_if=PROBABILITY_OF_IF,
  interestingness=INTERESTINGNESS
):
    probability_of_tree=defaultvalues.PROBABILITY_OF_TREE
    max_layers_of_tree=int(max_layers_of_tree)
    min_layers_of_tree=int(min_layers_of_tree)
    max_number_of_leafs_per_layer=int(max_number_of_leafs_per_layer)
    min_number_of_leafs_per_layer=int(min_number_of_leafs_per_layer)
    max_number_of_conditions_per_leaf=int(max_number_of_conditions_per_leaf)
    min_number_of_conditions_per_leaf=int(min_number_of_conditions_per_leaf)
    max_number_of_variables_per_leaf=int(max_number_of_variables_per_leaf)
    min_number_of_variables_per_leaf=int(min_number_of_variables_per_leaf)
    max_number_of_variables_per_fxn=int(max_number_of_variables_per_fxn)
    min_number_of_variables_per_fxn=int(min_number_of_variables_per_fxn)
    max_number_of_elements_per_leaf=int(max_number_of_elements_per_leaf)
    min_number_of_elements_per_leaf=int(min_number_of_elements_per_leaf)
    max_number_of_elements_per_fxn=int(max_number_of_elements_per_fxn)
    min_number_of_elements_per_fxn=int(min_number_of_elements_per_fxn)
    probability_of_if=float(probability_of_if)
    interestingness=int(interestingness)
    self.name=fxnMeta[0]
    self.type=fxnMeta[1]
    self.args=fxnMeta[2:]
    self.globalVariables=deepcopy(globalVariables)
    self.variables=deepcopy(globalVariables) # a 2d list representing the variables available to this function before the tree
    self.lineNumber=lineNumber
    self.preamble=[]
    self.postamble=[]
    self.elements=[]        # the non-branching elements in this function before the tree
    self.tree=None # the tree for this function
    preambleString= self.type+" "+self.name+" ("
    if len(self.args)>0:
      if self.name!="main":
        for i, arg in enumerate(self.args):
          funcVarName="funcVar"+str(i)
          funcVarType=arg
          preambleString=preambleString+funcVarType+" "+funcVarName+", "
          # append the funcVars to self.variables
          dummyFuncVar=[funcVarName, funcVarType]
          self.variables.append(dummyFuncVar)
        preambleString=preambleString[:-2]+")"
      else:
        preambleString="int main (int argc, char **argv)"
    else:
      preambleString=preambleString+")"
    self.preamble.append(preambleString)
    self.preamble.append("  {")

    # roll some fxn-specific variables
    for i in range(random.randint(MIN_NUMBER_OF_VARIABLES_PER_FXN,max_number_of_variables_per_fxn)):
      var=variable()
      self.appendVariable(var)
      #self.preamble.append(declareVariableText(1,var)) # 1 means to initialize the variable

    # roll some fxn-specific elements 
    for i in range(random.randint(MIN_NUMBER_OF_ELEMENTS_PER_FXN,max_number_of_elements_per_fxn)):
      isFxn=False
      for element in nonBranchingElement(self.variables, potentialFxns, isFxn):
        self.appendElement(element)
      
    if self.type!="void":
      if self.name=="main":
        self.postamble.append("    return 0;")
      else:
        self.postamble.append("    return "+getRelevantSource(self.type, self.variables)+";")
    self.postamble.append("  }")

    # decide whether or not to create a tree
    #TODO:
    #if random.random() < probability_of_tree:
    if 1:
      treeVars=deepcopy(globalVariables)
      for var in self.variables:
        treeVars.append(var)

      if self.name=="main":
        # create a bug tree
        #btRootIndex=self.tree.leafs[-1].getIndex()+1
        #bt = BugTree(globalVariables, availableFxns, rootIndex=btRootIndex, interestingness=2)
        self.tree=BuggedTree(treeVars, availableFxns, lineNumber, 
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
          interestingness=interestingness) 

      else:
        self.tree=Tree(treeVars, availableFxns, lineNumber, 
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
      
#
#        # attach the bug tree to the tree
#        for leaf in bt.leafs:
#          self.tree.leafs.append(leaf)
#        #TODO update the root's children with the bt root
#        rootsChildren=self.tree.leafs[0].getChildren()
#        insertBTIndex=random.randint(0,len(rootsChildren))
#        rootsChildren.insert(insertBTIndex, btRootIndex)
#        self.tree.leafs[0].setChildren(rootsChildren)
#        #self.lineNumber=self.tree.lineNumber
#
#        # update the indents for the leafs
#        for leaf in self.tree.leafs:
#          if leaf.getIndent()==-99: # part of the bad tree
#            if leaf.getIndex()==0:
#              leaf.setIndent(-1)
#            else:
#              leaf.setIndent(self.tree.leafs[leaf.getParent()].getIndent()+1)
#        # update the lastchild status for layer 1 (the children of self.tree.leafs[0])
#        rootsChildren=self.tree.leafs[0].getChildren()
#        for child in rootsChildren:
#          if child != rootsChildren[-1]:
#            self.tree.leafs[child].setLastChild(False)
#          else:
#            self.tree.leafs[child].setLastChild(True)
            
      

  def getVariables(self):
    return self.variables

  def setVariables(self, newVariables):
    self.variables=newVariables

  def appendVariable(self, newVariable):
    self.variables.append(newVariable)

  def getElements(self):
    return self.Elements

  def setElements(self, newElements):
    self.elements=newElements

  def appendElement(self, newElement):
    self.elements.append(newElement)

  def __str__(self):
    fxnString=""
    # print the fxn's preamble
    for line in self.preamble:
      fxnString=fxnString+line+'\n'
      self.lineNumber+=1
    # print the fxn's variables (but not the global variables)
    for var in self.variables:
      if var not in self.globalVariables and var[0][:-1]!="funcVar":
        fxnString=fxnString+"    "+declareVariableText(1,var)+'\n' # 1 means to initialize the variable
        self.lineNumber+=1
    # print the fxn's elements
    for element in self.elements:
      for line in element:
        fxnString=fxnString+"    "+line+'\n'
        self.lineNumber+=1

    # if you have a tree, print the tree
    if self.tree!=None:
      for line in self.tree.getTreeLines():
        if line[-2:]=="//": # 2 backslashes
          fxnString=fxnString+line+" bug path: line number: "+str(self.lineNumber)+'\n'
        else:
          fxnString=fxnString+line+'\n'
        self.lineNumber+=1

    # print the fxn's postamble
    for line in self.postamble:
      fxnString=fxnString+line+'\n'
      self.lineNumber+=1
    fxnString=fxnString[:-1] # get rid of last newline character
    
    return fxnString

  #def __str__(self):
  #  treeString=""
  #  for i, leaf in enumerate(self.leafs):
  #    treeString=treeString+str(i)+": "+str(leaf)+"\n"
  #  treeString=treeString[:-1]
  #  return treeString

'''
Tree class
Trees have a root and leafs.
the root and leafs are lexical Elements.
Elements are loaded into the list leafs.
leafStack is a stack (implemented as a list) of ints that represent the indices of Elements in leafs.
To use the tree, element indices are pushed onto and popped from leafStack.
The currentLeafIndex starts at 0 and is updated to the most recently popped off index from leafStack.
'''
class Tree:
  def __init__(self, globalVariables, potentialFxns, lineNumber,
  max_layers_of_tree=MAX_LAYERS_OF_TREE,
  min_layers_of_tree=MIN_LAYERS_OF_TREE,
  max_number_of_leafs_per_layer=MAX_NUMBER_OF_LEAFS_PER_LAYER,
  min_number_of_leafs_per_layer=MIN_NUMBER_OF_LEAFS_PER_LAYER,
  max_number_of_conditions_per_leaf=MAX_NUMBER_OF_CONDITIONS_PER_LEAF,
  min_number_of_conditions_per_leaf=MIN_NUMBER_OF_CONDITIONS_PER_LEAF,
  max_number_of_variables_per_leaf=MAX_NUMBER_OF_VARIABLES_PER_LEAF,
  min_number_of_variables_per_leaf=MIN_NUMBER_OF_VARIABLES_PER_LEAF,
  max_number_of_variables_per_fxn=MAX_NUMBER_OF_VARIABLES_PER_FXN,
  min_number_of_variables_per_fxn=MIN_NUMBER_OF_VARIABLES_PER_FXN,
  max_number_of_elements_per_leaf=MAX_NUMBER_OF_ELEMENTS_PER_LEAF,
  min_number_of_elements_per_leaf=MIN_NUMBER_OF_ELEMENTS_PER_LEAF,
  max_number_of_elements_per_fxn=MAX_NUMBER_OF_ELEMENTS_PER_FXN,
  min_number_of_elements_per_fxn=MIN_NUMBER_OF_ELEMENTS_PER_FXN,
  probability_of_if=PROBABILITY_OF_IF
):
    max_layers_of_tree=int(max_layers_of_tree)
    min_layers_of_tree=int(min_layers_of_tree)
    max_number_of_leafs_per_layer=int(max_number_of_leafs_per_layer)
    min_number_of_leafs_per_layer=int(min_number_of_leafs_per_layer)
    max_number_of_conditions_per_leaf=int(max_number_of_conditions_per_leaf)
    min_number_of_conditions_per_leaf=int(min_number_of_conditions_per_leaf)
    max_number_of_variables_per_leaf=int(max_number_of_variables_per_leaf)
    min_number_of_variables_per_leaf=int(min_number_of_variables_per_leaf)
    max_number_of_variables_per_fxn=int(max_number_of_variables_per_fxn)
    min_number_of_variables_per_fxn=int(min_number_of_variables_per_fxn)
    max_number_of_elements_per_leaf=int(max_number_of_elements_per_leaf)
    min_number_of_elements_per_leaf=int(min_number_of_elements_per_leaf)
    max_number_of_elements_per_fxn=int(max_number_of_elements_per_fxn)
    min_number_of_elements_per_fxn=int(min_number_of_elements_per_fxn)
    probability_of_if=float(probability_of_if)
    self.currentLeafIndex=0 # the index of the current leaf, which starts at 0 and is updated to the index of the leaf most recently popped off of the leafStack[].
    self.leafStack=[]       # a stack for keeping track of the indices of the elements in leafs[] during tree traversal
    self.leafs=[]           # a list of the leafs in the tree
    self.globalVariables=deepcopy(globalVariables)
    self.variables=deepcopy(globalVariables) # a 2d list representing the variables available to this function before the tree
    self.preamble=[]
    self.postamble=[]

      
    # create the pretree structure
    if TROUBLESHOOTING:
      self.pretree=[[0]]
      pretree=self.pretree
    else:
      pretree=[[0]] # a list of lists, where each sub-list represents a layer
    i=1 # keep track of the next element's index to place in the tree
    layers=random.randint(MIN_LAYERS_OF_TREE, max_layers_of_tree)-1 # -1 to account for the root
    for layer in range(layers):
      numLeafs=random.randint(min_number_of_leafs_per_layer, max_number_of_leafs_per_layer)
      # create a list of indices
      thisLayer=[]
      for leaf in range(numLeafs):
        thisLayer.append(i)
        i=i+1
      pretree.append(thisLayer)

    # create a bunch of blank Elements and put them in leafs[] with the root at index 0
    for i, layer in enumerate(pretree):
      for leaf in layer:
        parent=None
        index=leaf
        children=[]
        element=Element(parent,index, children)
        self.leafs.append(element)
        
    # set parent relationships
    self.leafs[0].setParent(None) # root is a special case
    for i, layer in enumerate(pretree[1:], start=1):#skip the root. i starts at 1
      previousLayer=pretree[i-1]
      for element in layer:
        parent=random.choice(previousLayer)
        self.leafs[element].setParent(parent)

    # set children relationships
    for parentLeaf in self.leafs:
      for childLeaf in self.leafs:
        if parentLeaf.getIndex() == childLeaf.getParent():
          parentLeaf.setChild(childLeaf.getIndex())
    
    # convert some of the Elements to Loops
    for i, leaf in enumerate(self.leafs):
      randomRoll=random.random() # a random number between 0.0 and 1.0
      if randomRoll >= probability_of_if:
        self.leafs[i]=Loop(leaf)

    # convert remaining Elements in leafs[] to PrimaryBranch and SecondaryBranch objects
    for leaf in self.leafs:
      if type(leaf)!=Loop:
        if leaf.getParent()==None: # root
          self.leafs[0]=PrimaryBranch(leaf)
        else: # not root
          siblings=self.leafs[leaf.getParent()].children
          siblingIndex=siblings.index(leaf.getIndex())# leaf.getIndex() returns the index in leafs, need the index in siblings
          if siblingIndex!=0: # is there a child to the left?
            if type(self.leafs[siblings[siblingIndex-1]])==PrimaryBranch: # is the child to the left a PrimaryBranch?
              choice=random.choice(["PrimaryBranch","SecondaryBranch"])
              if choice=="PrimaryBranch":
                self.leafs[leaf.getIndex()]=PrimaryBranch(leaf)
              else: # choice=="SecondaryBranch"
                self.leafs[leaf.getIndex()]=SecondaryBranch(leaf)
            elif type(self.leafs[siblings[siblingIndex-1]])==SecondaryBranch: # is the child to the left a SecondaryBranch?
              if self.leafs[siblings[siblingIndex-1]].isElse==True: # is the child to the left an 'else'?
                self.leafs[leaf.getIndex()]=PrimaryBranch(leaf)
              else: # the child is not an 'else'
                choice=random.choice(["PrimaryBranch","SecondaryBranch"])
                if choice=="PrimaryBranch":
                  self.leafs[leaf.getIndex()]=PrimaryBranch(leaf)
                else: # choice=="SecondaryBranch"
                  choice=random.choice(["else-if","else"])
                  if choice=="else-if":
                    self.leafs[leaf.getIndex()]=SecondaryBranch(leaf)
                  else: # choice=="else"
                    self.leafs[leaf.getIndex()]=SecondaryBranch(leaf)
                    self.leafs[leaf.getIndex()].setElse()
            else: # the child to the left is not a SecondaryBranch
              self.leafs[leaf.getIndex()]=PrimaryBranch(leaf)
          else: #there isn't a child to the left
            self.leafs[leaf.getIndex()]=PrimaryBranch(leaf)

    # fix indents for leafs
    for i, layer in enumerate(pretree):
      for leaf in layer:
        self.leafs[leaf].setIndent(i)

    # determine lastChild status
    for parentLeaf in self.leafs:
       if len(parentLeaf.getChildren())==0: # parentLeaf has no children
         pass
       else:
         children=parentLeaf.getChildren()
         lastChild=children[-1]
         self.leafs[lastChild].setLastChild(True)

    # set Element variables
    for leaf in self.leafs:
      for i in range(random.randint(MIN_NUMBER_OF_VARIABLES_PER_LEAF,max_number_of_variables_per_leaf)):
        leaf.appendVariable(variable())
    
    # update the parentVariables of child Elements
    for leaf in self.leafs:
      if leaf.getParent()!=None: # not the root
        for var in self.leafs[leaf.getParent()].getVariables():
          leaf.appendParentVariable(var)
      else: # the parent variables of the root are the global variables 
        for var in self.variables:
          leaf.appendParentVariable(var)

    # roll the conditions
    for leaf in self.leafs:
      leaf.rollConditions()

    # roll the preambles and postambles
    for leaf in self.leafs:
      leaf.rollAmbles()

    # rolling preambles and postambles resets the 'else' preamble
    # so, need to re-setElse()
    for leaf in self.leafs:
      if type(leaf)==SecondaryBranch:
        if leaf.isElse==True:
          leaf.setElse()

    # update the postambles of Elements with lastChild==True
    lastChildren=[]
    for leaf in self.leafs:
      if len(leaf.children)!=0:
        lastChildren.append(leaf.children[-1])

    for child in lastChildren:
      for postamble in self.leafs[self.leafs[child].getParent()].getPostamble():
        self.leafs[child].appendPostamble(postamble)

    # update the nonbranching elements of the leafs
    for leaf in self.leafs:
      for i in range(random.randint(MIN_NUMBER_OF_ELEMENTS_PER_LEAF,max_number_of_elements_per_leaf)):
        isFxn=True
        for element in nonBranchingElement(self.variables, potentialFxns, isFxn):
          leaf.appendElement(element)
    
  def getCurrentLeafIndex(self):
    return self.currentLeafIndex

  def pushChildren(self):
    children=self.getCurrentLeaf().getChildren()
    if (len(children)==0):
      return None
    else:
      for child in reversed(children):
        self.leafStack.append(child)
      return len(children)

  def pushLeaf(self, leafIndexToPush):
    self.leafStack.append(leafIndexToPush)

  def popLeaf(self):
    newCurrentLeafIndex=self.leafStack.pop()
    self.currentLeafIndex=newCurrentLeafIndex
    return newCurrentLeafIndex

  def getCurrentLeaf(self):
    currentLeaf=self.leafs[self.currentLeafIndex]
    return currentLeaf

  def getCurrentLeafPreamble(self):
   currentLeaf=self.getCurrentLeaf()
   return currentLeaf.getPreamble()

  def getCurrentLeafConditions(self):
    currentLeaf=self.getCurrentLeaf()
    return currentLeaf.getConditions()
  
  def getCurrentLeafElements(self):
    currentLeaf=self.getCurrentLeaf()
    return currentLeaf.getElements()

  def getCurrentLeafPostamble(self):
    currentLeaf=self.getCurrentLeaf()
    return currentLeaf.getPostamble()

  def getCurrentLeafParent(self):
    currentLeaf=self.leafs[self.currentLeafIndex]
    return currentLeaf.getParent()

  def getCurrentLeafAncestors(self):
    currentLeaf=self.leafs[self.currentLeafIndex]
    return currentLeaf.getAncestors()
  
  def getCurrentLeafVariables(self):
    currentLeaf=self.getCurrentLeaf()
    return currentLeaf.getVariables()
  
  def getCurrentLeafIndent(self):
    currentLeaf=self.getCurrentLeaf()
    return currentLeaf.getIndent()

  def getVariables(self):
    return self.variables

  def setVariables(self, newVariables):
    self.variables=newVariables

  def appendVariable(self, newVariable):
    self.variables.append(newVariable)

  def getElements(self):
    return self.Elements

  def setElements(self, newElements):
    self.elements=newElements

  def appendElement(self, newElement):
    self.elements.append(newElement)

  def getTreeLines(self):
    treeLineList=[]
    # for diagnostics 
    if TROUBLESHOOTING:
      print(self.pretree)
      for leaf in self.leafs:
        print(str(leaf))

    # traverse the tree and print the associated lexical elements
    self.pushLeaf(0)
    while(len(self.leafStack)>0):
      self.popLeaf()
      indent="  "*self.getCurrentLeafIndent()
      # the current leaf is the popped leaf
      for preamble in self.getCurrentLeafPreamble():
        treeLineList.append(indent+"    "+preamble)
      for var in self.getCurrentLeafVariables():
        # don't re-declare variables
        if (var not in self.globalVariables) and (var not in self.variables) and (not(len(var)>3)): # only declare variables that haven't been declared yet
          treeLineList.append(indent+"      "+declareVariableText(1,var))
      for element in self.getCurrentLeafElements():
        for line in element:
          treeLineList.append(indent+"      "+line)
      if (self.pushChildren()==None): # pushChildren pushes all of the children indices onto leafstack, unless there are none, in which case it returns None
        for i, postamble in enumerate(self.getCurrentLeafPostamble()):
          treeLineList.append(indent[2*i:]+"    "+postamble)
    # print the tree's postamble
    for line in self.postamble:
      treeLineList.append(line)

    return treeLineList

  def __str__(self):
    treeString=""
    # for diagnostics 
    if TROUBLESHOOTING:
      print(self.pretree)
      for leaf in self.leafs:
        print(str(leaf))

    # print the tree's preamble
    for line in self.preamble:
      treeString=treeString+line+'\n'
      self.lineNumber+=1
    # print the tree's variables (but not the global variables)
    for var in self.variables:
      if var not in self.globalVariables:
        treeString=treeString+"    "+declareVariableText(1,var)+'\n' # 1 means to initialize the variable
        self.lineNumber+=1
    # print the tree's elements
    for element in self.elements:
      for line in element:
        treeString=treeString+"    "+line+'\n'
        self.lineNumber+=1
    # traverse the tree and print the associated lexical elements
    self.pushLeaf(0)
    while(len(self.leafStack)>0):
      self.popLeaf()
      indent="  "*self.getCurrentLeafIndent()
      # the current leaf is the popped leaf
      for preamble in self.getCurrentLeafPreamble():
        treeString=treeString+indent+"    "+preamble+" //lineNumber: "+str(self.lineNumber)+'\n'
        self.lineNumber+=1
      for var in self.getCurrentLeafVariables():
        # don't re-declare variables
        if (var not in self.globalVariables) and (var not in self.variables) and (not(len(var)>2)): # only declare variables that haven't been declared yet
          treeString=treeString+indent+"      "+declareVariableText(1,var)+" //lineNumber: "+str(self.lineNumber)+'\n'
          self.lineNumber+=1
      for element in self.getCurrentLeafElements():
        for line in element:
          treeString=treeString+indent+"      "+line+" //lineNumber: "+str(self.lineNumber)+'\n'
          self.lineNumber+=1
      if (self.pushChildren()==None): # pushChildren pushes all of the children indices onto leafstack, unless there are none, in which case it returns None
        for i, postamble in enumerate(self.getCurrentLeafPostamble()):
          treeString=treeString+indent[2*i:]+"    "+postamble+" //lineNumber: "+str(self.lineNumber)+'\n'
          self.lineNumber+=1
    # print the tree's postamble
    for line in self.postamble:
      treeString=treeString+line+'\n'
      self.lineNumber+=1
    treeString=treeString[:-1] # get rid of last newline character
    
    return treeString

  #def __str__(self):
  #  treeString=""
  #  for i, leaf in enumerate(self.leafs):
  #    treeString=treeString+str(i)+": "+str(leaf)+"\n"
  #  treeString=treeString[:-1]
  #  return treeString

'''
Element class
'''
class Element:
  def __init__(self, parent, index, children):
    self.parent=parent          # an int. this element's parent's index in Tree.leafs[]
    self.index=index            # an int. the index of this element in Tree.leafs[]
    self.children=children      # a list of ints. each item in the list is the index of a child in Tree.leafs[]
    self.indent=0               # an int. the indent (equal to the layer number) for text produced by this leaf
    self.preamble=[]            # a string representing the preamble of the element
    self.conditions=[]          # a list of strings representing the condition(s) of the Element
    self.elements=[]            # a list of strings representing the non-loop/non-branch elements within this Element
    self.postamble=[]           # a list of strings. each string represents a postamble
    self.parentVariables=[]     # a 2d list of strings. each sublist represents a variable available to this Element from its ancestors.
    self.variables=[]           # a 2d list of strings. each sublist represents a variable available to this Element.
    self.lastChild=False        # a bool. 

  def getParent(self):
    return self.parent

  def setParent(self, newParent):
    self.parent=newParent

  def getIndex(self):
    return self.index

  def setIndex(self, newIndex):
    self.index=newIndex

  def getChildren(self):
    return self.children

  def setChild(self,child):
    self.children.append(child)

  def setChildren(self, newChildren):
    self.children=newChildren

  def setLastChild(self, status):
    self.lastChild=status

  def getIndent(self):
    return self.indent

  def setIndent(self, newIndent):
    self.indent=newIndent

  def getPreamble(self):
    return self.preamble

  def setPreamble(self, newPreamble):
    self.preamble=newPreamble

  def appendPreamble(self, newPreamble):
    self.preamble.append(newPreamble)

  def getConditions(self):
    return self.conditions

  def setConditions(self, newConditions):
    self.conditions=newConditions

  def getElements(self):
    return self.elements

  def setElements(self, newElements):
    self.elements=newElements

  def appendElement(self, newElement):
    self.elements.append(newElement)

  def getPostamble(self):
    return self.postamble

  def setPostamble(self, newPostamble):
    self.postamble=newPostamble

  def appendPostamble(self, newPostamble):
    self.postamble.append(newPostamble)

  def getVariables(self):
    return self.variables

  def setVariables(self, newVariables):
    self.variables=newVariables

  def appendVariable(self, newVariable):
    self.variables.append(newVariable)

  def getParentVariables(self):
    return self.parentVariables

  def setParentVariables(self, newVariables):
    self.parentVariables=newVariables

  def appendParentVariable(self, newVariable):
    self.parentVariables.append(newVariable)

  def rollConditions(self):
    #TODO: available fxns
    self.setConditions([makeCondition(self.getParentVariables(), availableFxns)])
    
  def __str__(self):
    return "parent: "+str(self.parent)+" | index: "+str(self.index)+" | children: "+str(self.children)+" | lastChild?: "+str(self.lastChild)+" | postamble: "+str(self.postamble)

'''
Loop class
'''
class Loop (Element):
  def __init__(self, element):
    super().__init__(parent=element.parent, index=element.index, children=element.children)

  def rollAmbles(self):
    condition=self.getConditions()[0] 
    loopChoice=random.choice(["while","do-while","for"])
    if loopChoice=="while":
      self.appendPreamble("while("+condition+"){")
      self.setPostamble(["}"])
      
    elif loopChoice=="do-while":
      self.appendPreamble("do{")
      self.setPostamble(["}while("+condition+");"])

    else: #loopChoice=="for"
      var=iteratorVariable()
      initialVar="int "+ var[0] + "=0"
      incrementVar=var[0]+"++"
      # append two blank strings to var to make these variables distinct from other variables and buffers
      var.append("")
      var.append("")
      # var now looks like ["name","type","",""]
      self.appendVariable(var)
      self.appendPreamble("for("+initialVar+"; "+condition+"; "+incrementVar+"){")
      self.setPostamble(["}"])
    

'''
PrimaryBranch class
'''
class PrimaryBranch (Element):
  def __init__(self, element):
    super().__init__(parent=element.parent, index=element.index, children=element.children)
  
  def rollAmbles(self):
    condition=self.getConditions()[0] 
    self.appendPreamble("if("+condition+"){")
    self.setPostamble(["}"])
      

'''
SecondaryBranch class
'''
class SecondaryBranch (Element):
  def __init__(self, element):
    super().__init__(parent=element.parent, index=element.index, children=element.children)
    self.isElse=False

  def rollAmbles(self):
    condition=self.getConditions()[0] 
    self.setPreamble(["else if("+condition+"){"])
    self.setPostamble(["}"])

  def setElse(self):
    self.setPreamble(["else{"])
    self.isElse=True

'''
BuggedTree class
'''
#TODO: the index for this root in the calling fxn will be something like len(leafs)
class BuggedTree:
  def __init__(self, globalVariables, potentialFxns, lineNumber,
  max_layers_of_tree=MAX_LAYERS_OF_TREE,
  min_layers_of_tree=MIN_LAYERS_OF_TREE,
  max_number_of_leafs_per_layer=MAX_NUMBER_OF_LEAFS_PER_LAYER,
  min_number_of_leafs_per_layer=MIN_NUMBER_OF_LEAFS_PER_LAYER,
  max_number_of_conditions_per_leaf=MAX_NUMBER_OF_CONDITIONS_PER_LEAF,
  min_number_of_conditions_per_leaf=MIN_NUMBER_OF_CONDITIONS_PER_LEAF,
  max_number_of_variables_per_leaf=MAX_NUMBER_OF_VARIABLES_PER_LEAF,
  min_number_of_variables_per_leaf=MIN_NUMBER_OF_VARIABLES_PER_LEAF,
  max_number_of_variables_per_fxn=MAX_NUMBER_OF_VARIABLES_PER_FXN,
  min_number_of_variables_per_fxn=MIN_NUMBER_OF_VARIABLES_PER_FXN,
  max_number_of_elements_per_leaf=MAX_NUMBER_OF_ELEMENTS_PER_LEAF,
  min_number_of_elements_per_leaf=MIN_NUMBER_OF_ELEMENTS_PER_LEAF,
  max_number_of_elements_per_fxn=MAX_NUMBER_OF_ELEMENTS_PER_FXN,
  min_number_of_elements_per_fxn=MIN_NUMBER_OF_ELEMENTS_PER_FXN,
  probability_of_if=PROBABILITY_OF_IF,
  rootIndex=0,
  interestingness=INTERESTINGNESS
):
    max_layers_of_tree=int(max_layers_of_tree)
    min_layers_of_tree=int(min_layers_of_tree)
    max_number_of_leafs_per_layer=int(max_number_of_leafs_per_layer)
    min_number_of_leafs_per_layer=int(min_number_of_leafs_per_layer)
    max_number_of_conditions_per_leaf=int(max_number_of_conditions_per_leaf)
    min_number_of_conditions_per_leaf=int(min_number_of_conditions_per_leaf)
    max_number_of_variables_per_leaf=int(max_number_of_variables_per_leaf)
    min_number_of_variables_per_leaf=int(min_number_of_variables_per_leaf)
    max_number_of_variables_per_fxn=int(max_number_of_variables_per_fxn)
    min_number_of_variables_per_fxn=int(min_number_of_variables_per_fxn)
    max_number_of_elements_per_leaf=int(max_number_of_elements_per_leaf)
    min_number_of_elements_per_leaf=int(min_number_of_elements_per_leaf)
    max_number_of_elements_per_fxn=int(max_number_of_elements_per_fxn)
    min_number_of_elements_per_fxn=int(min_number_of_elements_per_fxn)
    probability_of_if=float(probability_of_if)
    self.currentLeafIndex=0 # the index of the current leaf, which starts at 0 and is updated to the index of the leaf most recently popped off of the leafStack[].
    self.leafStack=[]       # a stack for keeping track of the indices of the elements in leafs[] during tree traversal
    self.leafs=[]           # a list of the leafs in the tree
    self.globalVariables=deepcopy(globalVariables)
    self.variables=deepcopy(globalVariables) # a 2d list representing the variables available to this function before the tree
    self.preamble=[]
    self.postamble=[]
    self.rootIndex=int(rootIndex)
    self.interestingness=int(interestingness)

      
    # create the pretree structure
    pretree=[[0]] # a list of lists, where each sub-list represents a layer
    #layers=random.randint(MIN_LAYERS_OF_TREE, max_layers_of_tree)-1 # -1 to account for the root
    layers=interestingness
    i=1 # keep track of the next element's index to place in the tree
    for layer in range(layers):
      numLeafs=random.randint(min_number_of_leafs_per_layer, max_number_of_leafs_per_layer)
      # create a list of indices
      thisLayer=[]
      for leaf in range(numLeafs):
        thisLayer.append(i)
        i=i+1
      pretree.append(thisLayer)
     
    # create a bunch of blank Elements and put them in leafs[] with the root at index 0
    for layer in pretree:
      for leaf in layer:
        parent=None
        index=leaf
        children=[]
        element=Element(parent,index, children)
        self.leafs.append(element)
        
    # set parent relationships
    # assuming that the pretree was created correctly, this code should be correct
    self.leafs[0].setParent(None) # root is a special case
    for i, layer in enumerate(pretree[1:], start=1):#skip the root. i starts at 1
      previousLayer=pretree[i-1]
      for element in layer:
        parent=random.choice(previousLayer)
        self.leafs[element].setParent(parent)

    # set children relationships
    for parentLeaf in self.leafs:
      for childLeaf in self.leafs:
        if parentLeaf.getIndex() == childLeaf.getParent():
          parentLeaf.setChild(childLeaf.getIndex())
    
    # make a clear path from the root to the bug
    chosenPathIndices=[]
    # start with a random element in the nth (=interestingness) layer
    # and work backwards to the root
    randomIndex=random.randint(0,len(pretree[-1])-1)
    randomElement=pretree[-1][randomIndex] # this is an index in leafs
    chosenParent=self.leafs[randomElement].getParent()
    chosenPathIndices.append(chosenParent)
    while (1):
      chosenParent=self.leafs[chosenParent].getParent()
      if chosenParent==None:
        break
      chosenPathIndices.append(chosenParent)
    chosenPathIndices = [element for element in reversed(chosenPathIndices)]

    for i, leaf in enumerate(self.leafs):
    # the root leaf is a PrimaryBranch element
      if i==0:
        self.leafs[i]=PrimaryBranch(leaf)
    # the rest of the leafs in the chosen path are also PrimaryBranch elements
      elif leaf.getIndex() in chosenPathIndices:
        self.leafs[i]=PrimaryBranch(leaf)

    #TODO only convert Elements, not PrimaryBranch or SecondaryBranch elements
    # convert some of the Elements to Loops
    for i, leaf in enumerate(self.leafs):
      randomRoll=random.random() # a random number between 0.0 and 1.0
      if (randomRoll >= probability_of_if) and (type(leaf)==Element):
        self.leafs[i]=Loop(leaf)

    # convert remaining Elements in leafs[] to PrimaryBranch and SecondaryBranch objects
    for leaf in self.leafs:
      if type(leaf)==Element: # if the leaf hasn't been set yet
        siblings=self.leafs[leaf.getParent()].children
        siblingIndex=siblings.index(leaf.getIndex())# leaf.getIndex() returns the index in leafs, need the index in siblings
        if siblingIndex!=0: # is there a child to the left?
          if type(self.leafs[siblings[siblingIndex-1]])==PrimaryBranch: # is the child to the left a PrimaryBranch?
            choice=random.choice(["PrimaryBranch","SecondaryBranch"])
            if choice=="PrimaryBranch":
              self.leafs[leaf.getIndex()]=PrimaryBranch(leaf)
            else: # choice=="SecondaryBranch"
              self.leafs[leaf.getIndex()]=SecondaryBranch(leaf)
          elif type(self.leafs[siblings[siblingIndex-1]])==SecondaryBranch: # is the child to the left a SecondaryBranch?
            if self.leafs[siblings[siblingIndex-1]].isElse==True: # is the child to the left an 'else'?
              self.leafs[leaf.getIndex()]=PrimaryBranch(leaf)
            else: # the child is not an 'else'
              choice=random.choice(["PrimaryBranch","SecondaryBranch"])
              if choice=="PrimaryBranch":
                self.leafs[leaf.getIndex()]=PrimaryBranch(leaf)
              else: # choice=="SecondaryBranch"
                choice=random.choice(["else-if","else"])
                if choice=="else-if":
                  self.leafs[leaf.getIndex()]=SecondaryBranch(leaf)
                else: # choice=="else"
                  self.leafs[leaf.getIndex()]=SecondaryBranch(leaf)
                  self.leafs[leaf.getIndex()].setElse()
          else: # the child to the left is not a SecondaryBranch
            self.leafs[leaf.getIndex()]=PrimaryBranch(leaf)
        else: #there isn't a child to the left
          self.leafs[leaf.getIndex()]=PrimaryBranch(leaf)

    # determine lastChild status
    for parentLeaf in self.leafs:
       if len(parentLeaf.getChildren())==0: # parentLeaf has no children
         pass
       else:
         children=parentLeaf.getChildren()
         lastChild=children[-1]
         self.leafs[lastChild].setLastChild(True)

    # set Element variables
    for leaf in self.leafs:
      for i in range(random.randint(MIN_NUMBER_OF_VARIABLES_PER_LEAF,max_number_of_variables_per_leaf)):
        leaf.appendVariable(variable())
    
    # update the parentVariables of child Elements
    for leaf in self.leafs:
      if leaf.getParent()!=None: # not the root
        for var in self.leafs[leaf.getParent()].getVariables():
          leaf.appendParentVariable(var)
      else: # the parent variables of the root are the global variables 
        for var in self.variables:
          leaf.appendParentVariable(var)

    # roll the conditions
    for leaf in self.leafs:
      leaf.rollConditions()

    # roll the preambles and postambles
    for leaf in self.leafs:
      leaf.rollAmbles()

    # rolling preambles and postambles resets the 'else' preamble
    # so, need to re-setElse()
    for leaf in self.leafs:
      if type(leaf)==SecondaryBranch:
        if leaf.isElse==True:
          leaf.setElse()

    # update the postambles of Elements with lastChild==True
    lastChildren=[]
    for leaf in self.leafs:
      if len(leaf.children)!=0:
        lastChildren.append(leaf.children[-1])

    for child in lastChildren:
      for postamble in self.leafs[self.leafs[child].getParent()].getPostamble():
        self.leafs[child].appendPostamble(postamble)

    # update the nonbranching elements of the leafs
    for leaf in self.leafs:
      for i in range(random.randint(MIN_NUMBER_OF_ELEMENTS_PER_LEAF,max_number_of_elements_per_leaf)):
        isFxn=False
        for element in nonBranchingElement(self.variables, potentialFxns, isFxn):
          leaf.appendElement(element)

    # change the preambles of the chosen path elements
    for leafIndex in chosenPathIndices:
      # TODO update the preambles of the chosen path elements to force user influence
      #def giveMeaningfulUserOrientedCondition(self, elementToAlter):
      #chosenPreamble=self.leafs[leafIndex].getPreamble()
      chosenPreamble=self.giveMeaningfulUserOrientedCondition(self.leafs[leafIndex])
      chosenPreamble[2] = chosenPreamble[2] + " //" # this is necessary for printing the tree later
      self.leafs[leafIndex].setPreamble(chosenPreamble)
      if leafIndex==chosenPathIndices[-1]:
        # place bug in BugTree
        bugVars=self.leafs[leafIndex].getParentVariables()
        leafElements=self.leafs[leafIndex].getElements()
        bugElements=self.bug(bugVars)
        #for element in reversed(bugElements):
        leafElements.insert(0, bugElements)
        self.leafs[leafIndex].setElements(leafElements)
    
    # fix the indents
    for i, layer in enumerate(pretree):
      for leafIndex in layer:
        self.leafs[leafIndex].setIndent(i)

    self.pretree=pretree
    self.chosenPathIndices=chosenPathIndices

  # replace the preamble so that I can 
  # 0) choose or create a variable
  # 1) slap a scanf for that variable before the condition
  # 2) create a meaningful condition with that variable
  # so, for example:
  # int var1;
  # scanf();
  # if (var1 >= 9000){

  def giveMeaningfulUserOrientedCondition(self, elementToAlter):
    alteredPreamble=[]
    # we are assuming that the element has some variables
    userVar=random.choice(elementToAlter.getParentVariables())
    # determine appropriate type specifier
    # types=["char","double","float", "int", "long", "short"]
    if userVar[1]=="char":
      typeSpecifier="c"
    if userVar[1]=="double":
      typeSpecifier="lf"
    if userVar[1]=="float":
      typeSpecifier="f"
    if userVar[1]=="int":
      typeSpecifier="d"
    if userVar[1]=="long":
      typeSpecifier="ld"
    if userVar[1]=="short":
      typeSpecifier="hu"

    # create a condition of type: useVar comparisonOperator appropriateValue
    comparisonOperators=[">", ">=", "==", "<=", "<"]
    comparisonOperator=random.choice(comparisonOperators)
    
    appropriateValue=getAppropriateValue(userVar[1])

    # put it all together
    # determine the type of the elementToAlter
    if type(elementToAlter)==PrimaryBranch:
      # check to see if userVar is a buffer
      if len(userVar)>2: # userVar is a buffer
        randomElement=str(random.randint(0,userVar[2]-1))
        alteredPreamble.append("scanf(\"%"+typeSpecifier+"\", &"+userVar[0]+"["+randomElement+"]);")
        alteredPreamble.append("dumpStdin();")
        conditionString="if ("+userVar[0]+"["+randomElement+"]"+comparisonOperator+appropriateValue+"){"
      else:
        alteredPreamble.append("scanf(\"%"+typeSpecifier+"\", &"+userVar[0]+");")
        alteredPreamble.append("dumpStdin();")
        conditionString="if ("+userVar[0]+comparisonOperator+appropriateValue+"){"
      alteredPreamble.append(conditionString)
    elif type(elementToAlter)==SecondaryBranch: # can't have an else
      # check to see if userVar is a buffer
      if len(userVar)>2: # userVar is a buffer
        randomElement=str(random.randint(0,userVar[2]-1))
        alteredPreamble.append("scanf(\"%"+typeSpecifier+"\", &"+userVar[0]+"["+randomElement+"]);")
        alteredPreamble.append("dumpStdin();")
        conditionString="else if ("+userVar[0]+"["+randomElement+"]"+comparisonOperator+appropriateValue+"){"
      else:
        alteredPreamble.append("scanf(\"%"+typeSpecifier+"\", &"+userVar[0]+");")
        alteredPreamble.append("dumpStdin();")
        conditionString="else if ("+userVar[0]+comparisonOperator+appropriateValue+"){"
      alteredPreamble.append(conditionString)

    return alteredPreamble

  def getCurrentLeafIndex(self):
    return self.currentLeafIndex

  def pushChildren(self):
    children=self.getCurrentLeaf().getChildren()
    if (len(children)==0):
      return None
    else:
      for child in reversed(children):
        self.leafStack.append(child)
      return len(children)

  def pushLeaf(self, leafIndexToPush):
    self.leafStack.append(leafIndexToPush)

  def popLeaf(self):
    newCurrentLeafIndex=self.leafStack.pop()
    self.currentLeafIndex=newCurrentLeafIndex
    return newCurrentLeafIndex

  def getCurrentLeaf(self):
    currentLeaf=self.leafs[self.currentLeafIndex]
    return currentLeaf

  def getCurrentLeafPreamble(self):
   currentLeaf=self.getCurrentLeaf()
   return currentLeaf.getPreamble()

  def getCurrentLeafConditions(self):
    currentLeaf=self.getCurrentLeaf()
    return currentLeaf.getConditions()
  
  def getCurrentLeafElements(self):
    currentLeaf=self.getCurrentLeaf()
    return currentLeaf.getElements()

  def getCurrentLeafPostamble(self):
    currentLeaf=self.getCurrentLeaf()
    return currentLeaf.getPostamble()

  def getCurrentLeafParent(self):
    currentLeaf=self.leafs[self.currentLeafIndex]
    return currentLeaf.getParent()

  def getCurrentLeafAncestors(self):
    currentLeaf=self.leafs[self.currentLeafIndex]
    return currentLeaf.getAncestors()
  
  def getCurrentLeafVariables(self):
    currentLeaf=self.getCurrentLeaf()
    return currentLeaf.getVariables()
  
  def getCurrentLeafIndent(self):
    currentLeaf=self.getCurrentLeaf()
    return currentLeaf.getIndent()

  def getVariables(self):
    return self.variables

  def setVariables(self, newVariables):
    self.variables=newVariables

  def appendVariable(self, newVariable):
    self.variables.append(newVariable)

  def getElements(self):
    return self.Elements

  def setElements(self, newElements):
    self.elements=newElements

  def appendElement(self, newElement):
    self.elements.append(newElement)

  def getTreeLines(self):
    treeLineList=[]
    # for diagnostics 
    if TROUBLESHOOTING:
      print(self.pretree)
      for leaf in self.leafs:
        print(str(leaf))

    # traverse the tree and print the associated lexical elements
    self.pushLeaf(0)
    while(len(self.leafStack)>0):
      self.popLeaf()
      indent="  "*self.getCurrentLeafIndent()
      # the current leaf is the popped leaf
      for preamble in self.getCurrentLeafPreamble():
        treeLineList.append(indent+"    "+preamble)
      for var in self.getCurrentLeafVariables():
        # don't re-declare variables
        if (var not in self.globalVariables) and (var not in self.variables) and (len(var)<4): # only declare variables that haven't been declared yet
          treeLineList.append(indent+"      "+declareVariableText(1,var))
      for element in self.getCurrentLeafElements():
        for line in element:
          treeLineList.append(indent+"      "+line)
      if (self.pushChildren()==None): # pushChildren pushes all of the children indices onto leafstack, unless there are none, in which case it returns None
        for i, postamble in enumerate(self.getCurrentLeafPostamble()):
          treeLineList.append(indent[2*i:]+"    "+postamble)
    # print the tree's postamble
    for line in self.postamble:
      treeLineList.append(line)

    # tailored fuzzing info
    treeLineList.append("// layers:")
    treeLineList.append("// " + str(self.pretree))
    treeLineList.append("// children:")
    for leaf in self.leafs:
      parentString="// " + str(leaf.getIndex())+": "
      for child in leaf.getChildren():
        parentString=parentString+str(child)+", "
      parentString=parentString[:-2]
      if leaf.getChildren():
        treeLineList.append(parentString)
    treeLineList.append("// bug path:")
    treeLineList.append("// "+ str(self.chosenPathIndices))
    treeLineList.append("// types:")
    for layer in self.pretree:
      for leaf in layer:
        typeString = "// " + str(leaf) + ": "
        typeString=typeString+self.leafs[leaf].getPreamble()[-1]
        treeLineList.append(typeString)

    return treeLineList

  def __str__(self):
    treeString=""
    # for diagnostics 
    if TROUBLESHOOTING:
      print(self.pretree)
      for leaf in self.leafs:
        print(str(leaf))

    # print the tree's preamble
    for line in self.preamble:
      treeString=treeString+line+'\n'
      self.lineNumber+=1
    # print the tree's variables (but not the global variables)
    for var in self.variables:
      if var not in self.globalVariables:
        treeString=treeString+"    "+declareVariableText(1,var)+'\n' # 1 means to initialize the variable
        self.lineNumber+=1
    # print the tree's elements
#    for element in self.elements:
#      for line in element:
#        treeString=treeString+"    "+line+'\n'
#        self.lineNumber+=1
    # traverse the tree and print the associated lexical elements
    self.pushLeaf(0)
    while(len(self.leafStack)>0):
      self.popLeaf()
      indent="  "*self.getCurrentLeafIndent()
      # the current leaf is the popped leaf
      for preamble in self.getCurrentLeafPreamble():
        treeString=treeString+indent+"    "+preamble+'\n'#+" //lineNumber: "+str(self.lineNumber)+'\n'
        self.lineNumber+=1
      for var in self.getCurrentLeafVariables():
        # don't re-declare variables
        if (var not in self.globalVariables) and (var not in self.variables) and (not(len(var)>3)): # only declare variables that haven't been declared yet
          treeString=treeString+indent+"      "+declareVariableText(1,var)+'\n'#+" //lineNumber: "+str(self.lineNumber)+'\n'
          self.lineNumber+=1
      for element in self.getCurrentLeafElements():
        for line in element:
          treeString=treeString+indent+"      "+line+'\n'#+" //lineNumber: "+str(self.lineNumber)+'\n'
          self.lineNumber+=1
      if (self.pushChildren()==None): # pushChildren pushes all of the children indices onto leafstack, unless there are none, in which case it returns None
        for i, postamble in enumerate(self.getCurrentLeafPostamble()):
          treeString=treeString+indent[2*i:]+"    "+postamble+'\n'#+" //lineNumber: "+str(self.lineNumber)+'\n'
          self.lineNumber+=1
    # print the tree's postamble
    for line in self.postamble:
      treeString=treeString+line+'\n'
      self.lineNumber+=1
    treeString=treeString[:-1] # get rid of last newline character

    return treeString
  
  '''
  bug()
  '''
  def bug(self, bufVars):
    #TODO: more and more interesting bugs
    availableBuffers=[]
    bugElements=[]
    for var in bufVars:
      if len(var)==3:
        availableBuffers.append(var)
    if len(availableBuffers)==0:
      newBuffVar=variable(isBuff=1)
      availableBuffers.append(newBuffVar)
      bugElements.append(declareVariableText(0,newBuffVar))
    bufVar=random.choice(availableBuffers)
    bufName=bufVar[0]
    bugElements.append("gets("+bufName+"); //")
    return bugElements

  #def __str__(self):
  #  treeString=""
  #  for i, leaf in enumerate(self.leafs):
  #    treeString=treeString+str(i)+": "+str(leaf)+"\n"
  #  treeString=treeString[:-1]
  #  return treeString
