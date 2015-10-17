#-*- coding: utf8 -*-
'''
Created on 2014��10��21��

@author: huang_yun
'''
import re
def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    # +++your code here+++
    names_top = []
    patten_year_line = re.compile(r'<h3 align="center">Popularity\s+in\s+(\d{4})</h3>') 
    patten_year = re.compile(r'(\d{4})')
    patten_name = re.compile(r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>')
    
    with open(filename,'r') as f:
        text = f.read()
        match_line = patten_year_line.search(text)
        if match_line:
            #print match_line.group()
            year_match = patten_year.search(match_line.group())
            year = year_match.group(1)
            print(year)
            names_top.append(year)
        
        name_tuples = patten_name.findall(text)
#         print name_tuples
#         for tuple_name in name_tuples:
#             print tuple_name[0],tuple_name[1],tuple_name[2]
#         malenames_to_rank = {}
#         femalenames_to_rank = {}
        names_to_rank = {}
        for rank,male,female in name_tuples:
            if male not in names_to_rank:
                names_to_rank[male] = rank
                
            if female not in names_to_rank:
                names_to_rank[female] = rank
        #print malenames_to_rank
        #print femalenames_to_rank
        sorted_names = sorted(names_to_rank.keys())
        #sorted_female_names = sorted(femalenames_to_rank.keys())
        for name in sorted_names:
                names_top.append(name+' '+ names_to_rank[name])
        
        print(names_top)


        
            
            
if __name__ == '__main__':
    extract_names('baby1990.html')