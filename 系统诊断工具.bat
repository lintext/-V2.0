@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

:: ============================================================
:: 桌面宠物AI - 系统诊断工具 v2.1 (修复版)
:: 功能：检查系统环境、依赖状态、服务运行情况
:: 修复：解决一闪而过的问题
:: ============================================================

title 桌面宠物AI - 系统诊断工具

color 0E

set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

echo.
echo +--------------------------------------------------+
|        桌面宠物AI - 系统诊断工具 v2.1                 |
+--------------------------------------------------+
echo.

:: 创建诊断报告文件
set "DIAG_REPORT=%PROJECT_ROOT%\system_diagnosis_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%.txt"

(
    echo ========================================
    echo   桌面宠物AI - 系统诊断报告
    echo ========================================
    echo 生成时间: %date% %time%
    echo 操作系统: %OS%
    echo 用户: %USERNAME%
    echo 计算机名: %COMPUTERNAME%
    echo.
) > "%DIAG_REPORT%"

:: ============================================================
:: 1. 操作系统信息
:: ============================================================
echo [1/7] 检查操作系统信息...

ver | findstr /I "10.0" >nul && set OS_VER=Windows 10/11
ver | findstr /I "6.3" >nul && set OS_VER=Windows 8.1
ver | findstr /I "6.1" >nul && set OS_VER=Windows 7

if not defined OS_VER set OS_VER=未知版本

echo [信息] 操作系统: %OS_VER%
echo [信息] 架构: %PROCESSOR_ARCHITECTURE%

(
    echo [操作系统]
    echo 版本: %OS_VER%
    echo 架构: %PROCESSOR_ARCHITECTURE%
    echo.
) >> "%DIAG_REPORT%"

echo.

:: ============================================================
:: 2. Python环境检查
:: ============================================================
echo [2/7] 检查Python环境...

python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do (
        echo [OK] Python 已安装 - 版本: %%v
        echo        路径: 
        where python
        
        (
            echo [Python环境]
            echo 状态: 已安装
            echo 版本: %%v
            echo 路径:
        ) >> "%DIAG_REPORT%"
        
        where python >> "%DIAG_REPORT%" 2>&1
        
        :: 检查关键库
        echo.
        echo        检查Python依赖库...
        (
            echo.
            echo Python库:
        ) >> "%DIAG_REPORT%"
        
        for %%l in (flask requests numpy pillow) do (
            python -c "import %%l" >nul 2>&1
            if !errorlevel! equ 0 (
                echo       [已安装] %%l
                echo       [OK] %%l >> "%DIAG_REPORT%"
            ) else (
                echo       [未安装] %%l
                echo       [缺失] %%l >> "%DIAG_REPORT%"
            )
        )
    )
) else (
    echo [错误] Python 未安装或未添加到PATH
    
    (
        echo [Python环境]
        echo 状态: 未安装
        echo 建议: 请安装Python并添加到PATH环境变量
        echo 下载地址: https://www.python.org/downloads/
        echo.
    ) >> "%DIAG_REPORT%"
)

echo.

:: ============================================================
:: 3. Node.js环境检查
:: ============================================================
echo [3/7] 检查Node.js环境...

node --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=1" %%v in ('node --version') do (
        echo [OK] Node.js 已安装 - 版本: %%v
        
        npm --version >nul 2>&1
        if !errorlevel! equ 0 (
            for /f "tokens=1" %%n in ('npm --version') do (
                echo [OK] npm 已安装 - 版本: %%n
            )
        ) else (
            echo [警告] npm 可能未正确安装
        )
        
        (
            echo [Node.js环境]
            echo Node.js: 已安装 ^(版本: %%v^)
            echo 路径: 
        ) >> "%DIAG_REPORT%"
        
        where node >> "%DIAG_REPORT%" 2>&1
    )
) else (
    echo [错误] Node.js 未安装或未添加到PATH
    
    (
        echo [Node.js环境]
        echo 状态: 未安装
        echo 建议: 请安装Node.js并添加到PATH环境变量
        echo 下载地址: https://nodejs.org/
        echo.
    ) >> "%DIAG_REPORT%"
)

echo.

:: ============================================================
:: 4. 项目文件完整性检查
:: ============================================================
echo [4/7] 检查项目文件完整性...

set MISSING_FILES=0
set MISSING_DIRS=0

(
    echo [项目文件检查]
) >> "%DIAG_REPORT%"

:: 检查必要文件
echo        必要文件:
set "REQUIRED_FILES=config.json package.json main.js index.html app.js go.bat 一键启动.bat"
for %%f in (%REQUIRED_FILES%) do (
    if exist "%PROJECT_ROOT%\%%f" (
        echo       [存在] %%f
        echo       [OK] %%f >> "%DIAG_REPORT%"
    ) else (
        echo       [缺失] %%f - 重要！
        echo       [缺失] %%f >> "%DIAG_REPORT%"
        set /a MISSING_FILES+=1
    )
)

:: 检查必要目录
echo.
echo        必要目录:
set "REQUIRED_DIRS=webui js css libs 2D data plugins mcp"
for %%d in (%REQUIRED_DIRS%) do (
    if exist "%PROJECT_ROOT%\%%d" (
        echo       [存在] %%d\
        echo       [OK] %%d\ >> "%DIAG_REPORT%"
    ) else (
        echo       [缺失] %%d\ - 重要！
        echo       [缺失] %%d\ >> "%DIAG_REPORT%"
        set /a MISSING_DIRS+=1
    )
)

