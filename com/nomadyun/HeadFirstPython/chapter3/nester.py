#-*- coding: UTF-8 -*- 
'''
Created on 2014年10月24日

@author: huang_yun
'''

import sys
movies = ['The Holy Grail',1975,'Terry Jones & Terry Gilliam',1991,
                'Graham Chapman',
                    ['Michael palin','John Cleese',['Terry Gilliam','Eric Idle','Terry Johns']],1999]

def print_lol(the_list,intend=False,level=0,fn=sys.stdout):
    for item in the_list:
        if isinstance(item,list):
            print_lol(item,intend,level+1,fn)
        else:
            if intend:
                for tab_stop in range(level):
                    print('\t',end=" ",file=fn)
            print(item,file=fn)

if __name__ == '__main__':
    print_lol(movies)
    print('\n')
    print_lol(movies,True)
    print('\n')
    print_lol(movies,True,1)
