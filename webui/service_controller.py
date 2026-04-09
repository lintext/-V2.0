#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebUI 模块化重构 - 服务控制模块
负责服务的启动、停止和状态管理
"""

import sys
import subprocess
import time
import os
from flask import Blueprint, jsonify

from .utils import PROJECT_ROOT, logger, service_processes, service_pids, is_service_running

CREATE_NO_WINDOW = 0x08000000 if sys.platform.startswith('win') else 0

service_bp = Blueprint('service', __name__)

import datetime
START_TIME = datetime.datetime.now()


@service_bp.route('/api/status')
def get_status():
    """获取所有服务的状态"""
    status = {}
    for service in service_pids.keys():
        status[service] = 'running' if service_pids.get(service, False) else 'stopped'
    return jsonify(status)


@service_bp.route('/api/system/info')
def get_system_info():
    """获取系统信息（版本、运行时间等）"""
    uptime = datetime.datetime.now() - START_TIME
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    uptime_str = f"{days}天{hours}小时{minutes}分钟{seconds}秒" if days > 0 else f"{hours}小时{minutes}分钟{seconds}秒"

    from .utils import WEBUI_VERSION
    return jsonify({
        'version': WEBUI_VERSION,
        'uptime': uptime_str,
        'start_time': START_TIME.strftime('%Y-%m-%d %H:%M:%S'),
        'start_timestamp': START_TIME.timestamp()
    })


@service_bp.route('/api/start/<service>', methods=['POST'])
def start_service(service):
    """启动指定服务"""
    try:
        if is_service_running(service):
            return jsonify({'success': False, 'error': '服务已在运行中'})

        # 允许 memos 后端放在仓库根目录或 plugins-dlc 目录中，按存在顺序选取
        memos_dir_candidates = [
            PROJECT_ROOT.parent / 'memos_system',
            PROJECT_ROOT.parent / 'plugins-dlc' / 'memos' / 'memos_system'
        ]
        memos_dir = memos_dir_candidates[0]
        for _p in memos_dir_candidates:
            if _p.exists():
                memos_dir = _p
                break

        script_map = {
            'live2d': {
                'script': str(PROJECT_ROOT / 'go.bat'),
                'cwd': str(PROJECT_ROOT),
                'log_file': PROJECT_ROOT / 'runtime.log'
            },
            'asr': {
                'script': str(PROJECT_ROOT.parent / '1.ASR.bat'),
                'cwd': str(PROJECT_ROOT.parent),
                'log_file': PROJECT_ROOT.parent / 'logs' / 'asr.log'
            },
            'tts': {
                'script': str(PROJECT_ROOT.parent / '2.TTS.bat'),
                'cwd': str(PROJECT_ROOT.parent),
                'log_file': PROJECT_ROOT.parent / 'logs' / 'tts.log'
            },
            'bert': {
                'script': str(PROJECT_ROOT.parent / '3.bert.bat'),
                'cwd': str(PROJECT_ROOT.parent),
                'log_file': PROJECT_ROOT.parent / 'logs' / 'bert.log'
            },
            'memos': {
                'script': str(memos_dir / 'start_memos.bat'),
                'cwd': str(memos_dir),
                'log_file': PROJECT_ROOT.parent / 'logs' / 'memos.log'
            },
            'rag': {
                'script': str(PROJECT_ROOT.parent / 'RAG.bat'),
                'cwd': str(PROJECT_ROOT.parent),
                'log_file': PROJECT_ROOT.parent / 'logs' / 'rag.log'
            }
        }

        if service not in script_map:
            return jsonify({'success': False, 'error': f'未知服务：{service}'})

        config = script_map[service]

        log_file = config.get('log_file')
        if log_file:
            log_dir = log_file.parent
            if not log_dir.exists():
                log_dir.mkdir(parents=True, exist_ok=True)
            try:
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.write('')
                logger.warning(f'已清空日志文件：{log_file}')
            except Exception as e:
                logger.error(f'清空日志文件失败：{e}')
        
        log_handle = None
        if log_file:
            try:
                log_handle = open(log_file, 'a', encoding='utf-8')
            except:
                pass

        proc = subprocess.Popen(
            ['cmd', '/c', config['script']],
            cwd=config['cwd'],
            creationflags=CREATE_NO_WINDOW if sys.platform.startswith('win') else 0,
            stdout=log_handle if log_handle else subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            shell=False
        )

        service_processes[service] = proc
        service_pids[service] = True
        logger.warning(f'{service} 服务已启动 (PID: {proc.pid})')

        return jsonify({'success': True, 'pid': proc.pid})
        
    except Exception as e:
        logger.error(f'启动 {service} 服务失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)})


@service_bp.route('/api/stop/<service>', methods=['POST'])
def stop_service(service):
    """停止指定服务"""
    try:
        # 使用 PowerShell 根据命令行参数查找 PID，然后用 taskkill /T 终止进程树
        if sys.platform.startswith('win'):
            # 优先使用 service_processes 中保存的进程 PID
            pids = []

            if service in service_processes:
                proc = service_processes[service]
                if proc and proc.poll() is None:
                    # 进程还在运行，使用记录的 PID
                    pids = [str(proc.pid)]
                    logger.debug(f'使用记录的 PID: {proc.pid}')

            # 如果没有找到记录的 PID，使用 PowerShell 查找
            if not pids:
                # 构建 bat 文件名
                if service == 'live2d':
                    bat_name = 'go.bat'
                elif service == 'memos':
                    bat_name = 'start_memos.bat'
                elif service == 'rag':
                    bat_name = 'RAG.bat'
                else:
                    bat_name = f'{service}.bat'

                # 使用 PowerShell 查找包含 bat 文件名的进程 PID
                ps_script = f"""
                $ErrorActionPreference = 'SilentlyContinue'
                $procs = Get-CimInstance Win32_Process | Where-Object {{ $_.CommandLine -and $_.CommandLine -like '*{bat_name}*' }}
                foreach ($proc in $procs) {{
                    Write-Output $proc.ProcessId
                }}
                """

                result = subprocess.run(
                    ['powershell', '-Command', ps_script],
                    capture_output=True, text=True, timeout=10
                )

                # 解析输出的 PID 列表
                pids = [line.strip() for line in result.stdout.split('\n') if line.strip().isdigit()]

            # 如果没有找到进程，说明服务已停止，直接重置状态
            if not pids:
                logger.info(f'{service} 服务已停止（进程不存在）')
                # 清除标记（确保按钮复位）
                service_pids[service] = False
                if service in service_processes:
                    del service_processes[service]
                return jsonify({'success': True, 'message': '服务已停止'})

            # 对每个 PID 使用 taskkill /T 终止进程树
            killed_count = 0
            failed_pids = []
            for pid in pids:
                kill_result = subprocess.run(
                    ['taskkill', '/F', '/T', '/PID', pid],
                    capture_output=True, text=True, timeout=10
                )
                # taskkill 成功时输出 "SUCCESS: ... has been terminated."（英文系统）或 "成功"（中文系统）
                output = kill_result.stdout + kill_result.stderr
                if 'SUCCESS' in output or '成功' in output or 'terminated' in output:
                    killed_count += 1
                    logger.debug(f'已终止进程树 PID: {pid}')
                else:
                    # 检查是否是因为进程已不存在（进程已自行退出）
                    if 'not found' in output.lower() or '找不到' in output:
                        # 进程已不存在，服务已停止，视为成功
                        killed_count += 1
                        logger.debug(f'进程 PID {pid} 已不存在，视为已停止')
                    elif kill_result.returncode != 0:
                        # 只有在返回码非 0 且不是 "not found" 时才认为是失败
                        failed_pids.append(pid)
                        logger.warning(f'终止进程 PID {pid} 失败：{output or f"返回码={kill_result.returncode}"}')
                    else:
                        # 返回码为 0 视为成功
                        killed_count += 1
                        logger.debug(f'已终止进程树 PID: {pid} (返回码=0)')

            # 清除服务标记（无论成功与否都重置按钮）
            service_pids[service] = False
            if service in service_processes:
                del service_processes[service]

            if killed_count > 0:
                logger.info(f'{service} 服务已停止（终止了 {killed_count} 个进程树）')
                return jsonify({'success': True, 'message': f'成功终止 {killed_count} 个进程'})
            elif failed_pids:
                logger.warning(f'{service} 服务停止：所有进程终止失败，但已重置状态')
                return jsonify({'success': True, 'warning': '进程可能已自行关闭'})
            else:
                return jsonify({'success': True, 'message': '服务已停止'})
        else:
            return jsonify({'success': False, 'error': '仅支持 Windows 系统'})
    except subprocess.TimeoutExpired:
        logger.error(f'停止 {service} 服务超时')
        # 即使超时也清除标记
        service_pids[service] = False
        return jsonify({'success': True, 'warning': '停止命令已发送，但可能未完全终止'})
    except Exception as e:
        logger.error(f'停止 {service} 服务失败：{str(e)}')
        # 异常时也清除标记
        service_pids[service] = False
        return jsonify({'success': True, 'warning': f'停止服务时出错：{str(e)}'})
