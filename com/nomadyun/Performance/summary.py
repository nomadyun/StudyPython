#usr/bin/python
# coding: utf-8
"""
Function: To get all performance testing data into 2 csv file
"""

import os
import re
import sys
import csv
import time
from libs import FPS_CSV_Report as FPSR
import shutil

fps_reports = ["IE_FPS.csv",
               "FireFox_FPS.csv",
               "Chrome_FPS.csv",
               "Safari_FPS.csv"]

def getCurTime():
    """
    :param mtime: 14 length string, e.g.'20140724185852'
    :return: "%Y-%m-%d %H:%M:%S"
    """
    mtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return mtime

def getBrowserInfo(csvfile):
    browser_info = []
    filepath = os.path.split(csvfile)
    filename = filepath[1]

    # Get the environment information
    result = re.search('(\w+)_\w+', filename)
    if result:
        for i in result.groups():
            browser_info.append(i)
    else:
        """
        Cannot get the information
        """
    # print browser_info
    return browser_info

def getfiles(rootDir):
    """
    Get all csv files from test folder, stored into a files list
    """
    filelists = []
    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:
        # for d in dirs:
        #     print os.path.join(root, d) # Get directory
        for f in files: # Get file
            filepath = os.path.join(root, f)
            # print filepath
            if filepath.endswith('csv'):
                filelists.append(filepath)
    return filelists

def getfiles_FPS_IE(files_list):
    """
    Get all FPS files list
    """
    fps_files = []
    for i in files_list:
        if 'ie_fps' in i.lower():
            fps_files.append(i)
    # print fps_files
    return fps_files

def getfiles_FPS_Firefox(files_list):
    """
    Get all FPS files list
    """
    fps_files = []
    for i in files_list:
        if 'firefox_fps' in i.lower():
            fps_files.append(i)
    # print fps_files
    return fps_files

def getfiles_FPS_Chrome(files_list):
    """
    Get all FPS files list
    """
    fps_files = []
    for i in files_list:
        if 'chrome_fps' in i.lower():
            fps_files.append(i)
    # print "FPS in Chrome", fps_files
    return fps_files

def getfiles_FPS_Safari(files_list):
    """
    Get all FPS files list
    """
    fps_files = []
    for i in files_list:
        if 'safari_fps' in i.lower():
            fps_files.append(i)
    # print fps_files
    return fps_files


def getfiles_KPI(files_list):
    """
    Get all KPI files list
    """
    kpi_files = []
    for i in files_list:
        if 'kpi' in i.lower():
            kpi_files.append(i)
    # print kpi_files
    return kpi_files

def get_FPS_report(rootDir, csvfile):
    mlist = getfiles(rootDir)
    # print mlist
    if len(mlist) == 0:
        print "Please be sure the 'tmp' folder is NOT empty!"

    csvfile = "reports/" + csvfile
    fsi = open(csvfile, 'wb')
    writer = csv.writer(fsi)

    writer.writerow(["Clip Name", "CPU Usage%"] + FPSR.patternList)
    if 'ie_fps' in csvfile.lower():
        t_list = getfiles_FPS_IE(mlist)
    elif 'firefox_fps' in csvfile.lower():
        t_list = getfiles_FPS_Firefox(mlist)
    elif 'chrome_fps' in csvfile.lower():
        t_list = getfiles_FPS_Chrome(mlist)
    elif 'safari_fps' in csvfile.lower():
        t_list = getfiles_FPS_Safari(mlist)
    else:
        print 'Cannot get any output data'

    if not t_list:
        fsi.close()
        os.remove(csvfile)
    else:
        for mfile in t_list:
            fso = open(mfile, 'rb')
            reader = csv.reader(fso)
            flag = True #Ignore the header if flag == false
            for row in reader:
                if not flag:
                    # row = getEnvironmentInfo(mfile) + row
                    writer.writerow(row)
                if 'Clip Name' in row:
                    flag = False
        fso.close()
        fsi.close()

def get_KPI_report(rootDir):
    mlist = getfiles(rootDir)
    # print mlist
    if len(mlist) == 0:
        print "Please be sure the 'tmp' folder is NOT empty!"

    kpi_reports = getfiles_KPI(mlist)
    for i in kpi_reports:
        newfile = os.path.split(i)[-1]
        shutil.copyfile(i, "reports/" + newfile)


if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     sys.exit("Error: please provide the 2 parameters: <Device ID> & <Formal Informal testing>!")

    # get all fps reports into 'reports' folder
    for report in fps_reports:
        get_FPS_report("temp/", report)

    # get all KPI reports into 'reports' folder
    get_KPI_report("temp/")


