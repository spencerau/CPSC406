import time

LOOKUP_DICT = {}

def fib_naive(n):
    if (n == 0 or n == 1):
        return n
    else:
        return fib_naive(n-1) + fib_naive(n-2)
    
def fib_memo(n):
    if (n <= 1):
        return n
    elif (n in LOOKUP_DICT):
        return LOOKUP_DICT[n]
    else:
        LOOKUP_DICT[n] = fib_memo(n-1) + fib_memo(n-2)
        return LOOKUP_DICT[n]


n = 40

start_time = time.time()
fib_naive(n)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time for Naive: {elapsed_time} seconds")

start_time = time.time()
fib_memo(n)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time for Memo: {elapsed_time} seconds")