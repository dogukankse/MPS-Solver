mps = open("ornek3.mps", "r").read()
objsense=False
if "MIN" in mps:
  objsense = True

#print(mps)
#print(objsense)

FOO = dict()


def removeEmpty(s):
  for i in range(1,16):
    s = s.strip().replace(" "*i," ").replace("\t","")
  a = s.replace(u"\u0014", "").replace(",",".").split(' ')
  b =[]
  for i in a:
    if not(i == ""):
      b.append(i)
  return b

def parser(mps):
  for row in mps[mps.find("FOO")+5:mps.find("COLUMNS")].splitlines(0):
    row = removeEmpty(row)
    FOO[row[1]] = {}

  for row in mps[mps.find("COLUMNS")+8:mps.find("RHS")].splitlines(0):
    row = removeEmpty(row)
    FOO[row[1]][row[0]] = float(row[2])
    if len(row)>3:
      FOO[row[3]][row[0]] = float(row[4])

def primalSimplex():
    '''
    1. standart hale getir(büyük eşit ve küçük eşit olan kısıtlara S ekle-çıkar eşitlik yap)
    '''

def twoPhaseSimplex():
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

def standardize():
  ''''
  standart hale getirme fonksiyonu
  eklenen S değişkenleri 0'dan büyük olacak
  '''  

  

parser(mps)
print(FOO)