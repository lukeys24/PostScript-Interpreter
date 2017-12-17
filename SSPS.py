# Luke Seo 11434217
# Nov 9, 2017
# CPTS 355
# HW 5.2 Interpreter

import re

# Change to static or dynamic to get respective results
scope = 'static'

# The operand stack: define the operand stack and its operations
opStack = []

# Pop for operand stack
def opPop():
    if (len(opStack) > 0) :
        x = opStack.pop()
        return x
    else :
        print("Empty operand stack!")

# Push for operand stack
def opPush(value):
    opStack.append(value)

# The dictionary stack: define the dictionary stack and its operations
dictStack = []

# Dictionary stack pop
def dictPop():
    if (len(dictStack) > 0) :
        x = dictStack.pop()
        return x
    else :
        print("Empty dictionary stack!")

# Dictionary stack push
def dictPush(index, d):
    # append the tuple to dict stack
    dictStack.append((index, d))

# Defines variable in top dictionary stack
def define(name, value):
    if (not (len(dictStack) > 0)):
        dictStack.append((0,{}))

    dictStack[len(dictStack) - 1][1][name] = value

def psDef() :
    if (len(opStack) > 1):
        value = opPop()
        name = opPop()
        if (isinstance(name, str)):
            define(name, value)
        else :
            print("Error: psDef - invalid name argument")
    else :
        print("Error: psDef - not enough arguments")

def lookup(name):
    # Check if our scope is static
    if scope == 'static':
        # Start at top of stack then go to links
        index = -1
        while True :
            (goToLink, dictCheck) = dictStack[index]
            # Found name in the current dictionary so return value
            if '/' + name in dictCheck.keys() :
                return dictCheck.get('/' + name, 0)
            else :
                # Change next index to link we have to go to
                index = goToLink
    else:
        # Case where we're implementing dynamic scoping
        for ((index, d)) in reversed(dictStack):
            if d.get('/' + name, None) != None:
                return d.get('/' + name, 0)

    return None

# Arithmetic and comparison operators: define all the arithmetic and comparison operators here --
# add, sub, mul, div, eq, lt, gt

def add():
    if (len(opStack) > 1) :
        op1 = opPop()
        op2 = opPop()
        if ((isinstance(op1, int) or isinstance(op1,float))
            and (isinstance(op2, int) or isinstance(op2,float))):
            opPush(op1+op2)
        else:
            print("Invalid types for add")
    else :
        print("Error, not enough arguments for add")

def sub():
    if (len(opStack) > 1) :
        op1 = opPop()
        op2 = opPop()
        if ((isinstance(op1, int) or isinstance(op1,float))
            and (isinstance(op2, int) or isinstance(op2,float))):
            opPush(op2-op1)
        else:
            print("Invalid types for sub")
    else :
        print("Error, not enough arguments for sub")

def mul():
    if (len(opStack) > 1) :
        op1 = opPop()
        op2 = opPop()
        if ((isinstance(op1, int) or isinstance(op1,float))
            and (isinstance(op2, int) or isinstance(op2,float))):
            opPush(op1*op2)
        else:
            print("Invalid types for mul")
            opPush(op2)
            opPush.push(op1)
    else :
        print("Error, not enough arguments for mul")

def div():
    if (len(opStack) > 1) :
        op1 = opPop()
        op2 = opPop()
        if ((isinstance(op1, int) or isinstance(op1,float))
            and (isinstance(op2, int) or isinstance(op2,float))):
            opPush(op2/op1)
        else:
            print("Invalid types for div")
    else :
        print("Error, not enough arguments for div")

def eq():
    if (len(opStack) > 1) :
        op1 = opPop()
        op2 = opPop()
        if ((isinstance(op1, int) or isinstance(op1,float) or isinstance(op1, str))
            and (isinstance(op2, int) or isinstance(op2,float) or isinstance(op2, str))):
            if (op1 == op2) :
                opPush(True)
            else :
                opPush(False)
        else:
            print("Invalid types for eq")
    else :
        print("Error, not enough arguments for eq")

def lt():
    if (len(opStack) > 1) :
        op1 = opPop()
        op2 = opPop()
        if ((isinstance(op1, int) or isinstance(op1,float))
            and (isinstance(op2, int) or isinstance(op2,float))):
            if (op2 < op1) :
                opPush(True)
            else :
                opPush(False)
        else:
            print("Invalid types for lt")
    else :
        print("Error, not enough arguments for lt")

