import re
import sys

mps = open("ornek.mps", "r").read()
objsense = False
if "MIN" in mps:
    objsense = True

s_count = 0
r_count = 0
FOO = dict()
FOO_CONST = dict()
VAR_CONST = dict()


def removeEmpty(s):
    for i in range(1, 16):
        s = s.strip().replace(" " * i, " ").replace("\t", "")
    a = s.replace(u"\u0014", "").replace(",", ".").split(' ')
    b = []
    for i in a:
        if not (i == ""):
            b.append(i)
    return b


def parser(mps):
    for row in mps[mps.find("ROWS") + 5:mps.find("COLUMNS")].splitlines(0):
        row = removeEmpty(row)
        FOO[row[1]] = {}
        FOO_CONST[row[1]] = row[0]

    for row in mps[mps.find("COLUMNS") + 8:mps.find("RHS")].splitlines(0):
        row = removeEmpty(row)
        FOO[row[1]][row[0]] = float(row[2])
        if len(row) > 3:
            FOO[row[3]][row[0]] = float(row[4])

    for row in mps[mps.find("RHS") + 4:mps.find("BOUNDS")].splitlines(0):
        row = removeEmpty(row)
        FOO[row[1]][row[0]] = float(row[2])
        if len(row) > 3:
            FOO[row[3]][row[0]] = float(row[4])

    for row in mps[mps.find("BOUNDS") + 7:mps.find("ENDATA")].splitlines(0):
        row = removeEmpty(row)
        if len(row) > 3:
            VAR_CONST[row[2]] = [row[0], float(row[3])]
        else:
            VAR_CONST[row[2]] = [row[0], None]
    return FOO


def getRSVars(foo):
    vars = list()
    for key, value in foo.items():
        if "r" == key or "CONTS" == key:
            continue
        for var in value:
            if match(var, '[R][^H]+[0-9]*'):
                if var not in vars:
                    vars.append(var)
            if match(var, '[S][^H]+[0-9]*') and value[var] == 1:
                if var not in vars:
                    vars.append(var)
    return vars


def printTable(table, column_keys, row_keys):
    print("------------")
    row_format = "{:<8}" * (len(column_keys) + 1)
    print(row_format.format("", *column_keys))
    for team, row in zip(row_keys, table):
        print(row_format.format(team, *row))
    print("------------")


def getVars(foo):
    vars = list()
    for key, value in foo.items():
        for var in value:
            if var in vars:
                continue
            vars.append(var)
    vars = sorted(list(vars), reverse=True)
    vars.remove("RHS1")
    vars.append("RHS1")
    return vars


def max_index(row):
    max_i = 0
    for i in range(0, len(row) - 1):
        if row[i] > row[max_i]:
            max_i = i
    return max_i


def min_index(row):
    max_i = 0
    for i in range(0, len(row) - 1):
        if row[i] < row[max_i]:
            max_i = i
    return max_i


def getColumnKey(table):
    if objsense == True:
        column_key_index = max_index(table[0])
    else:
        column_key_index = min_index(table[0])

    return column_key_index


def getRowIndex(column_key, table):
    min = float('inf')
    min_index = -1
    c = getColumn(column_key, table)
    for index, i in enumerate(c):
        if index == 0:
            continue
        if i <= 0:
            continue
        t = table[index][-1]
        if (t / i) < min:
            min = table[index][-1] / i
            min_index = index
        if min == float('inf') or min_index == -1:
            print("Çözümsüz")
            sys.exit(0)
    return min_index


def getPivot(table):
    column_key = getColumnKey(table)
    row_key = getRowIndex(column_key, table)
    return (row_key, column_key)


def getColumn(y, table):
    a = []
    for i in range(len(table)):
        a.append(table[i][y])
    return a


def iterate(table, row_key, column_key):
    for index, row in enumerate(table):
        if index == row_key:
            continue
        table[index] = substractRows(table[index], (multiplyOnce(table[row_key], table[index][column_key])))
    return table


def substractRows(a, b):
    c = []
    for i in range(len(b)):
        c.append(round(a[i] - b[i]))
    return c;


def sumRows(a, b):
    c = []
    for i in range(len(b)):
        c.append(round(a[i] + b[i]))
    return c;


def round(a):
    return float(("%0.2f" % a))


def multiplyRows(a, b):
    c = []
    for i in range(len(b)):
        c.append(round(a[i] * b[i]))
    return c;


def divisionOnce(array, pivot):
    c = []
    for i in range(len(array)):
        c.append(round(array[i] / pivot))
    return c;


def multiplyOnce(array, pivot):
    c = []
    for i in range(len(array)):
        c.append(round(array[i] * pivot))
    return c;


def primalSimplex(foo):
    '''
    1. standart hale getir(büyük eşit ve küçük eşit olan kısıtlara S ekle-çıkar eşitlik yap)
    '''


