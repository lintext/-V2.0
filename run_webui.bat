@echo off
chcp 65001 >nul 2>&1
cd /d %~dp0
echo 启动 WebUI 服务...

:: 使用模块方式启动以确保包路径正确
python -m webui.main_app

exit /b 0
