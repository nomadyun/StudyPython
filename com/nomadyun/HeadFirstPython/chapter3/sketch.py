#-*- coding: UTF-8 -*-
'''
Created on 2014年10月25日

@author: nomadyun
'''
Man_Says = []
Other_Says = []

try:
    with open('sketch.txt','r') as data:
        for each_line in data:
            try:
                (role,line_spoken) = each_line.split(':',1)
                line_spoken = line_spoken.strip()
                if role == 'Man':
                    Man_Says.append(line_spoken)
                else:
                    Other_Says.append(line_spoken)         
            except ValueError:
                pass                
except IOError as err:   
    print('File error:' + str(err))


try:
    with open('man_out.txt','w') as man_out:
        man_out.write('\n'.join(Man_Says))
    
    with open('other_out.txt','w') as other_out:   
        other_out.write('\n'.join(Other_Says))    

except IOError as err:
    print('Can not open the file:' + str(err))
    

if __name__ == '__main__':
    pass