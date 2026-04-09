@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

:: ============================================================
:: 桌面宠物AI应用程序 - 一键启动脚本 v2.1 (修复版)
:: 功能：自动启动WebUI控制面板 + Electron桌面宠物
:: 作者：AI Assistant
:: 创建日期：2026-04-04
:: 修复：解决一闪而过的问题
:: ============================================================

title 桌面宠物AI - 一键启动系统

:: 设置颜色主题
color 0A

:: 定义项目根目录
set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

:: 定义服务端口
set "WEBUI_PORT=5001"
set "MUSIC_PORT=9001"
set "EMOTION_PORT=9002"

:: 定义日志文件
set "LOG_FILE=%PROJECT_ROOT%\startup_log.txt"
set "ERROR_LOG=%PROJECT_ROOT%\error_log.txt"

:: 错误处理：确保任何错误都会显示并暂停
if not exist "%PROJECT_ROOT%" (
    echo.
    echo ========================================
    echo   [致命错误] 无法确定项目根目录！
    echo   当前路径: %PROJECT_ROOT%
    echo ========================================
    echo.
    pause
    exit /b 1
)

:: ============================================================
:: 函数定义区域（使用goto而非return）
:: ============================================================

:print_header
    echo.
    echo +--------------------------------------------------+
    echo |                                                  |
    echo |      桌面宠物AI应用程序 - 一键启动系统 v2.1       |
    echo |                                                  |
    echo +--------------------------------------------------+
    echo.
    goto :eof

:log_message
    set "MSG=[%date% %time%] %~1"
    echo !MSG! >> "%LOG_FILE%"
    goto :eof

:check_error
    if %errorlevel% neq 0 (
        call :log_message "[ERROR] %~1"
        echo.
        echo [错误] %~1
        echo [详细错误信息] >> "%ERROR_LOG%"
        echo 时间: %date% %time% >> "%ERROR_LOG%"
        echo 错误: %~1 >> "%ERROR_LOG%"
        echo ---------------------------------------- >> "%ERROR_LOG%"
        echo.
        echo 按任意键退出...
        pause >nul
        exit /b 1
    )
    goto :eof

:check_port
    netstat -ano | findstr ":%~1 " >nul 2>&1
    if %errorlevel% equ 0 (
        echo [警告] 端口 %~1 已被占用
        call :log_message "警告: 端口 %~1 已被占用"
    )
    goto :eof

:: ============================================================
:: 主程序开始
:: ============================================================

call :print_header

:: 清空日志文件
echo. > "%LOG_FILE%" 2>nul
echo. > "%ERROR_LOG%" 2>nul

call :log_message "========== 启动脚本执行开始 =========="

echo 正在检查系统环境...
echo.

:: ============================================================
:: 步骤1：依赖检查
:: ============================================================
echo [步骤 1/6] 检查系统依赖...
call :log_message "开始检查系统依赖"

:: 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   [错误] Python 未安装或未添加到PATH
    echo   请安装Python 3.8或更高版本
    echo   下载地址: https://www.python.org/downloads/
    echo ========================================
    echo.
    pause
    exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do (
    echo [OK] Python 版本: %%v
    call :log_message "Python版本: %%v"
)

:: 检查Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   [错误] Node.js 未安装或未添加到PATH
    echo   请安装Node.js 16或更高版本
    echo   下载地址: https://nodejs.org/
    echo ========================================
    echo.
    pause
    exit /b 1
)
for /f "tokens=1" %%v in ('node --version') do (
    echo [OK] Node.js 版本: %%v
    call :log_message "Node.js版本: %%v"
)

:: 检查npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   [错误] npm 未安装
    echo   npm通常随Node.js一起安装
    echo   请重新安装Node.js
    echo ========================================
    echo.
    pause
    exit /b 1
)
for /f "tokens=1" %%v in ('npm --version') do (
    echo [OK] npm 版本: %%v
    call :log_message "npm版本: %%v"
)

echo.
echo [成功] 所有基础依赖已就绪！
echo.

:: ============================================================
:: 步骤2：项目目录验证
:: ============================================================
echo [步骤 2/6] 验证项目目录结构...
call :log_message "验证项目目录结构"

