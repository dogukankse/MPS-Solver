# import sys
import re
import json
import sys
import pprint
import time

# file_name = sys.argv[1]

# with open(file_name) as file:
#   mps = file.read()
M = 99#float('INF')
mps = open("ornek.mps", "r").read()
mpsLines = mps.splitlines(0)
object = True
if 'MIN' in mpsLines[2]:
    object = False

s_count = 0
r_count = 0
foo_const = {}
foo = {}
vars = list()
vars_conts = {}
row_keys = []
foo_value_key = None

def appendVar(var):
    global vars
    if var in vars:
        return
    vars.append(var)

def removeEmpty(s):
    for i in range(1,16):
        s = s.strip().replace(" "*i," ").replace("\t","")
    a = s.replace(u"\u0014", "").replace(",",".").split(' ')
    b =[]
    for i in a:
        if not(i == ""):
            b.append(i)
    return b



def parse():
    global foo_value_key
    for row in mps[mps.find("ROWS")+5:mps.find("COLUMNS")].splitlines(0):
        row = removeEmpty(row)
        foo[row[1]] = {}
        foo_const[row[1]] = row[0]


    for row in mps[mps.find("COLUMNS")+8:mps.find("RHS")].splitlines(0):
        row = removeEmpty(row)
        appendVar(row[0])
        foo[row[1]][row[0]] = float(row[2])
        if len(row)>3:
            foo[row[3]][row[0]] = float(row[4])

    for row in mps[mps.find("RHS")+4:mps.find("BOUNDS")].splitlines(0):
        row = removeEmpty(row)
        appendVar(row[0])
        foo_value_key = row[0]
        foo[row[1]][row[0]] = float(row[2])
        if len(row)>3:
            foo[row[3]][row[0]] = float(row[4])

    for row in mps[mps.find("BOUNDS")+7:mps.find("ENDATA")].splitlines(0):
        row = removeEmpty(row)
        if len(row)>3:
            vars_conts[row[2]]= [row[0], float(row[3])]
        else:
            vars_conts[row[2]]= [row[0], None]



def getMainFoo(foo_const):
    for key,value in foo_const.items():
        if value == 'N':
            return key


def increaseVar(var,foo,key,i):
    global s_count
    global r_count
    if var == 'S':
        s_count= s_count+1
        var = var+str(s_count)
    if var == 'R':
        r_count= r_count+1
        var = var+str(r_count)

    if foo[key].get(var,None) == None:
        foo[key][var] = i
    else:
        foo[key][var] = foo[key]+i
    increaseMainFoo(key,foo[key][var],var,foo[key]["RHS1"])
    appendVar(var)
    row_keys.append(var)


def increaseMainFoo(key,k,var,rhs):
     if 'R' in var:
          foo[getMainFoo(foo_const)][var] = M
          if "RHS1" in foo[getMainFoo(foo_const)].keys():
              foo[getMainFoo(foo_const)]["RHS1"] =  foo[getMainFoo(foo_const)]["RHS1"] + rhs
          else:
              foo[getMainFoo(foo_const)]["RHS1"] = rhs


def normalize():
    for key,value in foo_const.items():
         if value ==   'L':
             increaseVar('S',foo,key,1)
         elif value == 'G':
             increaseVar('S',foo,key,-1)
             increaseVar('R',foo,key,1)
         elif value == 'E':
             increaseVar('R',foo,key,1)

def getColumn(y,table):
    a = []
    for i in range(len(table)):
        a.append(table[i][y])
    return a

def printTable(table):
    row_format="{:>8}" * (len(vars) + 1)
    print(row_format.format("", *vars))
    for team, row in zip(row_keys, table):
        print(row_format.format(team, *row))

def sumRows(a,b):
    c = []
    for i in range(len(b)):
        c.append(a[i]+b[i])
    return c;


def substractRows(a,b):
    c = []
    for i in range(len(b)):
        c.append(a[i]-b[i])
    return c;

def multiplyRows(a,b):
    c = []
    for i in range(len(b)):
        c.append(a[i]*b[i])
    return c;

def multiplyOnce(a,b):
    c = []
    for i in range(len(a)):
        c.append(a[i]*b)
    return c;

def max_index(row):
    max_i = 0
    for i in range(0, len(row)-1):
        if row[i] > row[max_i]:
            max_i = i

    return max_i

def simplex():
    global vars
    global foo_value_keys

    rhs_index = vars.index(foo_value_key)
    vars.remove(vars[rhs_index])
    vars.append(foo_value_key)
    rhs_index = vars.index(foo_value_key)

    cost_index = list(foo.keys()).index("COST")
    row_keys.insert(0,list(foo.keys())[cost_index])
    table = []

    const=[]
    foo["COST"]["RHS1"] = foo["COST"]["RHS1"]*M
    for var in vars:
        const.append(foo["COST"].get(var,0)*-1)

    table.append(const)


    for row in row_keys:
        f = []
        for key,value in foo.items():
            if key == "COST":
                continue
            if row in value.keys():
                for var in vars:
                    f.append(value.get(var,0))
        if len(f) > 0:
           table.append(f)



    pivot_y,pivot_x = (0,0)


    table[0] = sumRows(table[0],sumRows(multiplyOnce(table[3],M),multiplyOnce(table[4],M)))
    #table[0] = sumRows(table[0],)

    #printTable(table)


    while(not(checkMin(table[0]))):
        pivot_x = max_index(table[0])
        pivot_y = max_index(getColumn(max_index(table[0]),table[1:]))+1
        print(table[pivot_y][pivot_x])
        table[pivot_x] = multiplyOnce(table[pivot_x],1/table[pivot_y][pivot_x])
        for i in range(0,len(table)):
            if i == pivot_x:
                continue
            table[i] = substractRows(table[i] , multiplyOnce(table[pivot_x],table[pivot_y][i]))
        printTable(table)
        time.sleep(1)




def checkMin(t):
    for i in t:
        if i >0:
            return False
    return True



parse()
normalize()
simplex()

'''
print("--vars--")
print(list(reversed(sorted(vars))))
print("--foo--")
pprint.pprint(json.loads(json.dumps(foo)))
print("--var_consts--")
print(vars_conts)
print("--foo_consts--")
print(vars_conts)
'''