def twoPhaseSimplex(foo):
    '''
      1. standart hale getir(büyük eşit ve küçük eşit olan kısıtlara S ekle-çıkar eşitlik yap)
      2. litmit fonksiyonlarının değişken sayısı eşit ve kat sayıları +1 olmalıdır eğer değilse R yapay değişkeni değişken sayısı
          eksik olanlara eklenir. yapay değişken sadece = ve >= kısıtları olan limit fonksiyonlarına eklenir
      3. 1.Faz: amaç fonksiyonu r=R1+R2+....+Rn şeklinde tekrar yazılır. R'leri denklemden çekerek R'lerin eşitliğini buluruz.
          r fonksiyonunu buna göre düzenleriz(sabitler sağ değişkenler sol) Tabloyu oluştur(üst tarafta tüm değişkenler, sol tarafta bizim eklediğimiz değişkenler)
          r fonksiyonunda negatif(max için pozitif) değer kalmayıncaya kadar itere et. rnin sts 0 değilse çözümsüzdür
      4. 2.faz:R sutunlarını tablodan çıkar. satırdan kaysayıları alarak denklem oluştur. yeni denklemler bizim kısıt fonksiyonlarımız oluyo.
          amaç fonsiyonu nelere bağlı ise kısıt fonksiyonlarından onları çek.
      '''
    foo = createRFoo(foo)
    columns = getVars(foo)
    rows = getRSVars(foo)
    rows.insert(0, "r")
    table = createTable(foo, columns, rows)
    printTable(table, column_keys=columns, row_keys=rows)
    print("ITERASYON BASLIYOR")
    while (not (isFinished(table, objsense))):
        row_key, column_key = getPivot(table)
        table[row_key] = divisionOnce(table[row_key], table[row_key][column_key])
        table = iterate(table, row_key, column_key)
        rows[row_key] = columns[column_key]
        printTable(table, column_keys=columns, row_keys=rows)

    for index, var in enumerate(columns):
        if match(var, '[R][^H]+[0-9]*'):
            for tableIndex, tableVar in enumerate(table):
                del table[tableIndex][index]

    r = []
    for var in columns:
        if match(var, '[R][^H]+[0-9]*'):
            r.append(var)
    for i in r:
        columns.remove(i)

    printTable(table, column_keys=columns, row_keys=rows)
    minimize(columns, table, rows)
    return foo


def minimize(columns, table, rows):
    ###### r yi Z olarak yazma
    for index, column in enumerate(table):
        if index == 0:
            continue
        for c, b in enumerate(column):
            if table[0][c] != 0:
                table[0] = sumRows(table[0], multiplyOnce(table[index], -table[0][c]))
    printTable(table, column_keys=columns, row_keys=rows)

    birimList = dict()
    for y, column in enumerate(table):
        #satırları gez
        if y == 0:
            continue
        for x, row in enumerate(column):
            #sütünlari gez
            if x == len(column)-1:
                continue
            #her sütün için girdi aç
            birimList[x] = 0
            if row == 1:
                birimList[x] = birimList[x] +1
    print(birimList)

    return table


def isFinished(table, objsense):
    if objsense:
        # min
        for v in table[0][:len(table[0]) - 1]:
            if (v > 0):
                return False
        return True
    else:
        for v in table[0][:len(table[0]) - 1]:
            if (v < 0):
                return False
        return True


def createTable(foo, vars, rs_vars):
    table = []
    r = []
    for var in vars:
        r.append(foo["r"].get(var, 0) * -1)
    table.append(r)
    for row in rs_vars:
        f = []
        for key, value in foo.items():
            if key == "COST" or key == "r":
                continue
            if row in value.keys():
                for var in vars:
                    f.append(value.get(var, 0))
        if len(f) > 0:
            table.append(f)
    return table


def checkInDict(value, regex):
    for key in value:
        if match(key, regex):
            return True
    return False


def match(var, regex):
    return re.match(regex, var) != None


def createRFoo(foo):
    s_count = 0
    r = dict()
    for key, value in foo.items():
        if checkInDict(value, '[R][^H]+[0-9]*'):
            for variable in value:
                if match(variable, '[R][^H]+[0-9]*'):
                    continue
                r_variable = variable
                if match(variable, '[S][^H]+[0-9]*'):
                    s_count += 1
                    r_variable = "S%d" % s_count
                if r.get(variable, None) == None:
                    r[r_variable] = value[variable] * -1
                else:
                    r[r_variable] += value[variable] * -1
    foo.update({"r": r})
    return foo


def addVar(variable_name, foo, foo_key, value):
    foo[foo_key][variable_name] = value


def standardize(foo):
    ''''
    standart hale getirme fonksiyonu
    eklenen S değişkenleri 0'dan büyük olacak
    '''
    global s_count
    global r_count
    for key, value in FOO_CONST.items():
        if value == 'L':
            s_count += 1
            addVar('S%d' % s_count, foo, key, 1)
        elif value == 'G':
            s_count += 1
            addVar('S%d' % s_count, foo, key, -1)
            r_count += 1
            addVar('R%d' % r_count, foo, key, 1)
        elif value == 'E':
            r_count += 1
            addVar('R%d' % r_count, foo, key, 1)
    for key, value in foo.items():
        if value.get("RHS1", 0) < 0:
            for var in value:
                foo[key][var] = foo[key][var] * -1

    if r_count > 0:
        return twoPhaseSimplex(foo)
    else:
        return primalSimplex(foo)


FOO = parser(mps)
FOO = standardize(FOO)
