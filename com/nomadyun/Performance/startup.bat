echo off
::Close all drivers
TASKKILL /IM IEDriverServer.exe /F
TASKKILL /IM chromedriver.exe /F
::Close all browser instances
TASKKILL /IM iexplore.exe /F
::TASKKILL /IM firefox.exe /F
TASKKILL /IM chrome.exe /F
::Close the excel process
TASKKILL /IM excel.exe /F
::Remove all reports from 'temp' folder
rd temp\ /s /q
md temp
::Start testing and reporting
python reporting.py test_parameter.xml
python summary.py
::move the temporary log files into 'temp' folder
move /y KPI_log temp\
move /y KPI_log_1 temp\
pause