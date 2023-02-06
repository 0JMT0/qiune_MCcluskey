class Term:
    def __init__(self, term, ones):
        self.term = term
        self.ones = ones

    def check(self):
        print(f"Terms = {self.term} and oneNUM = {self.ones}")

def findDigit(in_list):
    digits = 0
    m = max(in_list)
    while m > 0:
        m //= 2
        digits += 1
    return digits

def int_to_binary(n,digits):
    return format(n,f'0{digits}b')

def count_ones(binary):
    return binary.count('1')

################################Main
mt_lst = [int(mt) for mt in input("Please input minterms : ").split()]
binary_lst = []
ones_lst = []
dig = findDigit(mt_lst)
################################Create Term
for value in mt_lst:
    binary_lst.append(int_to_binary(value,dig))
for value in binary_lst:
    ones_lst.append(count_ones(value))
print(binary_lst)
# print(ones_lst)
minterms = Term(binary_lst,ones_lst)
################################Create done
#minterms.check()