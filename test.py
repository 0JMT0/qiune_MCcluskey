from prettytable import PrettyTable

def int_to_binary(n,digits):
    return format(n,f'0{digits}b')

def count_ones(binary):
    return binary.count('1')

def findDigit(in_list):
    digits = 0
    m = max(in_list)
    while m > 0:
        m //= 2
        digits += 1
    return digits

def ones_sort(mtlist,dig):
    sort = []
    sorted = []
    for s in range(dig+1): # s代表1的個數
        for dec in mtlist: # dec代表minterms的數值
            if count_ones(int_to_binary(dec,dig)) == s:
                sort.append(dec)
        sorted.append(bubblesort(sort))
        sort = []
    return sorted

def bubblesort(bubble):
    if len(bubble) > 1:
        n = len(bubble)
        for i in range(n-1):
            for j in range(n-i-1):
                if bubble[j] > bubble[j+1]:
                    temp = bubble[j]
                    bubble[j] = bubble[j+1]
                    bubble[j+1] = temp
    return bubble

def flatten(l):
    return [item for sublist in l for item in sublist]

def comb(sd,dig,mode):
    #sd->sorted
    combine = []
    PI = []
    check = []
    comb_yes = []
    if mode == 0:
        for ones in range(len(sd)-1):
            cp1_list = sd[ones]
            cp2_list = sd[ones+1]
            for cp1 in cp1_list:
                combined = 0
                for cp2 in cp2_list:
                    for bit in range(dig):
                        if (cp1 + (2**bit)) == cp2:
                            combine.append([cp1,cp2,bit])
                            combined = 1
                    if combined == 1:
                        comb_yes.append(cp1)
                        comb_yes.append(cp2)
        PI = bubblesort(list(set(flatten(sd)) - set(comb_yes))) 
    if mode == 1:
        for index1 in range(len(sd)):
            each1 = sd[index1]
            dontcare1 = each1[-1]
            for index2 in range(len(sd)): 
                repeated = 0
                comb_yes = []
                each2 = sd[index2]
                dontcare2 = each2[-1]
                if (index2 != index1) and (dontcare1 == dontcare2):
                    comb_yes.append(bubblesort(each1[:-1]+each2[:-1]))
                if comb_yes != []:
                    for c in range(len(check)):
                        if comb_yes[0] == check[c]:
                           repeated = 1
                    if repeated == 0:
                        combine.extend(comb_yes)   
                check.append(bubblesort(each1[:-1]+each2[:-1]))  
    return (combine,PI)

def dontcareS(binary,dc,dig):
    str1 = " "
    binaryS = [str(i) for i in binary]
    binaryS[abs(dig-dc-1)] = '-'
    return (str1.join(binaryS))

def Table(sorteddec,sorteddecf):
    table = PrettyTable(["Ones","Minterms(dec)","Minterms(bin)"])
    repeated_ones = -1
    for t in range(len(sorteddecf)):
        bi = int_to_binary(sorteddecf[t],dig)
        o = count_ones(bi)
        if o == repeated_ones:
            table.add_row(["",sorteddecf[t],bi])
        else:
            table.add_row([o,sorteddecf[t],bi])
        repeated_ones = o

################################################################main

stage = PrettyTable(["Combine(dec)","Combine(bin)"])

mt_list = [6,9,13,18,19,25,27,29,41,45,57,61]
# b_list = [0,5,7,8,16,26,29,30,31]
# b_list = [20,28,38,39,52,60,102,103,127]
# b_list = [6,9,13,18,19,25,27,29,41,45,57,61]

dig = findDigit(mt_list)
sorteddec = ones_sort(mt_list,dig)
################################################################table
# Table(sorteddec,flatten(sorteddec))
# print(table)
################################################################stages
Combine = comb(sorteddec,dig,0)[0]
PrimeI = []
#PrimeI.append(int_to_binary((comb(sorteddec,dig)[1])[0],dig))
for t in range(len(Combine)):
    bi = int_to_binary((Combine[t])[0],dig)#取出每一組第一個值
    symbol = (Combine[t])[-1]#最後一個數值
    stage.add_row([Combine[t][0:2],dontcareS(bi,symbol,dig)])
#print(stage)
Combine = comb(Combine,dig,1)[0]
print(Combine)
# print(PrimeI)