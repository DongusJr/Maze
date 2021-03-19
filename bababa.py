import sys

# def fibo(n):
#     a_0 = 0
#     a_1 = 1
#     fibo_str = str(a_0) + str(a_1)
#     count = 2
#     while count < n:
#         a_0, a_1 = a_1, a_0 + a_1
#         fibo_str += str(a_1)
#         count += 1
#     return fibo_str

def print_many_A(n):
    count = 1
    while(count <= n):
        a_str = "A"*count
        count_other = print_a(a_str)
        print(f"Compression ratio for {count} is {((count_other*8)/(count*7))*100}%")
        count += 1

def print_a(a_str, other_A = "A"):
    count = 0
    if a_str == "":
        return 0
    try:
        if (a_str[0:len(other_A)]) == other_A:
            count += 1 + print_a(a_str[len(other_A):], other_A+"A")
        else:
            count += print_a(a_str, other_A[:-1])
    except:
        count += print_a(a_str, other_A[:-1])
    return count 

def print_one_A(n):
    a_str = "A"*n
    count_other = print_a(a_str)
    print(f"Compression ratio for {n} is {((count_other*8)/(n*7))*100}%")

if __name__ == "__main__":
    sys.setrecursionlimit(1000001)
    # with open("fibonumbers.txt", "w") as w:
    #     fibo_str = fibo(10000)
    #     w.write(fibo_str)
    print_many_A(100000)
    # print_one_A(1000000)
    