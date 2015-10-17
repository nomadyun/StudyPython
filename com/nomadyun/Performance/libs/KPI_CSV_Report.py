# usr/bin/Python
# -*- coding:utf-8 -*-

import re
import os
import csv
import time
from collections import OrderedDict


# pattern to clean up the original log
pattern_line_URL = "(?i)OpenInternalII,\s+\d*,\s+URL:(.*)"
pattern_line_AutoTest = "(?i)\[Plugin\s+Auto\s+Test\](.*)"
pattern_line_open = "(?i)\s*(VOCommonPlayerImpl::open,\s+\d*,\s+\[Open\]\s+call\s+open\s+\@)"
pattern_line_render = "(?i)\s*(gonna\s+to\s+be\s+rendered)"
pattern_line_seek = "(?i)\s*(VOCommonPlayerImpl::SetPosition,\s+\d*,\s+\[SEEK\])"
pattern_line_switch = "(?i)\s*(voOSMediaPlayer::CommitSelection)"
pattern_line_AdaptiveStream = "(?i)\s*(\[Video\]\s+size\s+changed\s+\@)"
pattern_line_Pause = "(?i)\s*(Pause\s+Use\s+time:)"
pattern_line_Resume = "(?i)\s*(\[start\]\s+playback\s+start\s+\@)"

# pattern to parse the target data
pattern_Open = "(?i)\s*(open,\s+\d*,\s+\[Open\]\s+call\s+open)\s+\@\s+(\d*)"
pattern_Complete = "(?i)\s*(\[Audio\]\s+gonna\s+to\s+be\s+rendered\s+\@)\s+(\d*)"
pattern_Seek = "(?i)\s*(\[SEEK\]\s+\@)\s+(\d*)"
pattern_SeekComplete = "(?i)(\[SEEK\]\s+\@).*?(\[Audio\]\s+gonna\s+to\s+be\s+rendered\s+\@)\s+(\d*)"
pattern_SetAudio = "(?i)(\[Commit\s+selected\s+audio\s+\d*\s+\]\s+\@)\s+(\d*)"
pattern_SetAComplete = "(?i)(\[Commit\s+selected\s+audio\s+\d*\s+\]\s+\@).*?(\[Audio\]\s+gonna\s+to\s+be\s+rendered\s+\@)\s+(\d*)"
pattern_AdaptiveStart = "(?i)(\[Video\]\s+gonna\s+to\s+be\s+rendered\s+\@)\s+(\d*)"
pattern_AdaptiveEnd = "(?i)(\[Video\]\s+gonna\s+to\s+be\s+rendered\s+\@).*?(\[Video\]\s+size\s+changed\s+\@)\s+(\d*)"
pattern_Pause = "(?i)(Pause\s+Use\s+time):(\d*)"
pattern_ResumeStart = "(?i)(\[start\]\s+playback\s+start\s+\@)\s+(\d*)"
pattern_ResumeEnd = "(?i)\s*(\[Audio\]\s+gonna\s+to\s+be\s+rendered\s+\@)\s+(\d*)"

# -*- No event called "[Commit selected subtitle]" within log -2014/08/12
pattern_SetSubtitle = "(?i)\s*(\[Commit\s+selected\s+subtitle\s+\d+\s+\]\s+\@)\s+(\d*)"
pattern_SetSComplete = "(?i)(\[Commit\s+selected\s+subtitle\s+\d*\s+]\s+\@).*?(\[Audio\]\s+gonna\s+to\s+be\s+rendered\s+\@)\s+(\d*)"

ScenarioCol = "Test Scenario"
clipName = "Clip Name"
TimeCol = "Performance Test Result"

scenarios_log_list = [
    "Play Live TV",
    "Zapping Live TV",
    "Play VOD",
    "Seek in VOD",
    "Set Audio in VOD",
    "Set Subtitle in VOD",
    "Play VOD from bookmark",
    "Set Audio in NTS",
    "Set Subtitle in NTS",
    "Adaptive Stream Show"
]

scenarios_list = [
    "Play Live TV",
    "Zapping Live TV",
    "Play VOD",
    "Seek in VOD-Forward",
    "Seek in VOD-Backward",
    "Set Audio in VOD",
    "Set Subtitle in VOD",
    "Play VOD from bookmark",
    "Set Audio in NTS",
    "Set Subtitle in NTS",
    "Adaptive Stream Show",
    "Pause in VOD",
    "Play after Pause in VOD"
]

def sortFile(originalLog, newLog):
    """
    To generate a new log based on original log per the latter maybe too big to cause error
    NB: This is function cost much time in order to shorten the log size
    """
    fs = open(originalLog, 'rb')
    try:
        if os.path.exists(newLog):
            fs1 = open(newLog, 'a+b')
        else:
            fs1 = open(newLog, 'wb')
    except Exception as e:
        print("**********", e)

    while True:
        line = fs.readline()
        if not line:
            break
        else:
            p = re.compile(pattern_line_URL + "|" + pattern_line_open + "|" + pattern_line_render + "|" + pattern_line_seek + "|" + pattern_line_switch + "|" + pattern_line_AdaptiveStream + "|" + pattern_line_Pause + "|" + pattern_line_Resume)
            result = p.search(line)
            if result:
                # print line
                fs1.write(line)
            else:
                continue
    fs.close()
    fs1.close()

