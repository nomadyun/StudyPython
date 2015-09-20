#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands


"""Copy Special exercise
"""
patten_files = re.compile(r'\w+_\w+_.\w{3}')


# +++your code here+++
# Write functions and modify main() to call them

def get_special_paths(dirname):
    all_files = []
    file_names = os.listdir(dirname)
    for filename in file_names:
        match = patten_files.search(filename)
        if match:
            file_rel_path = os.path.join(dirname,filename)
            file_abs_path = os.path.abspath(file_rel_path)
            all_files.append(file_abs_path)
    print all_files
            
def copy_to(paths,to_dir):
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    for path in paths:
        file_name = os.path.basename(path)
        shutil.copy(path,os.path.join(to_dir,file_name))
    
def zip_to(paths,zippath):
    zip_prog = r'C:\Program Files\7-Zip\7z.exe'
    cmd = zip_prog +' b'+' '+zippath+' '+'.join(paths)'
    print "Command I'm going to do:" + cmd
    (status, output) = commands.getstatusoutput(cmd)
    # If command had a problem (status is non-zero),
    # print its output to stderr and exit.
    if status:
        sys.stderr.write(output)
        sys.exit(1)

def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print "error: must specify one or more dirs"
        sys.exit(1)
    
    paths = []
    for dirname in args:
        paths.extend(get_special_paths(dirname))
# +++your code here+++
# Call your functions
    if todir:
        copy_to(paths, todir)
    elif tozip:
        zip_to(paths, tozip)
    else:
        print '\n'.join(paths)
        
if __name__ == "__main__":
    main()
