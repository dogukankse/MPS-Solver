# import sys

# file_name = sys.argv[1]

# with open(file_name) as file:
#   mps = file.read()

mps = open("ornek.mps", "r").read()
mpsLines = mps.splitlines(0)
objsense = mpsLines[2]


def Parse():
    costs = ""
    lim1 = ""
    lim2 = ""
    eqns = ""

    for cost in mpsLines:
        if "COST" in cost:
            if "N  COST" in cost:
                continue
            costs += cost + "\n"
    for lim in mpsLines:
        if "LIM1" in lim:
            if "L  LIM1" in lim:
                continue
            lim1 += lim + "\n"
    for lim in mpsLines:
        if "LIM2" in lim:
            if "G  LIM2" in lim:
                continue
            lim2 += lim + "\n"
    for eqn in mpsLines:
        if "EQN" in eqn:
            if "E  EQN" in eqn:
                continue
            eqns += eqn + "\n"
    print("COST:\n" + costs + "\nLim1:\n" + lim1 + "\nLim2:\n" + lim2 + "\nEQN:\n" + eqns)


Parse()
