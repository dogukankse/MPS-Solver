# import sys

# file_name = sys.argv[1]

# with open(file_name) as file:
#   mps = file.read()

mps = open("ornek.mps", "r").read()
mpsLines = mps.splitlines(0)
objsense = mpsLines[2]

costs = []
lim1 = []
lim2 = []
eqns = []


def listPrinter():
    for item in costs:
        print(item)
    print("-" * 100)
    for item in lim1:
        print(item)
    print("-" * 100)
    for item in lim2:
        print(item)
    print("-" * 100)
    for item in eqns:
        print(item)
    print("-" * 100)


def parse():
    globals()

    for cost in mpsLines:
        if "COST" in cost:
            if "N  COST" in cost:
                continue
            costs.append(cost)
    for lim in mpsLines:
        if "LIM1" in lim:
            if "L  LIM1" in lim:
                continue
            lim1.append(lim)
    for lim in mpsLines:
        if "LIM2" in lim:
            if "G  LIM2" in lim:
                continue
            lim2.append(lim)
    for eqn in mpsLines:
        if "EQN" in eqn:
            if "E  EQN" in eqn:
                continue
            eqns.append(eqn)
    listPrinter()
    simplex()


print(objsense)


def simplex():
    globals()

    if "MIN" in objsense:
        print(objsense)
    elif "MAX" in objsense:
        print(objsense)

    print(costs[0])
    print(lim1[0])
    print(lim2[0])
    print(eqns[0])


parse()