echo.
if %MISSIVE_FILES% equ 0 if %MISSIVE_DIRS% equ 0 (
    echo [成功] 项目文件完整！
) else (
    echo [警告] 发现 %MISSING_FILES% 个缺失文件，%MISSING_DIRS% 个缺失目录
)

echo.

:: ============================================================
:: 5. 服务端口检查
:: ============================================================
echo [5/7] 检查服务端口占用情况...

(
    echo [服务端口检查]
) >> "%DIAG_REPORT%"

set "PORTS=5001 9001 9002 3000"
for %%p in (%PORTS%) do (
    netstat -ano | findstr ":%%p " | findstr "LISTENING" >nul 2>&1
    if !errorlevel! equ 0 (
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%%p " ^| findstr "LISTENING"') do (
            echo       [占用] 端口 %%p (PID: %%a)
            echo       [占用] 端口 %%p ^(PID: %%a^) >> "%DIAG_REPORT%"
        )
    ) else (
        echo       [空闲] 端口 %%p
        echo       [空闲] 端口 %%p >> "%DIAG_REPORT%"
    )
)

echo.

:: ============================================================
:: 6. 进程运行状态
:: ============================================================
echo [6/7] 检查进程运行状态...

(
    echo [进程状态]
) >> "%DIAG_REPORT%"

:: 检查Electron
tasklist /FI "IMAGENAME eq electron.exe" 2>nul | find /I "electron.exe" >nul
if %errorlevel% equ 0 (
    echo [运行中] Electron 进程
    echo Electron: 运行中 >> "%DIAG_REPORT%"
    
    :: 显示详细信息（简化版）
    for /f "tokens=2" %%p in ('tasklist /FI "IMAGENAME eq electron.exe" /NH /FO CSV ^| findstr /r "[0-9]"') do (
        echo         PID: %%p
    )
) else (
    echo [未运行] Electron
    echo Electron: 未运行 >> "%DIAG_REPORT%"
)

:: 检查Python WebUI进程
wmic process where "name='python.exe' and commandline like '%%webui%%'" get processid 2>nul | findstr /r "[0-9]" >nul
if %errorlevel% equ 0 (
    echo [运行中] WebUI 服务
    echo WebUI: 运行中 >> "%DIAG_REPORT%"
) else (
    echo [未运行] WebUI 服务
    echo WebUI: 未运行 >> "%DIAG_REPORT%"
)

:: 检查Node.js
tasklist /FI "IMAGENAME eq node.exe" 2>nul | find /I "node.exe" >nul
if %errorlevel% equ 0 (
    echo [存在] Node.js 进程（可能包含本项目或其他程序）
    echo Node.js: 存在进程 >> "%DIAG_REPORT%"
) else (
    echo [无] Node.js 进程
    echo Node.js: 无进程 >> "%DIAG_REPORT%"
)

echo.

:: ============================================================
:: 7. 磁盘空间和内存检查
:: ============================================================
echo [7/7] 检查系统资源...

:: 磁盘空间
for /f "tokens=3" %%a in ('wmic logicaldisk where "DeviceID='%CD:~0,2%'" get FreeSpace /value ^| findstr "="') do (
    set FREE_SPACE=%%a
)
for /f "tokens=3" %%a in ('wmic logicaldisk where "DeviceID='%CD:~0,2%'" get Size /value ^| findstr "="') do (
    set TOTAL_SPACE=%%a
)

:: 转换为GB（整数除法）
set /a FREE_GB=!FREE_SPACE! / 1073741824
set /a TOTAL_GB=!TOTAL_SPACE! / 1073741824

echo [信息] 磁盘空间: 可用 !FREE_GB! GB / 总计 !TOTAL_GB! GB

:: 内存信息
for /f "skip=1" %%a in ('wmic os get TotalVisibleMemorySize') do (
    if not "%%a"=="" set TOTAL_MEM=%%a
)
for /f "skip=1" %%a in ('wmic os get FreePhysicalMemory') do (
    if not "%%a"=="" set FREE_MEM=%%a
)

:: 计算已使用内存
set /a USED_MEM=!TOTAL_MEM! - !FREE_MEM!
set /a MEM_MB=!USED_MEM! / 1024

echo [信息] 内存使用: 约 !MEM_MB! MB (!USED_MEM! KB)
echo [信息] 内存总量: 约 !TOTAL_MEM:~0,-3! MB

(
    echo [系统资源]
    echo 磁盘空间: 可用 !FREE_GB! GB / 总计 !TOTAL_GB! GB
    echo 内存使用: !MEM_MB! MB / 总量约 !TOTAL_MEM:~0,-3! MB
    echo.
) >> "%DIAG_REPORT%"

echo.

:: ============================================================
:: 生成诊断总结
:: ============================================================
echo.
echo +--------------------------------------------------+
|                    诊断完成                             |
+--------------------------------------------------+
|                                                          |
|  详细报告已保存至:                                       |
|     system_diagnosis_*.txt                              |
|                                                          |
|  建议:                                                   |

:: 根据检查结果给出建议
if %MISSIVE_FILES% gtr 0 (
    echo  - 请补充缺失的项目文件
)
if %MISSIVE_DIRS% gtr 0 (
    echo  - 请创建缺失的目录或重新下载项目
)

echo  - 如遇到问题，请查看详细诊断报告
echo  - 确保所有依赖已正确安装
+--------------------------------------------------+
echo.

echo [信息] 诊断报告路径: %DIAG_REPORT%
echo.

timeout /t 5 /nobreak >nul
exit /b 0