@echo off
setlocal

:menu
cls
echo Select Python script to run:
echo 1. Video_Merge.py
echo 2. Video_Format.py
echo 3. Exit
echo.
echo ** No Compression will be performed in any of the scripts.
echo ** Video_Format.py only converts .ts video file to any format.
echo.
set /p choice=Enter your choice: 

if "%choice%"=="1" (
    python Video_Merge.py
) else if "%choice%"=="2" (
    python Video_Format.py
) else if "%choice%"=="3" (
    exit
) else (
    echo Invalid choice. Please select a valid option.
    timeout /t 2 >nul
    goto menu
)

endlocal

pause