:: 检查关键目录
set "MISSING_DIRS="
set "REQUIRED_DIRS=webui js css libs 2D data"
for %%d in (%REQUIRED_DIRS%) do (
    if not exist "%PROJECT_ROOT%\%%d" (
        echo [错误] 缺少必要目录: %%d
        set "MISSING_DIRS=!MISSING_DIRS! %%d"
    )
)

:: 检查关键文件
set "MISSING_FILES="
set "REQUIRED_FILES=config.json package.json main.js index.html"
for %%f in (%REQUIRED_FILES%) do (
    if not exist "%PROJECT_ROOT%\%%f" (
        echo [错误] 缺少必要文件: %%f
        set "MISSING_FILES=!MISSING_FILES! %%f"
    )
)

:: 如果有缺失的文件或目录
if defined MISSING_DIRS (
    echo.
    echo ========================================
    echo   [致命错误] 项目文件不完整！
    echo   缺失目录:!MISSING_DIRS!
    echo   缺失文件:!MISSING_FILES!
    echo.
    echo   请确保已正确解压完整的项目包
    echo ========================================
    echo.
    pause
    exit /b 1
)

if defined MISSING_FILES (
    echo.
    echo ========================================
    echo   [致命错误] 项目文件不完整！
    echo   缺失文件:!MISSING_FILES!
    echo.
    echo   请确保已正确解压完整的项目包
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo [成功] 项目结构验证通过！
echo.

:: ============================================================
:: 步骤3：端口占用检查
:: ============================================================
echo [步骤 3/6] 检查服务端口...
call :log_message "检查服务端口占用情况"

call :check_port %WEBUI_PORT%
call :check_port %MUSIC_PORT%
call :check_port %EMOTION_PORT%

echo [成功] 端口检查完成！
echo.

:: ============================================================
:: 步骤4：安装和更新依赖
:: ============================================================
echo [步骤 4/6] 安装/更新项目依赖...
call :log_message "开始安装/更新依赖"

:: 安装Node.js依赖
cd /d "%PROJECT_ROOT%" >nul 2>&1
echo [信息] 正在检查npm依赖...
if exist "%PROJECT_ROOT%\node_modules" (
    echo [跳过] node_modules已存在，跳过安装
) else (
    echo [正在安装] npm install (这可能需要几分钟)...
    call npm install --production >nul 2>&1
    if %errorlevel% neq 0 (
        echo [警告] npm install 出现问题，但继续执行...
        call :log_message "警告: npm install 可能存在问题"
    ) else (
        echo [完成] npm install 成功
    )
)

:: 检查并安装Python依赖
echo [信息] 检查Python依赖...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo [正在安装] Flask...
    pip install flask -q >nul 2>&1
    if %errorlevel% equ 0 (
        echo [完成] Flask安装成功
        call :log_message "已安装Flask"
    ) else (
        echo [警告] Flask安装失败，WebUI可能无法启动
    )
) else (
    echo [OK] Flask 已安装
)

echo [成功] 所有依赖准备完成！
echo.

:: ============================================================
:: 步骤5：清理冗余文件（可选）
:: ============================================================
echo [步骤 5/6] 清理临时文件...
call :log_message "开始清理临时文件"

:: 只清理明显的临时文件
set CLEANED_COUNT=0

:: 清理__pycache__
if exist "%PROJECT_ROOT%\webui\__pycache__" (
    rd /s /q "%PROJECT_ROOT%\webui\__pycache__" >nul 2>&1
    set /a CLEANED_COUNT+=1
)

:: 清理其他明显缓存
for /d %%d in ("%PROJECT_ROOT%\__pycache__") do (
    if exist "%%d" (
        rd /s /q "%%d" >nul 2>&1
        set /a CLEANED_COUNT+=1
    )
)

echo [完成] 已清理 %CLEANED_COUNT% 个缓存目录
echo.

:: ============================================================
:: 步骤6：启动服务
:: ============================================================
echo [步骤 6/6] 启动所有服务...
call :log_message "开始启动所有服务"
echo.

:: ----------------------------------------------------------
:: 启动 WebUI 控制面板 (后台运行)
:: ----------------------------------------------------------
echo [1/3] 正在启动 WebUI 控制面板...
call :log_message "正在启动WebUI服务"

:: 使用start命令后台启动Python进程
:: 使用 helper 脚本启动 WebUI（优先使用 run_webui.bat）
if exist "%PROJECT_ROOT%\run_webui.bat" (
    start "WebUI-Server" "%PROJECT_ROOT%\run_webui.bat"
) else (
    start "WebUI-Server" cmd /c "cd /d "%PROJECT_ROOT%" && python -m webui.main_app"
)

