@echo off
chcp 65001 >nul 2>&1
cd /d %~dp0
echo 启动 Electron 桌面宠物...

if exist ".\node\node.exe" (
    echo 使用项目自带的 Node.js
    .\node\node.exe .\node_modules\electron\cli.js .
) else (
    echo 使用系统 Node.js
    node .\node_modules\electron\cli.js .
)

exit /b 0
