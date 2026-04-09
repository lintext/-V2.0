@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

:: ============================================================
:: 桌面宠物AI - 服务停止脚本 v2.1 (修复版)
:: 功能：安全停止所有相关服务和进程
:: 修复：解决一闪而过的问题
:: ============================================================

title 桌面宠物AI - 停止服务

color 0C

set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

echo.
echo +--------------------------------------------------+
|     桌面宠物AI - 服务停止工具 v2.1                   |
+--------------------------------------------------+
echo.

echo [信息] 正在停止所有相关服务...
echo.

:: ----------------------------------------------------------
:: 停止 Electron 进程
:: ----------------------------------------------------------
echo [1/4] 正在停止 Electron 进程...
tasklist /FI "IMAGENAME eq electron.exe" 2>nul | find /I "electron.exe" >nul
if %errorlevel% equ 0 (
    taskkill /F /IM electron.exe >nul 2>&1
    if %errorlevel% equ 0 (
        echo [成功] Electron 进程已停止
    ) else (
        echo [警告] 无法停止部分Electron进程
    )
) else (
    echo [信息] Electron 未在运行
)

:: ----------------------------------------------------------
:: 停止 Python WebUI 进程
:: ----------------------------------------------------------
echo [2/4] 正在停止 Python WebUI 服务...

:: 方法1：通过命令行查找并终止
wmic process where "name='python.exe' and commandline like '%%webui%%'" get processid 2>nul | findstr /r "[0-9]" >nul
if %errorlevel% equ 0 (
    for /f "tokens=2 delims= " %%a in ('wmic process where "name='python.exe' and commandline like '%%webui%%'" get processid /value ^| findstr ProcessId') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    echo [成功] WebUI 服务已停止（通过进程名）
) else (
    :: 方法2：通过端口查找并终止
    for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":5001 " ^| findstr "LISTENING"') do (
        taskkill /F /PID %%p >nul 2>&1
        if !errorlevel! equ 0 (
            echo [成功] 已通过端口5001停止WebUI进程
            goto :webui_done
        )
    )
    :webui_done
    echo [警告] 未找到WebUI服务进程或已自动停止
)

:: ----------------------------------------------------------
:: 停止 Node.js 后台进程
:: ----------------------------------------------------------
echo [3/4] 正在停止 Node.js 后台进程...
tasklist /FI "IMAGENAME eq node.exe" 2>nul | find /I "node.exe" >nul
if %errorlevel% equ 0 (
    :: 尝试只停止本项目相关的node进程（通过标题识别）
    taskkill /F /FI "WINDOWTITLE eq WebUI-Server*" >nul 2>&1
    taskkill /F /FI "WINDOWTITLE eq Desktop-Pet*" >nul 2>&1
    
    :: 检查是否还有残留的node进程
    timeout /t 1 /nobreak >nul
    tasklist /FI "IMAGENAME eq node.exe" 2>nul | find /I "node.exe" >nul
    if !errorlevel! equ 0 (
        echo [警告] 可能存在非本项目的Node.js进程（未强制关闭）
    ) else (
        echo [成功] Node.js 进程已停止
    )
) else (
    echo [信息] Node.js 未运行项目相关进程
)

:: ----------------------------------------------------------
:: 清理临时PID文件
:: ----------------------------------------------------------
echo [4/4] 清理临时文件...
if exist "%PROJECT_ROOT%\data\service_pids.txt" (
    del /q "%PROJECT_ROOT%\data\service_pids.txt" >nul 2>&1
    echo [成功] PID记录文件已清理
) else (
    echo [跳过] 无需清理的PID文件
)

if exist "%PROJECT_ROOT%\data\webui_port.txt" (
    del /q "%PROJECT_ROOT%\data\webui_port.txt" >nul 2>&1
    echo [成功] 端口配置文件已清理
)

echo.
echo +--------------------------------------------------+
|              所有服务已停止                             |
+--------------------------------------------------+
echo.

timeout /t 3 /nobreak >nul
exit /b 0