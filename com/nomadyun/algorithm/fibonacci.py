# -*- coding: utf-8 -*- 
'''
Created on 2015年10月18日

@author: nomadyun
'''

def fibonacci(n):
#     if n < 2:
#         return n
#     else:
#         return (fibonacci(n-1) + fibonacci(n-2))
    
    terms = [0,1]
    i = 2
    while i <= n:
        terms.append(terms[i-1] + terms[i-2])
        i = i + 1 
    return terms[n]
     
    
    
    
user_input = eval(input("Please input the sequence of fobinnaci: "))
item_of_user_input = fibonacci(user_input)
print(item_of_user_input)    