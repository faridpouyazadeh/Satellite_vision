@echo off
echo ================================================
echo          Satellite Vision Launcher
echo ================================================
echo.

:menu
echo Choose an option:
echo 1. Setup Environment (First time setup)
echo 2. Run Basic Satellite Processing
echo 3. Run Full AI Analysis
echo 4. Install Requirements Only
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto basic
if "%choice%"=="3" goto full
if "%choice%"=="4" goto install
if "%choice%"=="5" goto exit
echo Invalid choice. Please try again.
echo.
goto menu

:setup
echo.
echo Running setup...
python setup.py
echo.
pause
goto menu

:basic
echo.
echo Starting basic satellite processing...
python main_basic.py
echo.
pause
goto menu

:full
echo.
echo Starting full AI analysis...
python main_full.py
echo.
pause
goto menu

:install
echo.
echo Installing requirements...
pip install -r requirements.txt
echo.
pause
goto menu

:exit
echo.
echo Thank you for using Satellite Vision!
pause