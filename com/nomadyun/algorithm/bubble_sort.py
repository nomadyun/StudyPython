#-*- decoding: utf-8 -*-
'''
Created on 2014年10月31日

@author: huang_yun
'''
my_list = [1,6,7,2,9,4]
def bubblesort(array):
    for j in range(len(array)-1,-1,-1):
        for i in range(j):
            if array[i]>array[i+1]:
                array[i],array[i+1] = array[i+1],array[i]
    print(array)
if __name__ == '__main__':
    bubblesort(my_list)