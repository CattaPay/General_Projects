import pandas as pd
import numpy as np
import time

colnames = []
for i in range(8):
    colnames.append("dig" + str(i))

nerdledat = pd.read_csv("nerdlesolving\\allbois.csv", names = colnames, header = None)

nerdarray = nerdledat.values

bruh = True
i = 0
while bruh:
    if nerdarray[i][0] >= 10:
        bruh = False
        firstbad = i
    i += 1

goodarray = nerdarray[:firstbad]

def checkans(real, guess):
    res = [-1] * 8 # 0 is no match, 1 is inexact, 2 is exact
    got = [False] * 8
    # first pass only check if exact
    for i in range(8):
        if real[i] == guess[i]:
            res[i] = 2
            got[i] = True
    
    
    # second pass check all
    for i in range(8):
        if res[i] != 2:
            dig = guess[i]
            sat = True
            j = 0
            while j < 8 and sat:
                if not got[j] and dig == real[j]:
                    got[j] = True
                    res[i] = 1
                    sat = False
                j += 1
            if sat:
                res[i] = 0
    return(res)
            
def checkleadzero(boi):
    if boi[0] == 0: #check if first dig is 0
        return(True)

    for i in range(6): # check if op - 0 - dig
        if boi[i] >= 10 and boi[i+1] == 0 and boi[i+2] < 10:
            return(True)

    return(False)

def restoscore(boi): #converts guess array to an int value
    val = 0
    for i in range(8):
        val += 3 ** i * boi[i]
    return(val)







leadzeros = []
arrlen = len(goodarray)

for i in range(arrlen):
    leadzeros.append(checkleadzero(goodarray[i]))


noleadzeros = []
for i in range(arrlen):
    if not leadzeros[i]:
        noleadzeros.append(goodarray[i])
nlz = np.asarray(noleadzeros)

nlzlen = len(nlz)

fname = "scores2.csv"
largebox = []
startcase = 400
testcases = 600
time1 = time.perf_counter()
for i in range(startcase, startcase + testcases):
    scoreboard = [0] * (3 ** 8)
    for j in range(nlzlen):
        val = restoscore(checkans(nlz[i], nlz[j]))
        scoreboard[val] += 1
    largebox.append(scoreboard)
    print((i-startcase)/testcases * 100, "%")

time2 = time.perf_counter()
ops = testcases * nlzlen
print("operations: ", ops)
print("total time: ", time2-time1)
print("ops per sec: ", ops / (time2-time1))
print("est. time to cmpt: ", nlzlen * nlzlen / (ops / (time2-time1)))
print("est. time per lap: ", (time2-time1) / testcases)

largebox = np.asarray(largebox, dtype = "int")

np.savetxt("nerdlesolving\\" + fname, largebox, fmt='%i', delimiter=",")
