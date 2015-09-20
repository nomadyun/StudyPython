#-*- decoding: utf-8 -*-
'''
Created on 2014年10月31日

@author: huang_yun
'''
array = [1,6,7,2,9,4]
def bubblesort(numbers):
    for j in range(len(numbers)-1,-1,-1):
        for i in range(j):
            if numbers[i]>numbers[i+1]:
                numbers[i],numbers[i+1] = numbers[i+1],numbers[i]
            print(i,j)
            print(numbers)
if __name__ == '__main__':
    bubblesort(array)