def updateFile(newLog, updatedLog):
    """
    To reverse the order of these 2 lines:
    15:19:09.037 @@@VOLOG, ... cosmpengnwrap.cpp, COSMPEngnWrap::Open, 459, [Open] @ 350015264
    15: 19:09.057 @@@VOLOG, ... voAdaptiveStreamingController::OpenInternalII, 480, URL:http://10.2.68.24/ericsson/UTC/11/index.m3u8
    """
    try:
        fsi = open(updatedLog, 'wb')
        fso = open(newLog, 'rb')
    except Exception as e:
        print("**********", e)

    t_line = ""
    sid = 0
    while True:
        line = fso.readline()
        if not line:
            break
        else:
            p1 = re.compile(pattern_line_open)
            p2 = re.compile(pattern_line_URL)

            result1 = p1.search(line)
            result2 = p2.search(line)
            if result1:
                t_line = line
                continue
            elif result2:
                fsi.write("[Plugin Auto Test]" + scenarios_log_list[sid] + os.linesep)
                fsi.write(line + t_line)
                t_line = ""
                sid += 1
            else:
                fsi.write(line)
    fso.close()
    fsi.close()

def segmentLog_URL(logfile):
    """
    Put the test data (as value) and test clip (as key) into a dictionary
    """
    segment_mark = pattern_line_URL
    tempList = []
    logDict = OrderedDict([])
    fs = open(logfile)
    increment = 0

    for line in reversed(fs.readlines()):
        tempList.append(line)
        result = re.search(segment_mark, line)
        if result:
            tempList.reverse()
            dictKey = result.group(1)
            if dictKey in list(logDict.keys()):
                increment += 1
                dictKey = dictKey + "^" + str(increment)
            logDict[dictKey] = tempList
            tempList = []
        else:
            continue
    # print logDict
    fs.close()
    mitems = list(logDict.items())
    mitems.reverse()
    return OrderedDict(mitems)

def getClips():
    dict = segmentLog_URL('KPI_log_1')
    clip_list = []
    mitems = list(dict.items())

    inc = 0
    for ky in list(OrderedDict(mitems).keys()):
        if inc == 3:
            # The test clip is used for the 2 seek operation in scenario: 'Seek in VOD'
            clip_list.append(ky.split("^")[0])
        elif inc == (len(scenarios_log_list) - 1):
            clip_list.append(ky.split("^")[0])
            clip_list.append(ky.split("^")[0])
        clip_list.append(ky.split("^")[0])
        inc += 1

    return clip_list

def segmentLog_SC(logfile):
    """
    Put the test data (as value) and test scenario (as key) into a dictionary
    """
    segment_mark = pattern_line_AutoTest
    tempList = []
    logDict = OrderedDict([])
    fs = open(logfile)

    for line in reversed(fs.readlines()):
        tempList.append(line)
        result = re.search(segment_mark, line)
        if result:
            tempList.reverse()
            dictKey = result.group(1)
            logDict[dictKey] = tempList
            tempList = []
        else:
            continue
    # print logDict
    fs.close()
    mitems = list(logDict.items())
    mitems.reverse()
    return OrderedDict(mitems)

