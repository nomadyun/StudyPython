#-*- coding: UTF-8 -*-
'''
Created on 2014年10月27日

@author: nomadyun
'''

def char_count_dict(filename):
    char_count = {}
    try:
        file_input = open(filename,'r')
    except IOError:
        print('Fail to open the file.')
    else:
        for line in file_input:
            x = 0
            while(x<len(line)):              
                char = line[x]
                if not char in char_count:
                    char_count[char] = 1
                else:
                    char_count[char] = char_count[char] + 1
                x = x +1       
    file_input.close()
    return char_count
    
def print_chars(filename):
    char_count = char_count_dict(filename)
    chars = sorted(char_count.keys())
    for char in chars:
        print(char,char_count[char]) 

if __name__ == '__main__':
    print_chars('ocr.txt')