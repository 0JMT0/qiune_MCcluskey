from prettytable import PrettyTable
import itertools

def int_to_binary(n):
    return format(n,f'0{digits}b')

def count_ones(binary):
    return binary.count('1')

def twoPowerORnot(b):
    twoPower = False

    for bit in range(digits):
        if b == (2**bit):
            twoPower = True
    return twoPower

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

def comb(sd,mode):#sd->sorted
    PI = []
    all = []
    combine = []
    check1 = []
    check2 = []
    comb_yes = []
    global alone_PI

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
        if PI != []:
            alone_PI = True

    if mode == 1:
        for index1 in range(len(sd)):
            dontcare1 = []
            each1 = sd[index1]#取出每一組
            all.append(each1)
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
                if (index2 != index1) and (dontcare1 == dontcare2) and (ones1 == ones2-1) and (twoPowerORnot(each2[0]-each1[0])):#不是同一個、don't care位置一樣、1個數差一、差為2的冪次
                    cy = bubblesort(each1[:-1]+each2[:-1])
                    comb_yes.append(cy)
                if comb_yes != []:
                    check2.append(each1)#存合併過的
                    check2.append(each2)
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

def dontcareS(binary, bits):
    str1 = " "
    binaryS = [str(i) for i in binary]

    if bits != -1:#表示不是帶有don't care位元
        if type(bits) == int:
            binaryS[abs(digits-bits-1)] = '-'
        else:
            for dc in range(len(bits)):
                binaryS[abs(digits-bits[dc]-1)] = '-'
        return (str1.join(binaryS))

    if type(bits) == int:
        return (str1.join(binaryS))

def table(Dec_list,mode):
    global Table,Stage,Prime_Implicants,PI_bins,alone_PI
    PI_bins = []
    Table = PrettyTable(["Ones","Minterms(dec)","Minterms(bin)"])
    Table.align["Minterms(dec)"] = "l"
    Stage = PrettyTable(["Ones","Combined(dec)","Combined(bin)"])
    Stage.align["Combined(dec)"] = "l"
    Prime_Implicants = PrettyTable(["Combined(dec)","Combined(bin)"])
    Prime_Implicants.align["Combined(dec)"] = "l"
    repeated_ones = -1

    if mode == 0:
        for t in range(len(Dec_list)):
            bi = int_to_binary(Dec_list[t])
            o = count_ones(bi)
            if o == repeated_ones:
                Table.add_row(["",Dec_list[t],bi])
            else:
                Table.add_row([o,Dec_list[t],bi])
            repeated_ones = o

    if mode == 1:
        Stage.clear
        for t in range(len(Dec_list)):
            bi = int_to_binary((Dec_list[t])[0])
            ones = count_ones(bi)
            if ones == repeated_ones:
                Stage.add_row(["",(Dec_list[t])[:-1],dontcareS(bi,(Dec_list[t])[-1])])
            else:
                Stage.add_row([ones,(Dec_list[t])[:-1],dontcareS(bi,(Dec_list[t])[-1])])
            repeated_ones = ones

    if mode == 2:
        for t in range(len(Dec_list)):
            bi = int_to_binary((Dec_list[t])[0])
            if Dec_list[t] == Dec_list[0] and alone_PI:#第一格且是單個數組成的PI
                for l in range(len(Dec_list[0])):
                    bi = int_to_binary((Dec_list[0])[l])
                    bi_with_dc = dontcareS(bi,-1)
                    PI_bins.append(bi_with_dc)
                    Prime_Implicants.add_row([(Dec_list[0])[l],bi_with_dc])#-1表示都是單個數組成的PI的模式
            else:
                bi_with_dc = dontcareS(bi,(Dec_list[t])[-1])
                PI_bins.append(bi_with_dc)
                Prime_Implicants.add_row([(Dec_list[t])[:-1],bi_with_dc])

def chart(mt,decs,bins):
    global Chart,alone_PI
    Chart = PrettyTable(" ")
    Chart.hrules = 1
    Xpositions = []
    Nomatch = True

    for pi in range(len(bins)):
        Chart.add_row([bins[pi]])

    if alone_PI:
        alones = decs[0]
        decs.remove(decs[0])
        for l in range(len(alones)):#將單個得拆成獨立一個在list
            decs.insert(l,alones[l])

    for l in range(len(decs)):
        if type(decs[l]) == list:
            cache = (decs[l])[:-1]
            decs.remove(decs[l])
            decs.insert(l,cache)

    for each1 in range(len(mt)):#each1為mt_list中每一項的位置
        for each2 in range(len(decs)):#each2為clean_PI中每一項的位置
            Nomatch = True
            if type(decs[each2]) == int and decs[each2] == mt[each1]:
                Xpositions.append("X")
                Nomatch = False
            if type(decs[each2]) == list:
                for each3 in range(len(decs[each2])):#each3為clean_PI中每一項list之中的每個位置
                    if (decs[each2])[each3] == mt[each1]:
                        Xpositions.append("X")
                        Nomatch = False
            if Nomatch:
                Xpositions.append(" ")
        Chart.add_column("{}".format(mt[each1]),Xpositions)
        Xpositions = []
################################################################[MAIN]
mt_list = [int(mt) for mt in input("Please input minterms and don't cares in order: ").split()]
Combine = []
PrimeI = []
CandP = []#Combine和PrimeI的緩存
global digits
global alone_PI 
alone_PI = False
if mt_list != []:
    digits = finddigit(mt_list)
    sorteddec = ones_sort(mt_list)
    stages = len(sorteddec)
#################################################################[table]
    print("STAGE 0")
    table(flatten(sorteddec),0)
    print(Table)
#################################################################[stages]
    CandP = comb(sorteddec,0)
    Combine = CandP[0]
    PrimeI.append(CandP[1])
    if Combine != []:
        print("STAGE {}".format(len(sorteddec)-stages+1))
        # print(Combine)
        table(Combine,1)
        print(Stage)
    else:
        alone_PI = True
    stages -= 1
    while stages > 0:
        CandP = comb(Combine,1)
        Combine = CandP[0]
        PrimeI.extend(CandP[1])
        if Combine == []:
            break
        print("STAGE {}".format(len(sorteddec)-stages+1))
        table(Combine,1)
        print(Stage)
        # print(Combine)
        stages -= 1
    # print("Prime Implicants:\n{}".format(list(filter(None,PrimeI))))#去除空的項並印出
    print("Prime Implicants")
    clean_PI = list(filter(None,PrimeI))
    table(clean_PI,2)
    print(Prime_Implicants)
    chart(mt_list,clean_PI,PI_bins)
    print("Chart")
    print(Chart)
else:
    print("WTF are you doing?")