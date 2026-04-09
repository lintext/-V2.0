@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

:: ============================================================
:: 桌面宠物AI - 项目清理与优化工具 v2.1 (修复版)
:: 功能：清理冗余文件、优化项目结构、释放磁盘空间
:: 修复：解决一闪而过的问题
:: ============================================================

title 桌面宠物AI - 项目清理工具

color 0B

set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

set /a TOTAL_FILES=0
set /a TOTAL_SIZE=0

echo.
echo +--------------------------------------------------+
|        桌面宠物AI - 项目清理与优化工具 v2.1           |
+--------------------------------------------------+
echo.

echo [警告] 此操作将清理以下内容：
echo   - 临时文件（.tmp, .bak, .old等）
echo   - 缓存目录（__pycache__, .cache等）
echo   - 日志文件（可选）
echo   - 编译产物（.pyc等）
echo.
set /p CONFIRM="是否继续？(Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo [信息] 操作已取消。
    pause
    exit /b 0
)

echo.
echo [开始] 正在清理...
echo.

:: ============================================================
:: 1. 清理临时文件
:: ============================================================
echo [1/6] 清理临时文件...

set "TEMP_EXTENSIONS=.tmp .bak .old .swp .swo ~ .orig .log .pyc .pyo"

for %%e in (%TEMP_EXTENSIONS%) do (
    for /r "%PROJECT_ROOT%" %%f in (*%%e) do (
        if exist "%%f" (
            set /a TOTAL_FILES+=1
            for %%A in ("%%f") do set /a TOTAL_SIZE+=%%~zA
            del /q "%%f" >nul 2>&1
        )
    )
)

if %TOTAL_FILES% gtr 0 (
    echo [完成] 已删除 %TOTAL_FILES% 个临时文件
) else (
    echo [信息] 未发现需要清理的临时文件
)

echo.

:: ============================================================
:: 2. 清理缓存目录
:: ============================================================
echo [2/6] 清理缓存目录...

set CACHE_COUNT=0

:: 清理__pycache__
for /d /r "%PROJECT_ROOT%" %%d in (__pycache__) do (
    if exist "%%d" (
        rd /s /q "%%d" >nul 2>&1
        set /a CACHE_COUNT+=1
        echo       已删除: %%d
    )
)

:: 清理node_modules/.cache
if exist "%PROJECT_ROOT%\node_modules\.cache" (
    rd /s /q "%PROJECT_ROOT%\node_modules\.cache" >nul 2>&1
    set /a CACHE_COUNT+=1
    echo       已删除: node_modules\.cache
)

:: 清理electron-cache
if exist "%PROJECT_ROOT%\electron-cache" (
    rd /s /q "%PROJECT_ROOT%\electron-cache" >nul 2>&1
    set /a CACHE_COUNT+=1
    echo       已删除: electron-cache
)

if %CACHE_COUNT% gtr 0 (
    echo [完成] 已清理 %CACHE_COUNT% 个缓存目录
) else (
    echo [信息] 无需清理的缓存目录
)

echo.

:: ============================================================
:: 3. 清理日志文件（可选）
:: ============================================================
echo [3/6] 清理日志文件...

set /p CLEAN_LOGS="是否清空日志文件内容？(Y/N): "
if /i "%CLEAN_LOGS%"=="Y" (
    set LOG_COUNT=0
    
    :: 清理logs目录下的日志
    if exist "%PROJECT_ROOT%\logs" (
        for /r "%PROJECT_ROOT%\logs" %%f in (*.log *.txt) do (
            if exist "%%f" (
                echo. > "%%f"
                set /a LOG_COUNT+=1
            )
        )
    )
    
    :: 清理根目录的日志
    for %%f in ("%PROJECT_ROOT%\startup_log.txt" "%PROJECT_ROOT%\error_log.txt") do (
        if exist "%%f" (
            echo. > "%%f"
            set /a LOG_COUNT+=1
        )
    )
    
    echo [完成] 已清空 %LOG_COUNT% 个日志文件
) else (
    echo [跳过] 日志文件保持不变
)

echo.

:: ============================================================
:: 4. 清理备份文件
:: ============================================================
echo [4/6] 清理备份文件...

set BACKUP_COUNT=0
for /r "%PROJECT_ROOT%" %%f in (*backup* *副本* *copy*) do (
    if exist "%%f" (
        set /a TOTAL_FILES+=1
        del /q "%%f" >nul 2>&1
        set /a BACKUP_COUNT+=1
    )
)

if %BACKUP_COUNT% gtr 0 (
    echo [完成] 已删除 %BACKUP_COUNT% 个备份文件
) else (
    echo [信息] 无需清理的备份文件
)

echo.

:: ============================================================
:: 5. 整理项目结构
:: ============================================================
echo [5/6] 整理项目结构...

:: 确保必要目录存在
set DIR_CREATED=0
set "DIRS_TO_CREATE=data logs temp backup"

for %%d in (%DIRS_TO_CREATE%) do (
    if not exist "%PROJECT_ROOT%\%%d" (
        mkdir "%PROJECT_ROOT%\%%d" >nul 2>&1
        if !errorlevel! equ 0 (
            echo       创建目录: %%d\
            set /a DIR_CREATED+=1
        )
    )
)

if %DIR_CREATED% gtr 0 (
    echo [完成] 已创建 %DIR_CREATED% 个必要目录
) else (
    echo [信息] 目录结构完整，无需调整
)

echo.

:: ============================================================
:: 6. 生成清理报告
:: ============================================================
echo [6/6] 生成清理报告...

set /a SIZE_MB=%TOTAL_SIZE% / 1048576

echo.
echo +--------------------------------------------------+
|                    清理报告                            |
+--------------------------------------------------+
|                                                          |
|  清理文件数量:     %TOTAL_FILES% 个                      |
|  释放空间:         约 %SIZE_MB% MB                       |
|  完成时间:         %time%                               |
|                                                          |
|  项目已优化完成！                                         |
+--------------------------------------------------+
echo.

:: 将报告写入文件
(
    echo 桌面宠物AI - 项目清理报告
    echo ========================================
    echo 清理时间: %date% %time%
    echo 清理文件数: %TOTAL_FILES%
    echo 释放空间: 约 %SIZE_MB% MB
    echo ----------------------------------------
) > "%PROJECT_ROOT%\cleanup_report_%date:~0,4%%date:~5,2%%date:~8,2%.txt"

echo [信息] 详细报告已保存至: cleanup_report_*.txt
echo.

timeout /t 3 /nobreak >nul
exit /b 0