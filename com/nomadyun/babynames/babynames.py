#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

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
            #print year
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
        
        return names_top

        


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print 'usage: [--summaryfile] file [file ...]'
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]

# +++your code here+++
# For each filename, get the names, then either print the text output
# or write it to a summary file
    for filename in args:
        names_top = extract_names(filename)
        
        # Make text out of the whole list
        text = '\n'.join(names_top)

        if summary:
            outf = open(filename + '.summary', 'w')
            outf.write(text + '\n')
            outf.close()
        else:
            print text


  
if __name__ == '__main__':
    main()
