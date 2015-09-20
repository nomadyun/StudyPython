::set variables
set installer="EricssonBrowserPlugin.msi"
set build_location="\\fs\Development\Build\main\daily\71895\windows\app\debug\EricssonBrowserPlugin.msi"
set install_location="C:\ProgramData\VisualOn\BrowserPlugin\"
set cfg_file="\\fs\Public\AutomationTest\PerformanceTest\Plug-in\Development\cfg_file\volog.cfg"
set vompEngnDLL_location="\\fs\Development\Build\main\daily\71895\windows\lib\debug\vompEngn.Dll"
set voPlugInIEDLL_location="\\fs\Development\Build\main\daily\71895\windows\lib\debug\voPlugInIE.dll"
set voOSPlayerDLL_location="\\fs\Development\Build\main\daily\71895\windows\lib\debug\voOSPlayer.dll"
::echo %build_location%
::echo %cfg_file%
::echo %vompEngnDLL_location%
::echo %voPlugInIEDLL_location%
::echo %install_location%
::echo %voOSPlayerDLL_location%

::copy build file and installation
echo f|xcopy %build_location% %installer% /y /i
msiexec /uninstall %installer% /quiet
timeout 2
msiexec /package %installer% /quiet
timeout 2

::copy test files
xcopy %cfg_file% %install_location% /i /y
xcopy %vompEngnDLL_location% %install_location% /i /y
::For IE testing
xcopy %voPlugInIEDLL_location% %install_location% /i /y
::For Chrome/Firefox testing
xcopy %voOSPlayerDLL_location% %install_location% /i /y

echo installation completed!

exit


