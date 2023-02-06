from prettytable import PrettyTable
import itertools

def int_to_binary(n):
    return format(n,f'0{digits}b')

def count_ones(binary):
    return binary.count('1')

def finddigit(in_list):

    if type(in_list) == int:
        dig = -1
        m = in_list
        while m > 0:
            m //= 2
            dig += 1
    else:
        dig = 0
        m = max(in_list)
        while m > 0:
            m //= 2
            dig += 1
    return dig

def ones_sort(mtlist):
    sort = []
    sorted = []
    for s in range(digits+1): # s代表1的個數
        for dec in mtlist: # dec代表minterms的數值
            if count_ones(int_to_binary(dec)) == s:
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

def comb(sd,mode,stage):
    #sd->sorted
    PI = []
    all = []
    combine = []
    check1 = []
    check2 = []
    comb_yes = []
    if mode == 0:
        for ones in range(len(sd)):
            if ones != len(sd)-1:
                cp1_list = sd[ones]
                cp2_list = sd[ones+1]
                for cp1 in cp1_list:
                    combined = 0
                    for cp2 in cp2_list:
                        for bit in range(digits):
                            if (cp1 + (2**bit)) == cp2:
                                combine.append([cp1,cp2,bit])
                                combined = 1
                        if combined == 1:
                            comb_yes.append(cp1)
                            comb_yes.append(cp2)
        PI = bubblesort(list(set(flatten(sd)) - set(comb_yes))) 
    if mode == 1:
        for index1 in range(len(sd)):
            dontcare1 = []
            each1 = sd[index1]#取出每一組
            all.append(each1[:-1])
            ones1 = count_ones(int_to_binary(each1[0]))#透過第一位知道1的個數來分組
            if type(each1[-1]) == int:
                dontcare1.append(each1[-1])
            else:
                dontcare1.extend(each1[-1])
            for index2 in range(len(sd)): 
                repeated = False
                comb_yes = []
                dontcare2 = []
                each2 = sd[index2]
                ones2 = count_ones(int_to_binary(each2[0]))
                if type(each2[-1]) == int:
                    dontcare2.append(each2[-1])
                else:
                    dontcare2.extend(each2[-1])
                if (index2 != index1) and (dontcare1 == dontcare2) and (ones1 == ones2-1) and (finddigit(each2[0]-each1[0]) != -1):#不是同一個、don't care位置一樣、1個數差一、差不為基數
                    cy = bubblesort(each1[:-1]+each2[:-1])
                    comb_yes.append(cy)
                if comb_yes != []:
                    check2.append(each1[:-1])#存合併過的
                    check2.append(each2[:-1])
                    for c in range(len(check1)):#是否重複
                        if comb_yes[0] == check1[c]:
                           repeated = True
                    if repeated == False:
                        dontcare2.append(finddigit(each2[0]-each1[0]))
                        comb_yes = list(itertools.chain.from_iterable(comb_yes))#將list拆開和don't care重組
                        comb_yes.append(bubblesort(dontcare2))
                        combine.append(comb_yes)   
                    check1.append(bubblesort(each1[:-1]+each2[:-1]))
        PI = [i for i in all if i not in check2]
    return (combine,PI)

def dontcareS(binary, dc):
    str1 = " "
    binaryS = [str(i) for i in binary]
    binaryS[abs(digits-dc-1)] = '-'
    return (str1.join(binaryS))

def Table(sorteddecf):
    table = PrettyTable(["Ones","Minterms(dec)","Minterms(bin)"])
    repeated_ones = -1
    for t in range(len(sorteddecf)):
        bi = int_to_binary(sorteddecf[t])
        o = count_ones(bi)
        if o == repeated_ones:
            table.add_row(["",sorteddecf[t],bi])
        else:
            table.add_row([o,sorteddecf[t],bi])
        repeated_ones = o

################################################################main
Stage = PrettyTable(["Combine(dec)","Combine(bin)"])
mt_list = [6,9,13,18,19,25,27,29,41,45,57,61]
# b_list = [0,5,7,8,16,26,29,30,31]
# b_list = [20,28,38,39,52,60,102,103,127]
# b_list = [6,9,13,18,19,25,27,29,41,45,57,61]
global digits
digits = finddigit(mt_list)
sorteddec = ones_sort(mt_list)
################################################################table
# Table(flatten(sorteddec))
# print(table)
################################################################stages
stage = 0
Combine = comb(sorteddec,0,stage)[0]
PrimeI = []
CandP = []

# for t in range(len(Combine)):
#     bi = int_to_binary((Combine[t])[0])#取出每一組第一個值
#     symbol = (Combine[t])[-1]#最後一個數值
#     Stage.add_row([Combine[t][0:2],dontcareS(bi,symbol)])

stage = 1
CandP = comb(Combine,1,stage)
Combine = CandP[0]
PrimeI = CandP[1]
print(Combine)
print(PrimeI)