def gt():
    if (len(opStack) > 1) :
        op1 = opPop()
        op2 = opPop()
        if ((isinstance(op1, int) or isinstance(op1,float))
            and (isinstance(op2, int) or isinstance(op2,float))):
            if (op2 > op1) :
                opPush(True)
            else :
                opPush(False)
        else:
            print("Invalid types for gt")
    else :
        print("Error, not enough arguments for gt")

# String operators: define the string operators length, get, getinterval
def length():
    if (len(opStack) > 0):
        op1 = opPop()
        if ((isinstance(op1, str))):
            opPush(len(op1) - 2)
        else :
            print("Expecting a string for length")
    else :
        print("Not enough arguments in stack for length")

def get():
    if (len(opStack) > 1):
        opIndex = opPop()
        opString = opPop()
        if ((isinstance(opString, str)) and (isinstance(opIndex, int))):
            if (opIndex >= 0 and opIndex < len(opString)):
                charString = opString[opIndex + 1]
                opPush(ord(charString))
        else :
            print("Expecting a string for length")
    else :
        print("Not enough arguments in stack for get")

def getinterval():
    if (len(opStack) > 2):
        opCount = opPop()
        opIndex = opPop()
        opString = opPop()
        if ((isinstance(opString, str)) and (isinstance(opIndex,int)) and (isinstance(opCount, int))):
            if (opIndex >= 0 and opIndex < len(opString) and opCount >= 0 and opCount <= len(opString)):
                subStr = opString[opIndex + 1:opCount + opIndex + 1]
                opPush('(' + subStr + ')')
        else:
            print("Invalid types for getinterval")
    else:
        print("Not enough arguments in stack for getinterval")

# Boolean operators: define the boolean operators and, or, not;
def psAnd():
    if (len(opStack) > 1):
        op1 = opPop()
        op2 = opPop()
        if ((isinstance(op1, bool)) and (isinstance(op2,bool))) :
            opPush(op1 and op2)
        else :
            print("Invalid types for and")
    else:
        print("Not enough arguments in stack for and")

def psOr():
    if (len(opStack) > 1):
        op1 = opPop()
        op2 = opPop()
        if ((isinstance(op1, bool)) and (isinstance(op2, bool))):
            opPush(op1 or op2)
        else:
            print("Invalid types for or")
    else:
        print("Not enough arguments in stack for or")


def psNot():
    if (len(opStack) > 0):
        op1 = opPop()
        if ((isinstance(op1, bool))):
            opPush(not op1)
        else:
            print("Invalid types for not")
    else:
        print("Not enough arguments in stack for not")

# Define the stack manipulation and print operators: dup, exch, pop, roll, copy, clear, stack

# Duplicates top value on stack
def dup():
    if len(opStack) > 0:
        op1 = opPop()
        opPush(op1)
        opPush(op1)
    else:
        print("Not enough arguments for dup")

# swaps the top two elements in opStack
def exch():
    if len(opStack) > 1:
        op1 = opPop()
        op2 = opPop()
        opPush(op1)
        opPush(op2)
    else:
        print("Not enough arguments for exch")

# pops the top value from the operand stack
def pop():
    if (len(opStack) > 0):
        opPop()
    else:
        print("Not enough arguments for pop")

# Pops 2 integer values m and n from stack, rolls the top m values n times
def roll():
    if len(opStack) > 1:
        n = opPop()
        m = opPop()
        copyList = []
        for x in range(0, m):
            copyList.append(opPop())
        if (n > 0):
            copyList[len(copyList):] = copyList[0:n]
            copyList[0:n] = []
        else:
            copyList[:0] = copyList[n:]
            copyList[n:] = []

        for x in reversed(copyList[0:]):
            opPush(x)
        del copyList[:]

    else:
        print("Not enough arguments for roll")

# Copies certain number of values onto stack
def copy():
    if (len(opStack) > 0):
        opCount = opPop()
        copy = []
        for x in range(0, opCount):
            copy.append(opPop())
        for item in reversed(copy):
            opPush(item)
        for item in reversed(copy):
            opPush(item)
    else:
        print("Not enough arguments for copy")

# Clears operand stack
def clear():
    del opStack[:]
    del dictStack[:]

# Prints operand stack
def stack():
    testList = []
    if scope == 'static':
        print("Static")
    else :
        print("Dynamic")
    print("=============")
    for a in reversed(opStack) :
        testList.append(a)
        print(a)

    curIndex = len(dictStack) - 1
    for (index, dict) in reversed(dictStack) :
        print("----", curIndex ,"----", index ,"----")
        for (var, val) in dict.items():
            print(var, " ", val, " ", sep="")
        curIndex = curIndex - 1
    print("==============")

    return testList


