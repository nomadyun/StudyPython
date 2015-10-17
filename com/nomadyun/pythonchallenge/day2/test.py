#-*- coding:utf-8 -*-
'''
Created on 2014年10月28日

@author: huang_yun
'''
s = ''.join([line.rstrip() for line in open('ocr.txt')])    
occurrences = {}
for c in s: 
    occurrences[c] = occurrences.get(c, 0) + 1
avgOC = len(s) // len(occurrences)
print(''.join([c for c in s if occurrences[c] < avgOC]))     

if __name__ == '__main__':
    pass