#-*- coding: utf-8 -*-
'''
Created on 2014年11月9日

@author: nomadyun
'''
import re

class Athlete:
    def __init__(self,a_name,a_dob=None,a_times=[]):
        self.name = a_name
        self.dob = a_dob
        self.times = a_times
    def top3(self):
        return(sorted(set([sanitize(i) for i in self.times]))[0:3])

def sanitize(time_string):
    clean_data = re.sub(r'[-|:]',r'.',time_string)
    return clean_data

def get_data(file_name):
    try:
        with open(file_name,'r') as f:
            data = f.readline().strip().split(',')
        return(Athlete(data.pop(0),data.pop(0),data))
    
    except IOError as err:
        print('File Error:'+ str(err))
        return None

if __name__ == '__main__':
    james = get_data('james.txt')
    print(james.name)
