# usr/bin/Python
# -*- coding:utf-8 -*-


from . import KPI_CSV_Report as report
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from winreg import *

# wait for 20 second
SHORT_TIME = 20
# wait for 60 second
LONG_TIME = 60


def waitPlaytime(wait_time):
    try:
        playtime = browser.find_element_by_id("playTimeShow")
        play_time = playtime.get_attribute("value")
        print(play_time)
        time.sleep(1)
        element = WebDriverWait(browser, wait_time).until_not(
            EC.text_to_be_present_in_element_value((By.ID, "playTimeShow"), play_time)
        )
        if element:
            print("Test passed")
    except Exception as e:
        print(e)
        print("Test may be failed, please check if you are still online or not")

def waitSDK_version(wait_time):
    try:
        element = WebDriverWait(browser, wait_time).until(
            EC.visibility_of_element_located((By.ID, "sdkversion"))
        )
        if element:
            """
            Can find the ID: sdkversion
            """
        build_num = browser.find_element_by_id("brandversion").text
        return build_num.split(" ")[-1]
    except Exception as e:
        print(e)
        browser.close()
        sys.exit("ERROR: Cannot initiate the player, please check if it is properly installed.")

def switchServer(new_srv="public-ott-nodrm.verimatrix.com:80"):
    # Update test clip server by changing the regedit:
    # [HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\VisualOn\BrowserPlugin\DRMVerification\Verimatrix]
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE,
                      "Software\\Wow6432Node\\VisualOn\\BrowserPlugin\\DRMVerification\\Verimatrix",
                      0, KEY_ALL_ACCESS)
        old_srv = QueryValueEx(key, 'server')[0]
        if old_srv != new_srv:
            SetValueEx(key, 'server', 0, REG_SZ, new_srv)
            print("The new DRM server is:", QueryValueEx(key, 'server')[0])
            # Test page need a refresh
            return True
        else:
            # Test page doesn't need a refresh
            return False

    except Exception as e:
        print("Error in updating the DRM server:", e)

    finally:
        key.Close()

def launchPage(browser_type, samplePage):

    page_info = []
    global browser

    if browser_type.lower() == "ie":
        try:
            browser = webdriver.Ie()
            browser.maximize_window()
            browserID = 1
        except:
            print("Test Failed")
            sys.exit("ERROR: Cannot open the test page, please check the browser setting.")

    # Launch FireFox and load the test page
    elif browser_type.lower() == "firefox":
        try:
            fp = webdriver.FirefoxProfile("profiles/firefox")
            browser = webdriver.Firefox(fp)
            browser.maximize_window()
            browserID = 2
        except:
            print("Test Failed")
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
            time.sleep(2)
        except:
            print("Test Failed")
            sys.exit("ERROR: Cannot open the test page, please check the browser setting.")
    # Launch Safari and load the test page
    else:
        pass
        browserID = 4
        # To-do in Mac OS

    browser.get(samplePage)
    assert "OnStream" in browser.title
    build_ver = waitSDK_version(SHORT_TIME)
    
    # wait for the DRM stuff registered
    time.sleep(10)

    # page_info.append()
    page_info.append(browserID)
    page_info.append(build_ver)

    return page_info

def testPause():
    browser.execute_script("voplayer.pause()")
    time.sleep(5)

def testResume():
    browser.execute_script("voplayer.play()")
    time.sleep(5)

def getPlayer():
    try:
        mplayer = browser.find_element_by_css_selector("#p-plugin")
    except Exception as e:
        print("Fatal Error: Cannot get the player", e)
    return mplayer

def setOffset(offset):
    browser.find_element_by_id("offset").clear()
    player = getPlayer()
    player._parent.execute_script("document.getElementById('offset').value=\'" + offset + "\'")
    player._parent.execute_script("setOffsetValue('offset')")
    print("offset is set to: %s" % offset)

def resetOffset():
    browser.find_element_by_id("offset").clear()
    player = getPlayer()
    player._parent.execute_script("document.getElementById('offset').value=\'0'")
    player._parent.execute_script("setOffsetValue('offset')")

def playClip(testclip, logfile, browser_type, samplePage):
    """
    play test clip
    """
    print("scenario:", testclip[2])

    # restart the browser if the test scenario requests
    if testclip[3] == "yes":
        browser.close()
        time.sleep(int(testclip[4]))

        # get log
        report.sortFile(logfile, "KPI_log")
        print("Target log file updated")

        launchPage(browser_type, samplePage)

    # refresh the browser if DRM server request a change
    elif switchServer(testclip[0]):
        browser.refresh()
        time.sleep(5)

    # play test clip
    player = getPlayer()
    # get the bookmark
    offset_value = int(testclip[-1])
    if offset_value != 0:
        setOffset(testclip[-1])
    else:
        resetOffset()
    testdata = "'" + testclip[1] + "'"
    clip = "document.getElementById('clipID').value=" + testdata
    player._parent.execute_script(clip)
    time.sleep(1)
    player._parent.execute_script("openClip('clipID')")

    waitPlaytime(SHORT_TIME)
    time.sleep(5)
    return player

