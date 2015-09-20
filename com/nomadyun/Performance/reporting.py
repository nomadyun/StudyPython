# usr/bin/Python
# -*- coding:utf-8 -*-

from libs import FPS_UITest
from libs import FPS_CSV_Report
from libs import KPI_UITest
from libs import KPI_CSV_Report
import os
import sys
from xml.dom import minidom


global testenv_list
global testcase_list
global testset_fps
global testset_kpi
testset_fps = []
testset_kpi = []

# test environment list is formatted as:
# [test type, play mode, [browser list], [DRM_Server, test clip, scenario name, seekforward, seekbackward, bookmark]]
testenv_list = []
testcase_list = []


def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []

def get_attrvalue(node, attrname):
    return node.getAttribute(attrname) if node else ''

def parseXML(filename):
    doc = minidom.parse(filename)
    root = doc.documentElement
    launchParams_nodes = get_xmlnode(root, 'launchParams')
    varValue_list = []
    namValue_list = []

    for launchnode in launchParams_nodes:
        variable_nodes = get_xmlnode(launchnode, 'variable')
        for varnode in variable_nodes:
            var_value = get_attrvalue(varnode, 'value').strip()
            varValue_list.append(var_value)
            name_value = get_attrvalue(varnode, 'name').strip()
            namValue_list.append(name_value)
    for nam_i in range(0, len(namValue_list)):
        if namValue_list[nam_i].find("targetBuildPath") != -1:
            buildPath = varValue_list[nam_i].strip()
            testenv_list.append(buildPath)
            #print "buildPath: " + buildPath + "\n"
        elif namValue_list[nam_i].find("targetSampler") != -1:
            targetSampler = varValue_list[nam_i].strip()
            testenv_list.append(targetSampler)
            #print "targetSampler: " + targetSampler + "\n"
        elif namValue_list[nam_i].find("dll_vompEngn") != -1:
            dll_vompEngn = varValue_list[nam_i].strip()
            testenv_list.append(dll_vompEngn)
            #print "dll_vompEngn: " + dll_vompEngn + "\n"
        elif namValue_list[nam_i].find("dll_voPlugInIE") != -1:
            dll_voPlugInIE = varValue_list[nam_i].strip()
            testenv_list.append(dll_voPlugInIE)
            #print "dll_voPlugInIE: " + dll_voPlugInIE + "\n"
        elif namValue_list[nam_i].find("dll_voOSPlayer") != -1:
            dll_voOSPlayer = varValue_list[nam_i].strip()
            testenv_list.append(dll_voOSPlayer)
            #print "dll_voOSPlayer: " + dll_voOSPlayer + "\n"
        elif namValue_list[nam_i].find("volog") != -1:
            vologAdd = varValue_list[nam_i].strip()
            testenv_list.append(vologAdd)
            #print "vologAdd: " + vologAdd + "\n"
        elif namValue_list[nam_i].find("log_location") != -1:
            loglocation = varValue_list[nam_i].strip()
            testenv_list.append(loglocation)
    case_nodes = get_xmlnode(root, 'case')
    for casenode in case_nodes:
        casename = get_attrvalue(casenode,'name').strip()
        testcase_list.append(casename)
        #print "casename: " + casename + "\n"
        playermodenodes = get_xmlnode(casenode, 'playermode')
        for playermodenode in playermodenodes:
            playermode = get_attrvalue(playermodenode, 'enable').strip()
            testcase_list.append(playermode)
            #print "playermode: " + playermode + "\n"
            brow_nodes = get_xmlnode(playermodenode, 'browser')
            browser_list = []
            for brow_node in brow_nodes:
                var_nodes = get_xmlnode(brow_node, 'variable')
                for var_node in var_nodes:
                    var_node_value = get_attrvalue(var_node, 'enable').strip()
                    if var_node_value == "yes":
                        browName = get_attrvalue(var_node, 'name').strip()
                        browser_list.append(browName)
            testcase_list.append(browser_list)
            drm_nodes = get_xmlnode(playermodenode, 'DRM_Server')
            for drm_node in drm_nodes:
                drmtmp_list = []
                drmName = get_attrvalue(drm_node, 'name').strip()
                drmtmp_list.append(drmName)
                #print "drmName: " + drmName + "\n"
                clip_nodes = get_xmlnode(drm_node, 'testclip')
                for clip_node in clip_nodes:
                    clipName = get_attrvalue(clip_node, 'name').strip()
                    #ast.literal_eval(clipName)
                    drmtmp_list.append(clipName)
                    clipscenario = get_attrvalue(clip_node, 'scenario').strip()
                    drmtmp_list.append(clipscenario)
                    restartbrowser = get_attrvalue(clip_node, 'restart').strip()
                    drmtmp_list.append(restartbrowser)
                    restartinterval = get_attrvalue(clip_node, 'interval').strip()
                    drmtmp_list.append(restartinterval)
                    clipseekfor = get_attrvalue(clip_node, 'seekforward').strip()
                    drmtmp_list.append(clipseekfor)
                    clipseekbac = get_attrvalue(clip_node, 'seekbackward').strip()
                    drmtmp_list.append(clipseekbac)
                    clipbookmark = get_attrvalue(clip_node, 'bookmark').strip()
                    drmtmp_list.append(clipbookmark)
                testcase_list.append(drmtmp_list)

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

def get_testset(lst):
    flag = False
    for i in lst:
        if not flag:
            testset_fps.append(i)
            if str(i) == "kpi":
                testset_kpi.append(i)
                del testset_fps[-1]
                flag = True
        else:
            testset_kpi.append(i)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Error: Please provide configuration file!")

    # get the test data from config file
    confFile = sys.argv[1]
    parseXML(confFile)
    # print testenv_list

    # get the sampler page
    sampler_page = testenv_list[1]
    # get the log file path
    logfile = testenv_list[-1]

    # get the test set: FPS & KPI
    get_testset(testcase_list)
    # print testset_fps
    # print testset_kpi

    # FPS testing and reporting
    play_mode = testset_fps[1]
    browser_list = testset_fps[2]
    test_clips = testset_fps[3:]
    # print test_clips
    # # print samplePage, play_mode, browser_list, test_clip
    for browser_test in browser_list:
        for test_clip in test_clips:
            fps_result = FPS_UITest.executeUITest(sampler_page, browser_test, test_clip, play_mode)
            FPS_CSV_Report.get_report(logfile, fps_result)
        print "PASS: FPS Report generated for", browser_test

    # KPI testing and reporting
    browser_list = testset_kpi[2]
    test_clips = testset_kpi[3:]
    for browser_test in browser_list:
        kpi_result = KPI_UITest.executeUITest(sampler_page, browser_test, test_clips, logfile)
        KPI_CSV_Report.get_report(logfile, kpi_result)

        print "PASS: KPI Report generated for", browser_test