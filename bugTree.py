import random
from copy import deepcopy
from buggyHeader import *
#from buggyClasses import *
from defaultvalues import *
TROUBLESHOOTING=False
'''
bugTree.py
functions concerning the BugTree class
'''
#TODO: the index for this root in the calling fxn will be something like len(leafs)
class BugTree:
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
    self.lineNumber=int(lineNumber)
    self.interestingness=int(interestingness)

      
    # create the pretree structure
    if TROUBLESHOOTING:
      self.pretree=[[0]]
      pretree=self.pretree
    else:
      pretree=[[0]] # a list of lists, where each sub-list represents a layer
    i=1 # keep track of the next element's index to place in the tree
    layers=interestingness -1# the total number of layers should include the root. also, the bug is in the last layer
    for layer in range(layers):
      numLeafs=random.randint(min_number_of_leafs_per_layer, max_number_of_leafs_per_layer)
      # create a list of indices
      thisLayer=[]
      for leaf in range(numLeafs):
        thisLayer.append(i)
        i=i+1
      pretree.append(thisLayer)
     
    #TODO: deleteme
    print(pretree)

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
    #TODO: change root's parent to 0 later
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
    for layer in pretree:
      chosenPathLeafIndex=random.choice(layer)
      chosenPathIndices.append(chosenPathLeafIndex)

    #TODO: deleteme
    print("chosen path: " + str(chosenPathIndices))
    
    for i, leaf in enumerate(self.leafs):
    # the root leaf is a PrimaryBranch element
      if i==0:
        self.leafs[i]=PrimaryBranch(leaf)
    # the rest of the leafs in the chosen path are either PrimaryBranch or SecondaryBranch element
      elif leaf.getIndex() in chosenPathIndices:
        choice=random.choice(["primary","secondary"])
        if choice=="primary":
          self.leafs[i]=PrimaryBranch(leaf)
        else:
          self.leafs[i]=SecondaryBranch(leaf)

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

    # fix indents for leafs
    #TODO: need to figure out indent situation
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
        for element in nonBranchingElement(self.variables, potentialFxns):
          leaf.appendElement(element)

    # TODO update all of the elements indices
#    for i, layer in enumerate(pretree):
#      for j, index in enumerate(layer):
#        print(index+rootIndex)
#        pretree[i][j]=index+rootIndex
#    print(pretree)
    
    # TODO: update the parent indices
    for leaf in self.leafs:
      print(leaf.getIndex()+rootIndex)
      if leaf.getParent()==None:
        leaf.setIndex(rootIndex)
        leaf.setParent(0)
        for i, child in enumerate(leaf.getChildren()):
          leaf.children[i]=leaf.children[i]+rootIndex
      else:
        leaf.setIndex(leaf.getIndex()+rootIndex)
        leaf.setParent(leaf.getParent()+rootIndex)
        for i, child in enumerate(leaf.getChildren()):
          leaf.children[i]=leaf.children[i]+rootIndex

    for leaf in self.leafs:
      print(leaf)

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
        if (var not in self.globalVariables) and (var not in self.variables) and (not(len(var)>2)): # only declare variables that haven't been declared yet
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
        if (var not in self.globalVariables) and (var not in self.variables) and (not(len(var)>2)): # only declare variables that haven't been declared yet
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

  #def __str__(self):
  #  treeString=""
  #  for i, leaf in enumerate(self.leafs):
  #    treeString=treeString+str(i)+": "+str(leaf)+"\n"
  #  treeString=treeString[:-1]
  #  return treeString
