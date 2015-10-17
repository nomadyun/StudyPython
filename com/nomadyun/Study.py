from functools import reduce
def f(x):
    return x*x
L = list(map(f,[1,2,3,4,5,6,7,8,9]))
print(L)

def fn(x,y):
    return x*10+y
def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
fmap = list(map(char2num, '13579'))
print(fmap)
M = reduce(fn, fmap)
print(M)