# Get the target data
def get_list():
    result_list = []
    for k, v in list(segmentLog_SC('KPI_log_1').items()):
        # print k, v
        if str(k) in scenarios_log_list[0]:
            result1 = re.search(pattern_Open, str(v))
            result2 = re.search(pattern_Complete, str(v))
            if result1 and result2:
                # print result1.groups()
                # print result2.groups()
                # print int(result2.groups()[-1]) - int(result1.groups()[-1])
                result_list.append(int(result2.groups()[-1]) - int(result1.groups()[-1]))
            else:
                result_list.append(None)
                result_list.append(None)

        elif str(k) in scenarios_log_list[1]:
            result1 = re.search(pattern_Open, str(v))
            result2 = re.search(pattern_Complete, str(v))
            if result1 and result2:
                # print result1.groups()
                # print result2.groups()
                # print int(result2.groups()[-1]) - int(result1.groups()[-1])
                result_list.append(int(result2.groups()[-1]) - int(result1.groups()[-1]))
            else:
                result_list.append(None)

        elif str(k) in scenarios_log_list[2]:
            result1 = re.search(pattern_Open, str(v))
            result2 = re.search(pattern_Complete, str(v))
            if result1 and result2:
                # print result1.groups()
                # print result2.groups()
                # print int(result2.groups()[-1]) - int(result1.groups()[-1])
                result_list.append(int(result2.groups()[-1]) - int(result1.groups()[-1]))
            else:
                result_list.append(None)

        elif str(k) in scenarios_log_list[3]:
            result1 = re.findall(pattern_Seek, str(v))
            result2 = re.findall(pattern_SeekComplete, str(v), re.S)
            if result1 and result2:
                # print result1
                # print result2
                # print int(result2[0][-1]) - int(result1[0][-1])
                # print int(result2[1][-1]) - int(result1[1][-1])
                result_list.append(int(result2[0][-1]) - int(result1[0][-1]))
                result_list.append(int(result2[1][-1]) - int(result1[1][-1]))
            else:
                result_list.append(None)
                result_list.append(None)

        elif str(k) in scenarios_log_list[4]:
            result1 = re.search(pattern_SetAudio, str(v))
            result2 = re.search(pattern_SetAComplete, str(v))
            if result1 and result2:
                # print result1.groups()
                # print result2.groups()
                # print int(result2.groups()[-1]) - int(result1.groups()[-1])
                result_list.append(int(result2.groups()[-1]) - int(result1.groups()[-1]))
            else:
                result_list.append(None)

        elif str(k) in scenarios_log_list[5]:
            result1 = re.search(pattern_SetSubtitle, str(v))
            result2 = re.search(pattern_SetSComplete, str(v))
            if result1 and result2:
                # print result1.groups()
                # print result2.groups()
                # print int(result2.groups()[-1]) - int(result1.groups()[-1])
                result_list.append(int(result2.groups()[-1]) - int(result1.groups()[-1]))
            else:
                result_list.append(None)

        elif str(k) in scenarios_log_list[6]:
            result1 = re.search(pattern_Seek, str(v))
            result2 = re.search(pattern_SeekComplete, str(v), re.S)
            if result1 and result2:
                # print result1.groups()
                # print result2.groups()
                # print int(result2.groups()[-1]) - int(result1.groups()[-1])
                result_list.append(int(result2.groups()[-1]) - int(result1.groups()[-1]))
            else:
                result_list.append(None)

        elif str(k) in scenarios_log_list[7]:
            result1 = re.search(pattern_SetAudio, str(v))
            result2 = re.search(pattern_SetAComplete, str(v), re.S)
            if result1 and result2:
                # print result1.groups()
                # print result2.groups()
                # print int(result2.groups()[-1]) - int(result1.groups()[-1])
                result_list.append(int(result2.groups()[-1]) - int(result1.groups()[-1]))
            else:
                result_list.append(None)

        elif str(k) in scenarios_log_list[8]:
            result1 = re.search(pattern_SetSubtitle, str(v))
            result2 = re.search(pattern_SetSComplete, str(v))
            if result1 and result2:
                # print result1.groups()
                # print result2.groups()
                # print int(result2.groups()[-1]) - int(result1.groups()[-1])
                result_list.append(int(result2.groups()[-1]) - int(result1.groups()[-1]))
            else:
                result_list.append(None)

        else:
            result1 = re.search(pattern_AdaptiveStart, str(v))
            result2 = re.search(pattern_AdaptiveEnd, str(v), re.S)
            if result1 and result2:
                # print result1.groups()[-1]
                # print result2.groups()[-1]
                # print int(result2.groups()[-1]) - int(result1.groups()[-1])
                result_list.append(int(result2.groups()[-1]) - int(result1.groups()[-1]))
            else:
                result_list.append(None)

            result1 = re.search(pattern_Pause, str(v))
            result2 = re.findall(pattern_ResumeStart, str(v))
            result3 = re.findall(pattern_ResumeEnd, str(v))
            if result1 and result2 and result3:
                # print result1.groups()[-1]
                # print result2.groups()[-1]
                # print result3.groups()[-1]
                # print int(result2[0][-1]) - int(result1[0][-1])
                # print int(result2[1][-1]) - int(result1[1][-1])
                result_list.append(int(result1.groups()[-1]))
                result_list.append(int(result3[1][-1]) - int(result2[1][-1]))
            else:
                result_list.append(None)
                result_list.append(None)

    return result_list

def getCurTime():
    mtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return mtime

def get_report(original_log, kpi_result):

    # Update the log
    updateFile('KPI_log', 'KPI_log_1')

    # Get the results: scenarios (as scenarios_list), test clips, time records
    clips = getClips()
    records = get_list()

    res_list = []
    res_list.append(scenarios_list)
    res_list.append(clips)
    res_list.append(records)
    # print res_list

    res_list = list(map(list, list(zip(*res_list))))
    # print res_list

    # write result to CSV file
    new_dir = "temp/" + kpi_result[1] + "/" + getCurTime()
    os.makedirs(new_dir)
    csv_name = new_dir + "/" + str(kpi_result[0]) + "_KPI.csv"
    csvfile = file(csv_name, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow([ScenarioCol] + [clipName] + [TimeCol])

    for i in res_list:
        writer.writerow(i)

    csvfile.close()

    # delete the temporary log after report is generated
    os.remove("KPI_log")

# if __name__ == "__main__":
#
#     # from KPI_UITest import executeTest_IE
#     # executeTest_IE()
#
    # logfile1 = "C:/ProgramData/VisualOn/BrowserPlugin/volog.log"
    # get_report(logfile1, ["Chrome", "3.13.0.7028"])
    # print get_list()
