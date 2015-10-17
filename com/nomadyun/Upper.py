# -*- coding: utf-8 -*-
'''
Created on 2014年10月18日

@author: nomadyun
'''
def copy():
    try:
        inputFile = open('small.txt','r')
    except IOError:
        print('Open File failed.')
    outputFile = open('upper.txt','w')
    lineList = inputFile.readlines()
    for line in lineList:
        for s in line:
            newS = s.upper()
            outputFile.write(newS)
    inputFile.close()
    outputFile.flush()
    outputFile.close()
if __name__ == '__main__':
        copy()

    
    
    