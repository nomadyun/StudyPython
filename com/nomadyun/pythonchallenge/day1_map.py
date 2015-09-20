#-*- coding: UTF-8 -*-
'''
Created on 2014年10月25日

@author: nomadyun
'''
import sys
string = '''g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb
        gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb.
                    lmu ynnjw ml rfc spj.'''
url_str = 'map'  
list_a = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def f(a):
    if list_a.index(a) < len(list_a)-2:
        alpha =  list_a[list_a.index(a)+2]      
    else:       
        alpha = list_a[list_a.index(a)-24]
    return alpha

def out_put(strs):
    list_new = map(f,list_a)
    for x in strs:
        if x.isalpha():
            x_new = list_new[list_a.index(x)]
        else:
            x_new = x
        sys.stdout.write(x_new)  

    '''
    table = string.maketrans(string.ascii_lowercase,string.ascii_lowercase[2:]+string.ascii_lowercase[:2])
    string.translate(table)
    '''

if __name__ == '__main__':
    out_put(string)
    print '\n'
    out_put(url_str)  

