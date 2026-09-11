@echo off
setlocal
where py >nul 2>nul
if not errorlevel 1 goto use_py
where python >nul 2>nul
if not errorlevel 1 goto use_python
echo Python 3.9 or newer is required. Install Python from https://www.python.org/downloads/
echo Then run this file again.
pause
exit /b 1
:use_py
py -3 "%~dp0build.py" %*
goto finished
:use_python
python "%~dp0build.py" %*
:finished
set PB_BUILD_RESULT=%errorlevel%
if not "%PB_BUILD_RESULT%"=="0" echo Build failed. Read the error above.
pause
exit /b %PB_BUILD_RESULT%