# Define the dictionary manipulation operators: psDict, begin, end, psDef
def psDict():
    if (len(opStack) > 0) :
        opPop()
        opPush({})
    else :
        print("Not enough arguments for psDict")

def begin():
    if (len(opStack) > 0):
        newDict = opPop()
        if (isinstance(newDict, dict)):
            dictPush(0, {})
        else :
            print("Wrong type for begin")
    else:
        print("Not enough arguments for begin")

def end():
    if (len(dictStack) > 0):
        dictPop()
    else :
        print("Not enough arugments for end")

# Defining if and ifelse
def psIf():
    codeBlock = opPop()
    boolVal = opPop()
    if isinstance(boolVal, bool):
        if boolVal:
            interpretSPS(codeBlock, scope)
    else:
        print("Value popped is not a bool for ifelse")

def psIfElse():
    elseCodeBlock = opPop()
    ifCodeBlock = opPop()
    boolVal = opPop()
    if isinstance(boolVal, bool):
        if boolVal:
            interpretSPS(ifCodeBlock, scope)
        else:
            interpretSPS(elseCodeBlock, scope)
    else:
        print("Value popped is not a bool for ifelse")

# Parsing
def tokenize(s):
    return re.findall("/?[a-zA-Z()][a-zA-Z0-9_()]*|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

# Parses a PostScript list
def parse(s):
    result = []
    it = iter(s)
    for c in it:
        # Case where not properly nested
        if c == '}':
            return False
        # Case where we need to create code array
        elif c == '{':
            result.append(groupMatching(it))
        else:
            if isInt(c):
                result.append(int(c))
            # Check if bool
            elif c in ['True', 'true', 'False', 'false']:
                if c in ['True', 'true']:
                    result.append(True)
                else:
                    result.append(False)
            else:
                result.append(c)
    return result

# Used to parse code blocks, recursive if there's a code block within a code block
def groupMatching(it):
    result = []
    for c in it:
        if c == '}':
            return result
        elif c == '{':
            result.append(groupMatching(it))
        else:
            if isInt(c):
                result.append(int(c))
            elif c in ['True', 'true', 'False', 'false']:
                if c in ['True', 'true']:
                    result.append(True)
                else:
                    result.append(False)
            elif c != ' ':
                result.append(c)
    return result

# Returns bool whether the string represents an integer
def isInt(c):
    try:
        int(c)
        return True
    except ValueError:
        return False

# Finds link for the passed in token
def findStaticLink(token):
    # Check top of the list then go bottom up
    index = -1
    (ind, dictCheck) = dictStack[index]

    # Link is at the top of the stack (end of list)
    if token in dictCheck.values() :
        return len(dictStack) - 1
    else :
        # Go to link from tuple at top of stack
        index = ind
        while True:
            # Get new tuple from current link
            (ind, dictCheck) = dictStack[index]

            # Check if token is in new dictionary we're checking
            if token in dictCheck.values() :
                return dictStack.index((ind,dictCheck))
            else :
                index = ind

# Interprets PostScript code array
def interpretSPS(code, scope):
    for token in code:
        # Basic case we just push value
        if isinstance(token, int) or isinstance(token, bool):
            opPush(token)
        # Strings can be variable to define, PS string, built in PS function,
        #   code array, or varaible to look up
        elif isinstance(token, str):
            if token[0] == '/' or token[0] == '(':
                opPush(token)
            # Token is a PostScript built in function
            elif token in ['def', 'lookup', 'add', 'sub', 'mul', 'div', 'eq', 'lt', 'gt', 'length', 'get',
                           'getinterval', 'and', 'or', 'not', 'dup','exch', 'pop', 'roll', 'copy', 'clear',
                           'stack', 'dict', 'begin', 'end', 'if', 'ifelse']:
                if token == 'def':
                    psDef()
                elif token == 'lookup':
                    lookup()
                elif token == 'add':
                    add()
                elif token == 'sub':
                    sub()
                elif token == 'mul':
                    mul()
                elif token == 'div':
                    div()
                elif token == 'eq':
                    eq()
                elif token == 'lt':
                    lt()
                elif token == 'gt':
                    gt()
                elif token == 'length':
                    length()
                elif token == 'get':
                    get()
                elif token == 'getinterval':
                    getinterval()
                elif token == 'and':
                    psAnd()
                elif token == 'or':
                    psOr()
                elif token == 'not':
                    psNot()
                elif token == 'dup':
                    dup()
                elif token == 'exch':
                    exch()
                elif token == 'pop':
                    pop()
                elif token == 'roll':
                    roll()
                elif token == 'copy':
                    copy()
                elif token == 'clear':
                    clear()
                elif token == 'stack':
                    stack()
                elif token == 'dict':
                    psDict()
                elif token == 'begin':
                    begin()
                elif token == 'end':
                    end()
                elif token == 'if':
                    psIf()
                elif token == 'ifelse':
                    psIfElse()
            else:
                # Variable we have to look up
                val = lookup(token)

                # Case where it's a code array, so evaluate
                if isinstance(val, list):
                    link = 0
                    if scope == 'static':
                        link = findStaticLink(val)

                    dictPush(link, {})
                    interpretSPS(val, scope)
                    dictPop()

                # Case where it's a value we push (string, bool, int)
                elif isinstance(val, str) or isinstance(val, bool) or isInt(val):
                    opPush(val)

                # Invalid value
                else:
                    raise ValueError('Value not valid in PostScript')
        # Code array that we will later define with def
        elif isinstance(token, list):
            opPush(token)
        else:
            raise ValueError('Value not valid in PostScript')


# Interprets string by tokenizing, parsing and then interpreting PostScript code array
def interpreter(s, scope):
    interpretSPS(parse(tokenize(s)), scope)


# Test functions
def testAdd():
    clear()
    opPush(1)
    opPush(2)
    add()
    if opPop() != 3 :
        return False
    else :
        return True

def testSub():
    clear()
    opPush(3)
    opPush(1)
    sub()
    if opPop() != 2 :
        return False
    else :
        return True

def testMul():
    clear()
    opPush(10)
    opPush(5)
    mul()
    if opPop() != 50 :
        return False
    else :
        return True

def testDiv():
    clear()
    opPush(50)
    opPush(5)
    div()
    if opPop() != 10 :
        return False
    else :
        return True

def testEq():
    clear()
    opPush(10)
    opPush(10)
    eq()
    if opPop() != True :
        return False
    else :
        return True

def testLt():
    clear()
    opPush(10)
    opPush(50)
    lt()
    if opPop() != True :
        return False
    else :
        return True

def testGt():
    clear()
    opPush(50)
    opPush(10)
    gt()
    if opPop() != True:
        return False
    else:
        return True

def testLength():
    clear()
    opPush("(one)")
    length()
    if opPop() != 3 :
        return False
    else :
        return True

def testGet():
    clear()
    opPush("(CptS355)")
    opPush(0)
    get()
    if opPop() != 67 :
        return False
    else :
        return True

def testGetInterval():
    clear()
    opPush("(CptS355)")
    opPush(0)
    opPush(3)
    getinterval()
    if opPop() != "(Cpt)" :
        return False
    else :
        return True

def testpsAnd():
    clear()
    opPush(True)
    opPush(True)
    psAnd()
    if opPop() != True :
        return False
    else :
        return True

def testpsOr():
    clear()
    opPush(True)
    opPush(False)
    psOr()
    if opPop() != True :
        return False
    else :
        return True

def testpsNot():
    clear()
    opPush(True)
    psNot()
    if opPop() != False :
        return False
    else :
        return True

def testDup():
    clear()
    opPush(4)
    dup()
    if opPop() != 4 :
        return False
    else :
        return True

def testExch():
    clear()
    opPush(5)
    opPush(4)
    exch()
    if opPop() != 5:
        return False
    else :
        return True

def testPop():
    clear()
    opPush(10)
    pop()
    if len(opStack) != 0 :
        return False
    else :
        return True

def testRoll():
    clear()
    opPush(1)
    opPush(2)
    opPush(3)
    opPush(4)
    opPush(5)

    opPush(4)
    opPush(2)
    roll()
    if opPop() != 3 or opPop() != 2 or opPop() != 5 or opPop() != 4 or opPop() != 1 :
        return False
    else :
        return True

def testCopy():
    clear()
    opPush(50)
    opPush(40)
    opPush(30)
    opPush(3)
    copy()
    if len(opStack) != 6 or opPop() != 30 or opPop() != 40 or opPop() != 50:
        return False
    else:
        return True

def testClear():
    opPush(50)
    opPush(60)
    clear()
    if len(opStack) == 0 :
        return True
    else :
        return False

def testStack():
    opPush(10)
    opPush(30)
    testList = stack()
    if testList[1] == 10 and testList[0] == 30 :
        return True
    else :
        return False

def testpsDict():
    clear()
    opPush(5)
    psDict()
    if opPop() != {} :
        return False
    else :
        return True

def testBegin():
    opPush({})
    begin()
    if dictPop() != {} :
        return False
    else :
        return True

def testEnd():
    dictPush(0, {})
    end()
    if len(dictStack) == 0:
        return True
    else :
        return False

def testpsDef():
    opPush('/x')
    opPush(500)
    psDef()
    x = dictStack[len(dictStack) - 1][1]['/x']
    if x != 500 :
        return False
    else :
        return True

def testLookup():
    opPush('/y')
    opPush(500)
    psDef()
    y = lookup('y')
    if y != 500 :
        return False
    else :
        return True

def testParse():
    input1 = "/square { dup mul } def (square) 4 square dup 16 eq true and {(pass)} {(fail)} ifelse stack"
    testList = parse(tokenize(input1))
    if testList != ['/square', ['dup', 'mul'], 'def', '(square)', 4, 'square', 'dup', 16, 'eq', True,
                    'and', ['(pass)'], ['(fail)'], 'ifelse', 'stack']:
        return False
    else:
        return True

def testInterpreter():
    # Test input 1
    print("")
    print("Input 1 intrepreter")
    input1 = "/square { dup mul } def (square) 4 square dup 16 eq true and {(pass)} {(fail)} ifelse stack"
    interpreter(input1, scope)
    clear()
    dictStack[:]
    print("")

    # Test input 2
    print("Input 2 intrepreter")
    input2 = "(facto) dup length /n exch def /fact { 0 dict begin /n exch def n 2 lt { 1} {" \
             "n 1 sub fact n mul } ifelse end } def n fact stack"
    interpreter(input2, scope)
    clear()
    dictStack[:]
    print("")

    # Test input 3
    input3 = """
    /lt6 { 6 lt } def
    1 2 3 4 5 6 4 -3 roll
    dup dup lt6 exch 3 gt and {mul mul} if
    stack
    clear
    """
    print("Input 3 intrepreter")
    interpreter(input3, scope)
    clear()
    dictStack[:]
    print("")

    # Test input 4
    input4 = """
    (CptS355_HW5) 4 3 getinterval
    (355) eq
    {(You_are_in_CptS355)} if
    stack
    """
    print("Input 4 intrepreter")
    interpreter(input4, scope)
    clear()
    dictStack[:]
    print("")

def testSSPS():
    input = "/m 50 def " \
            "/n 100 def " \
            "/egg1 {/m 25 def n} def " \
            "/chic " \
                "{ /n 1 def " \
                "/egg2 { n } def " \
                "m " \
                "n " \
                "egg1 " \
                "egg2 " \
                "stack } def " \
            "n " \
            "chic"

    input2 = "/x 10 def " \
             "/A { x } def " \
             "/C { /x 40 def A stack } def " \
             "/B { /x 30 def /A { x } def C } def " \
             "B"

    input3 = "/x 4 def " \
             "/g { x stack } def " \
             "/f { /x 7 def g } def " \
             "f"
    interpreter(input, scope)
    clear()
    dictStack = []
    print()

    interpreter(input2, scope)
    clear()
    dictStack = []
    print()

    interpreter(input3, scope)
    clear()
    dictStack = []

if __name__ == '__main__':
    """
    testCases = [('add', testAdd), ('sub',testSub), ('mul', testMul), ('div', testDiv),
                 ('eq', testEq), ('lt', testLt), ('gt', testGt), ('length', testLength) ,
                 ('get', testGet), ('getinterval', testGetInterval), ('psAnd', testpsAnd) ,
                 ('psOr', testpsOr), ('psNot', testpsNot), ('dup', testDup), ('exch', testExch) ,
                 ('pop', testPop), ('roll', testRoll), ('copy', testCopy), ('clear', testClear) ,
                 ('stack', testStack), ('psDict', testpsDict), ('begin', testBegin), ('end', testEnd),
                 ('psDef', testpsDef), ('lookup', testLookup), ('parse', testParse)]

    
    failedTests = [testName for (testName, testProc) in testCases if not testProc()]
    if failedTests:
        for test in failedTests:
            print(test + " failed")
    else :
        print("All tests passed")
    """

    #testInterpreter()
    testSSPS()