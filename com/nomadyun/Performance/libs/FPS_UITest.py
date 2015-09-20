# usr/bin/Python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import psutil
import sys


browser_IE = "iexplore.exe"
browser_chrome = "chrome.exe"
browser_firefox = "firefox.exe"
browser_firefox_container = "plugin-container.exe"

SHORT_TIME = 15
LONG_TIME = 60

def waitSDK_version(test_browser, wait_time):
    try:
        element = WebDriverWait(test_browser, wait_time).until(
            EC.visibility_of_element_located((By.ID, "sdkversion"))
        )
        build_num = test_browser.find_element_by_id("brandversion").text
        return build_num.split(" ")[-1]
    except:
        test_browser.close()
        sys.exit("ERROR: Cannot initiate the player, please check if it is properly installed.")

def waitPlaytime(test_browser, wait_time):
    try:
        playtime = test_browser.find_element_by_id('playTimeShow')
        play_time = playtime.get_attribute("value")
        print play_time
        time.sleep(2)
        element = WebDriverWait(test_browser, wait_time).until_not(
            EC.text_to_be_present_in_element_value((By.ID, "playTimeShow"), play_time)
        )
        if element:
            print "Test passed"
    except:
        print "Test may be failed, please check if you are still online or not"

def get_parameters(*lst):
    return lst

def get_cpu_data(browser_name):

    piece_cpu = []
    ps = psutil.get_process_list()

    for p in ps:
        if browser_name in str(p.name) or browser_firefox_container in str(p.name):
            try:
                cpu_data = p.get_cpu_percent(interval=2)
                piece_cpu.append(cpu_data)
            except:
                piece_cpu.append(0)
        else:
            continue
    piece_avg_cpu = getAverageCPUdata(piece_cpu)
    return piece_avg_cpu

def getAverageCPUdata(lst):
    total = 0.0
    for i in lst:
        total += float(i)
    return float(total)/len(lst)

def launchPage(browser_type, samplePage):
    # Launch IE and load the test page
    page_info = []

    if browser_type.lower() == "ie":
        try:
            browser = webdriver.Ie()
            browser.maximize_window()
            browserID = 1
        except:
            print "Test Failed"
            sys.exit("ERROR: Cannot open the test page, please check the browser setting.")

    # Launch FireFox and load the test page
    elif browser_type.lower() == "firefox":
        try:
            fp = webdriver.FirefoxProfile("profiles/firefox")
            browser = webdriver.Firefox(fp)
            browser.maximize_window()
            browserID = 2
        except:
            print "Test Failed"
            sys.exit("ERROR: Cannot open the test page, please check the browser setting.")

    # Launch Chrome and load the test page
    elif browser_type.lower() == "chrome":
        try:
            ch_options = Options()
            ch_options.add_argument("--ignore-certificate-errors")
            ch_options.add_argument("--start-maximized")
            ch_options.add_argument("--always-authorize-plugins")
            ch_options.add_argument("--test-type")
            browser = webdriver.Chrome(chrome_options=ch_options)
            browserID = 3
        except:
            print "Test Failed"
            sys.exit("ERROR: Cannot open the test page, please check the browser setting.")
    # Launch Safari and load the test page
    else:
        browserID = 4
        pass
        # To-do in Mac OS

    browser.get(samplePage)
    time.sleep(5)
    # assert "OnStream" in browser.title
    page_info.append(browser)
    page_info.append(browserID)

    return page_info

def playclip(browser, playmode, testedClip, browser_id):

    player = browser.find_element_by_css_selector("#p-plugin")

    inputURL = browser.find_element_by_id('clipID')
    inputURL.clear()

    testClip = "'" + testedClip[1] + "'"

    testclip = "document.getElementById('clipID').value=" + testClip
    # print testclip
    player._parent.execute_script(testclip)

    player._parent.execute_script("openClip('clipID')")

    waitPlaytime(browser, LONG_TIME)

    if playmode == "yes":
        # Full screen test
        player._parent.execute_script("fullScreen()")
    else:
        # Normal screen test
        pass

    count = 0
    cpuPercentList = []
    while True:
        # browser.refresh()
        seekBar = browser.find_element_by_id('seekbar')
        getseekWidth = seekBar.get_attribute('style')
        print getseekWidth

        if '0px' in getseekWidth or '100%' in getseekWidth:
            count += 1

        if count == 1:
            # close the browser after 15 seconds for log generation
            time.sleep(15)
            browser.quit()
            break
        else:
            if browser_id == 1:
                cpu_data = get_cpu_data(browser_IE)
            elif browser_id == 2:
                cpu_data = get_cpu_data(browser_firefox)
            elif browser_id == 3:
                cpu_data = get_cpu_data(browser_chrome)
            else:
                pass

            cpu_data = float('%0.3f' % cpu_data)
            print cpu_data
            cpuPercentList.append(cpu_data)

    avgCpuPercent = getAverageCPUdata(cpuPercentList)
    return avgCpuPercent


def executeUITest(samplePage, browser_type, testedClip, playmode):

    cpu_browser_info = []

    cpu_browser_info.append(browser_type)
    cpu_browser_info.append(testedClip[1])

    browserInfo = launchPage(browser_type, samplePage)
    mbrowser = browserInfo[0]
    mbrowserID = browserInfo[1]

    # Test the build is properly installed
    build_ver = waitSDK_version(mbrowser, SHORT_TIME)
    cpu_browser_info.append(build_ver)

    CPUPercent = playclip(mbrowser, playmode, testedClip, mbrowserID)

    cpu_browser_info.append(CPUPercent)
    waitTime = int(testedClip[4])
    print waitTime
    time.sleep(waitTime)
    return cpu_browser_info

# if __name__ == "__main__":
#     executeTest_IE(samplePage, testClip, flag)



