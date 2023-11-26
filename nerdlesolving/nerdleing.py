# nerdle stuff

import time

# teststr = "56-10*2=36"

# bois = teststr.split("=")

# ops = ["+", "-", "*", "/", "="]

def boxtonum(arra):
    count = 0
    for i in range(len(arra)):
        count += arra[i] * (10 ** i)
    return(count)

def countinbox(arra, num):
    count = 0
    for i in range(len(arra)):
        if num == arra[i]:
            count += 1

def flipfloop(arra):
    outbox = []
    for i in range(len(arra)):
        outbox.append(arra[len(arra)-i-1])
    return(outbox)

def divzerocheck(vals, n):
    return(vals[n+1] == 0)
            

def collapse(vals, n, op): # 10 is +, 11 is -, 12 = *, 13 = /
    newvals = []
    for i in range(len(vals)-1):
        if i < n:
            newvals.append(vals[i])
        elif i == n:
            if op == 10:
                newvals.append(vals[i] + vals[i+1])
            elif op == 11:
                newvals.append(vals[i] - vals[i+1])
            elif op == 12:
                newvals.append(vals[i] * vals[i+1])
            elif op == 13:
                newvals.append(vals[i] / vals[i+1])
        else:
            newvals.append(vals[i+1])
    return(newvals)



def calcs(vals, ops):
    newops = []
    for i in range(len(ops)):
        newops.append(ops[i])
    
    while 12 in newops or 13 in newops:    
        for i in range(len(newops)):
            if newops[i] == 12:
                vals = collapse(vals, i, 12)
                newops.pop(i)
                break
            elif newops[i] == 13:
                if divzerocheck(vals, i):
                    return("Div0", [])
                vals = collapse(vals, i, 13)
                newops.pop(i)
                break

    while 10 in newops or 11 in newops:    
        for i in range(len(newops)):
            if newops[i] == 10:
                vals = collapse(vals, i, 10)
                newops.pop(i)
                break
            elif newops[i] == 11:
                vals = collapse(vals, i, 11)
                newops.pop(i)
                break
    return(vals, newops)



def combos(n, bois, seed):
    outbox = [0]*n
    for i in range(n):
        exp = (bois**(n-i-1))
        delta = seed // exp
        outbox[i] = delta
        seed -= delta * exp
    return(outbox)

def backtoback(arra):
    for i in range(len(arra)-1):
        if arra[i] >= 10 and arra[i+1] >= 10:
            return(True)
    return(False)



#convert string to rep

# rep = [0]*len(teststr)
# for i in range(len(teststr)):
#     if teststr[i] in ops:
#         rep[i] = int(ops.index(teststr[i])+10)
#     else:
#         rep[i] = int(teststr[i])



# place = 0
# box = []
# numbres = []
# operations = []
# for i in range(len(teststr)):
#     bruh = len(teststr)-i-1
#     if rep[bruh] <= 9:
#         box.append(rep[bruh])
#     else:
#         numbres.append(boxtonum(box))
#         box = []
#         operations.append(rep[bruh])
#     if bruh == 0:
#         numbres.append(boxtonum(box))
#         box = []
# numbres = flipfloop(numbres)
# operations = flipfloop(operations)

# # do multiplication and division
# endnums, endops = calcs(numbres, operations)

# #print(endnums)

# #check if right
# truth = (endnums[0] == endnums[1])


# # generate test cases



#f = open("bruh.csv", "w")
leng = 15 ** 8

goodcount = 0
greatcount = 0

tim = time.perf_counter()
for k in range(leng):
    if k % 100000 == 0:
        print("{:.3%}".format(k/leng))
    # 1) only one equals sign
    # 2) no operations to right of equals sign
    
    testcase = combos(8, 15, k)
    #print(testcase)
    equalscount = False
    signtoright = False
    for i in testcase:
        if i == 14 and not equalscount:
            equalscount = True
        elif equalscount:
            if i >= 10:
                signtoright = True

    if equalscount and not signtoright and not (testcase[len(testcase)-1] == 14 or testcase[0] == 14):
        # 3) no back to back operations
        if not backtoback(testcase):
            #4) does it work?
            goodcount += 1
            box = []
            numbres = []
            operations = []
            for i in range(len(testcase)):
                bruh = len(testcase)-i-1
                if testcase[bruh] <= 9:
                    box.append(testcase[bruh])
                else:
                    numbres.append(boxtonum(box))
                    box = []
                    operations.append(testcase[bruh])
                if bruh == 0:
                    numbres.append(boxtonum(box))
                    box = []
            numbres = flipfloop(numbres)
            operations = flipfloop(operations)


            
            # do multiplication and division
            endnums, endops = calcs(numbres, operations)

            if(endnums[0] == endnums[1]):
                outstr = ""
                for i in range(len(testcase)-1):
                    outstr += str(testcase[i]) + ","
                outstr += str(testcase[len(testcase)-1]) + "\n"
                #f.write(outstr)             
                greatcount += 1
#f.close()
print(time.perf_counter() - tim)
print(goodcount / leng)
print(greatcount / leng) 

# 92.649s for 15^6 
# 66.324s for 15^6

# 50s for 15^6 on vscode
# 674.5s for 15^7