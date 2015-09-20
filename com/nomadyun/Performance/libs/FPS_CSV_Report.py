# usr/bin/Python
# -*- coding:utf-8 -*-

import re
import os
import csv
import sys
import time


pattern_AutoTest = "(?i)\[Plugin\s+Auto\s+Test\](.*)"
pattern_FPS = "(?i)\s*(voCMediaPlayer::ShowResult)*?(Video\s+Frames)\s+(\d*),\s+(\d*)\s+(\d*)\s+(\d*)"

patternDic = {
    "FPS" : pattern_FPS
}

patternList = [
    "Decoder FPS",
    "Render FPS",
]

clipName = "Clip Name"
CPU_AvgPercentage = "CPU Usage%"

def createFile(originalLog, newLog):
    """
    To generate a new log based on original log per the latter maybe to big to cause error
    """
    if not os.path.exists(originalLog):
        sys.exit("ERROR: cannot find the log file, please confirm the dll/cfg files are correctly located.")

    fs = open(originalLog, 'rb')
    try:
        fs1 = open(newLog, 'wb')
    except Exception as e:
        print "**********", e

    fs1.write("[Plugin Auto Test]FPS")
    while True:
        line = fs.readline()
        if not line:
            break
        else:
            key_word = "(?i)\s*voCMediaPlayer::ShowResult"
            result = re.findall(key_word, line)
            if result:
                # print line
                fs1.write(line)
            else:
                continue
    fs.close()
    fs1.close()

def segmentLog(logfile):
    segment_mark = pattern_AutoTest
    #Store the log in a playback session
    tempList = []
    logDict = {}
    fs = open(logfile)
    for line in reversed(fs.readlines()):
        tempList.append(line)
        result = re.search(segment_mark, line)
        if result:
            # tempList.reverse()
            temp = ''.join(tempList)

            logDict[result.group(1)] = temp
            tempList = []
        else:
            continue
    # print logDict
    fs.close()
    return logDict

def text2list(log_file, testclip, cpuInfo):
    content = segmentLog(log_file)
    segmentList = []

    # k: link name
    # v: related log message of this link
    for k, v in content.items():
        tempList = []
        tempList.append(str(testclip))
        tempList.append(str(cpuInfo))

        result = re.findall(pattern_FPS, str(v))
        if result:
            decoderSum = 0.0
            renderSum = 0.0
            length = 100 * len(result)
            for i in result:
                decoderSum += int(i[-2])
                renderSum += int(i[-1])
            print float(decoderSum)/length, float(renderSum)/length
            # Decoder FPS
            tempList.append(round(decoderSum/length, 2))
            # Render FPS
            tempList.append(round(renderSum/length, 2))
        else:
            tempList.append(None)
            print "Data missing error(FPS): Please check the log file."
        segmentList.append(tempList)
        print segmentList
    return segmentList

def getCurTime():
    mtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return mtime

def get_report(original_log, fps_result):
    logfile = "Log_FPS"
    createFile(original_log, logfile)

    # write result to CSV file
    new_dir = "temp/" + fps_result[2] + "/" + getCurTime()
    os.makedirs(new_dir)
    csv_name = new_dir + "/" + str(fps_result[0]) + "_FPS.csv"

    # if os.path.exists(csv_name):
    #     csv_name = csv_name.split("_")[0] + "FPS_1.csv"

    csvfile = file(csv_name, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow([clipName] + [CPU_AvgPercentage] + patternList)

    line_list = text2list(logfile, fps_result[1], fps_result[-1])
    for i in line_list:
        writer.writerow(i)
    csvfile.close()
    # To-do: Move file into result folder

# if __name__ == "__main__":
#
#     # from KPI_UITest import executeTest_IE
#     # executeTest_IE()
#
#
#     logfile1 = r"C:/ProgramData/VisualOn/BrowserPlugin/volog.log"
#     get_report(logfile1, ['ie', "test clip file", "3.0128", "5.345"])
