# -*- coding: utf-8 -*- 
'''
Created on 2015年10月17日

@author: nomadyun
'''
def factorial(number):
    if number <= 1:
        return 1
    else:
        return number*factorial(number-1)

#     product = 1
#     for i in range(number):
#         product = product * (i+1)
#     return product
    
user_input = eval(input("Enter a non-negative integer to take a factorial of: "))

factorial_of_user_input = factorial(user_input)    
print(factorial_of_user_input)