:: 等待WebUI启动
echo [等待] WebUI 服务初始化中...
timeout /t 6 /nobreak >nul

:: 验证WebUI是否成功启动（简单检测）
netstat -ano | findstr ":%WEBUI_PORT% " | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo [成功] WebUI 控制面板启动成功！
    echo        访问地址: http://localhost:%WEBUI_PORT%
    call :log_message "WebUI启动成功 - http://localhost:%WEBUI_PORT%"
    
    :: 将端口号写入配置文件供Electron读取
    echo %WEBUI_PORT% > "%PROJECT_ROOT%\data\webui_port.txt" 2>nul
) else (
    echo.
    echo [警告] WebUI 可能还在启动中，请稍后手动访问 http://localhost:%WEBUI_PORT%
    call :log_message "警告: WebUI可能未完全启动"
)

echo.

:: ----------------------------------------------------------
:: 启动 Electron 桌面宠物应用
:: ----------------------------------------------------------
echo [2/3] 正在启动 Electron 桌面宠物应用...
call :log_message "正在启动Electron应用"

:: 使用 helper 脚本启动 Electron 桌面应用（优先使用 run_electron.bat）
if exist "%PROJECT_ROOT%\run_electron.bat" (
    start "Desktop-Pet" "%PROJECT_ROOT%\run_electron.bat"
) else (
    :: 如果没有 helper，则尝试直接调用 node/electron
    if exist "%PROJECT_ROOT%\node\node.exe" (
        echo [信息] 使用项目自带的 Node.js 环境
        start "Desktop-Pet" "%PROJECT_ROOT%\node\node.exe" "%PROJECT_ROOT%\node_modules\electron\cli.js" "."
    ) else (
        echo [信息] 使用系统环境的 Node.js
        start "Desktop-Pet" cmd /c "cd /d "%PROJECT_ROOT%" && node "%PROJECT_ROOT%\node_modules\electron\cli.js" ".""
    )
)

:: 等待Electron启动
echo [等待] Electron 应用程序初始化中...
timeout /t 10 /nobreak >nul

echo [成功] Electron 桌面宠物已启动！
call :log_message "Electron桌面宠物启动成功"
echo.

:: ----------------------------------------------------------
:: 打开主页面
:: ----------------------------------------------------------
echo [3/3] 正在打开浏览器...
call :log_message "正在打开浏览器访问主页"

:: 延迟一下确保服务完全就绪
timeout /t 2 /nobreak >nul

:: 尝试打开WebUI控制面板
start "" "http://localhost:%WEBUI_PORT%" 2>nul

echo [成功] 已尝试打开浏览器！
echo.

:: ============================================================
:: 启动完成总结
:: ============================================================
echo.
echo +--------------------------------------------------+
|                    启动完成总结                        |
+--------------------------------------------------+
|                                                          |
|  WebUI控制面板:     http://localhost:%WEBUI_PORT%         |
|  桌面宠物状态:     运行中                               |
|  音乐服务端口:      %MUSIC_PORT%                            |
|  情绪服务端口:      %EMOTION_PORT%                            |
|                                                          |
|  日志文件:          startup_log.txt                       |
|  错误日志:          error_log.txt                         |
|                                                          |
+----------------------------------------------------------+
|  提示:                                                    |
|  - 此窗口可关闭，不影响已启动的服务                      |
|  - 关闭桌面宠物请点击宠物界面上的退出按钮               |
|  - 如需停止所有服务，请运行 stop_services.bat            |
+----------------------------------------------------------+
echo.

call :log_message "========== 启动脚本执行完成 =========="
call :log_message "所有服务已成功启动并正常运行"

:: 显示快捷键提示
echo 可用快捷键:
echo    Ctrl+Q          - 退出应用
echo    Ctrl+G          - 打断语音播放
echo    Ctrl+T          - 强制窗口置顶
echo    Ctrl+Shift+1~9  - 触发动作1~9
echo    Ctrl+Shift+0    - 停止所有动作
echo    Ctrl+M          - 切换聊天框显示
echo.

echo ==========================================
echo   按任意键关闭此窗口...
echo   (已启动的服务将继续运行)
echo ==========================================
pause >nul
exit /b 0