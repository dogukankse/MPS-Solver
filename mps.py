# import sys
import re
import json
import sys
# file_name = sys.argv[1]

# with open(file_name) as file:
#   mps = file.read()

mps = open("ornek2.mps", "r").read()
mpsLines = mps.splitlines(0)
objsense = mpsLines[2]

foo_const = {}
foo = {}
vars = set()
vars_conts = {}


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

    for row in mps[mps.find("ROWS")+5:mps.find("COLUMNS")].splitlines(0):
        row = removeEmpty(row)
        foo[row[1]] = {}
        foo_const[row[1]] = row[0]


    for row in mps[mps.find("COLUMNS")+8:mps.find("RHS")].splitlines(0):
        row = removeEmpty(row)
        vars.add(row[0])
        foo[row[1]][row[0]] = float(row[2])
        if len(row)>3:
            foo[row[3]][row[0]] = float(row[4])

    for row in mps[mps.find("RHS")+4:mps.find("BOUNDS")].splitlines(0):
        row = removeEmpty(row)
        vars.add(row[0])
        foo[row[1]][row[0]] = float(row[2])
        if len(row)>3:
            foo[row[3]][row[0]] = float(row[4])

    for row in mps[mps.find("BOUNDS")+7:mps.find("ENDATA")].splitlines(0):
        row = removeEmpty(row)
        if len(row)>3:
            vars_conts[row[2]]= [row[0], float(row[3])]
        else:
            vars_conts[row[2]]= [row[0], None]


    print("var_consts")
    print(json.dumps(vars_conts))
    print("foos")
    print(json.dumps(foo))
    #simplex()




def simplex():
    globals()

    if "MIN" in objsense:
        print(objsense)
    elif "MAX" in objsense:
        print(objsense)


parse()
