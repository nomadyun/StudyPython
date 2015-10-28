# -*- coding: utf-8 -*- 
'''
Created on 2015年10月22日

@author: nomadyun
'''
# hail_list = []
# lengh = 0
def hailstone(n):
#     global hail_list,lengh
#     hail_list.append(n)
#     lengh = lengh + 1
#  
#     if n <= 1:
#         n = 1 
#     elif n%2 == 0:
#         hailstone(int(n/2))
#     else:
#         hailstone(int(3*n+1))
    hail_list = []
    lengh = 0
    while(n >= 1):
        hail_list.append(n)
        lengh = lengh + 1
        if n == 1:
            n = 1
            break
        elif n % 2 == 0:
            n = int(n/2)
        else:
            n = int(n*3+1)
    return hail_list,lengh

user_input = eval(input("Please input a integer number: "))

print(hailstone(user_input))
        