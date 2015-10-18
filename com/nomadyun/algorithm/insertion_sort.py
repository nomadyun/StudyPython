# -*- coding: utf-8 -*- 
'''
Created on 2015年10月18日

@author: nomadyun
'''
my_array = [1,6,7,2,9,4]
def insertion_sort(array):
    for index in range(1,len(array)):
        value = array[index]
        i = index -1
        while i >= 0 and (value < array[i]):
            array[i+1] = array[i]
            array[i] = value
            i = i -1
    print(array)
if __name__ == '__main__':
    insertion_sort(my_array)        