def testSeek(testclip, logfile, browser_type, samplePage):

    SEEK_POSITION_Forward = testclip[-3]
    SEEK_POSITION_backword = testclip[-2]

    player = playClip(testclip, logfile, browser_type, samplePage)

    # Seek - First Time
    player._parent.execute_script("voplayer.setPosition(\'" + SEEK_POSITION_Forward + "\')")
    position = player._parent.execute_script("return voplayer.getPosition()")
    print("The current position is:", position)

    # Wait for the play time changes
    waitPlaytime(LONG_TIME)
    time.sleep(5)

    # Seek - Second Time
    player._parent.execute_script("voplayer.setPosition(\'" + SEEK_POSITION_backword + "\')")
    position = player._parent.execute_script("return voplayer.getPosition()")
    print("The current position is:", position)

    waitPlaytime(LONG_TIME)
    time.sleep(5)

def testAudio(testclip, logfile, browser_type, samplePage):

    player = playClip(testclip, logfile, browser_type, samplePage)

    audioCount = player._parent.execute_script("return voplayer.getAudioCount()")
    print("Audio Stream Amount is %d" % audioCount)

    # select audio stream (the last one)
    if audioCount > 1:
        audioCount -= 1
        player._parent.execute_script("voplayer.selectAudio(\'" + str(audioCount) + "\')")
    else:
        print("Invalid Test Clip: Only one audio stream in this clip!")

    # commit selection
    player._parent.execute_script("commitSelection()")

    waitPlaytime(LONG_TIME)
    time.sleep(5)
    print("audio stream was changed")

def testSubtitle(testclip, logfile, browser_type, samplePage):

    player = playClip(testclip, logfile, browser_type, samplePage)

    # count the subtitle
    subtitleCount = player._parent.execute_script("return voplayer.getSubtitleCount()")
    print("Subtitle Stream Amount is %d" % subtitleCount)

    # select subtitle stream (the last one)
    if subtitleCount > 1:
        subtitleCount -= 1
        player._parent.execute_script("voplayer.selectSubtitle(\'" + str(subtitleCount) + "\')")
    else:
        print("Invalid Test Clip: Only one subtitle stream in this clip!")

    # commit selection
    player._parent.execute_script("commitSelection()")

    waitPlaytime(LONG_TIME)
    time.sleep(5)
    print("subtitle stream was changed")

def testAdaptiveStream(testclip, logfile, browser_type, samplePage):
    # include 3 test scenario in this function: 1) Adaptive stream show, 2) Pause, 3) Resume
    player = playClip(testclip, logfile, browser_type, samplePage)

    # Adaptive stream show
    count = 0
    while count < 4:
        time.sleep(5)
        log = browser.find_element_by_id("showlog").get_attribute('value')

        if "VO_OSMP_CB_VIDEO_SIZE_CHANGED" in log:
            count += 1
        else:
            continue
    # Pause
    testPause()

    # Reset
    testResume()

def executeUITest(samplePage, browser_type, testClips, logfile):

    kpi_info = []
    kpi_info.append(browser_type)

    pageInfo = launchPage(browser_type, samplePage)

    kpi_info.append(pageInfo[-1])

    # Play Live TV
    test_clip = testClips[0]
    playClip(test_clip, logfile, browser_type, samplePage)

    # Live TV Zapping
    test_clip = testClips[1]
    playClip(test_clip, logfile, browser_type, samplePage)

    # Play VOD
    test_clip = testClips[2]
    playClip(test_clip, logfile, browser_type, samplePage)

    # Seek in VOD: Forward & Backward
    test_clip = testClips[3]
    testSeek(test_clip, logfile, browser_type, samplePage)

    # Set Audio in VOD
    test_clip = testClips[4]
    testAudio(test_clip, logfile, browser_type, samplePage)

    # Set Subtitle in VOD
    test_clip = testClips[5]
    testSubtitle(test_clip, logfile, browser_type, samplePage)

    # Play VOD from bookmark
    test_clip = testClips[6]
    playClip(test_clip, logfile, browser_type, samplePage)

    # Set Audio in NTS
    test_clip = testClips[7]
    testAudio(test_clip, logfile, browser_type, samplePage)

    # Set Subtitle in NTS
    test_clip = testClips[8]
    testSubtitle(test_clip, logfile, browser_type, samplePage)

    # Adaptive Steam Show
    test_clip = testClips[9]
    testAdaptiveStream(test_clip, logfile, browser_type, samplePage)

    print("Success: Test passed")

    browser.close()

    time.sleep(15)

    report.sortFile(logfile, "KPI_log")

    return kpi_info

# if __name__ == "__main__":
#     testcollection = listt[3:]
#     sample = "file:///D:/MyProjects/Plug-In/Sample/window/SamplePlayer.html"
#     logf = "C:/ProgramData/VisualOn/BrowserPlugin/volog.log"
#     executeUITest(sample, "chrome", testcollection, logf)