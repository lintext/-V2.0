#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebUI 模块化重构 - 日志与监控模块
负责日志读取、心情状态监控和 Live2D 动作管理
"""

import json
import datetime
import urllib.request
import pymysql
from pathlib import Path
from collections import deque
from flask import Blueprint, request, jsonify

from .utils import PROJECT_ROOT, logger

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'xiaoai',
    'charset': 'utf8mb4'
}

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            charset=DB_CONFIG['charset'],
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        logger.error(f'MySQL 连接失败: {e}')
        raise e

log_bp = Blueprint('log', __name__)


# ============ 日志 API ============

@log_bp.route('/api/logs/<log_type>')
def get_logs(log_type):
    """获取指定类型的日志（优化版：只读取最后 100 行）"""
    try:
        log_file = PROJECT_ROOT / 'runtime.log'
        if not log_file.exists():
            return jsonify({'logs': [], 'error': '日志文件不存在'})

        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                last_lines = deque(f, maxlen=100)

                logs = []
                for line in last_lines:
                    line = line.strip()
                    if line:
                        is_tool_log = '[TOOL]' in line
                        if log_type == 'tool' and is_tool_log:
                            logs.append(line)
                        elif log_type == 'pet' and not is_tool_log:
                            logs.append(line)

                return jsonify({'logs': logs})
        except Exception as e:
            return jsonify({'logs': [], 'error': str(e)})
    except Exception as e:
        return jsonify({'logs': [], 'error': str(e)})


@log_bp.route('/api/logs/tail/<log_type>')
def tail_logs(log_type):
    """获取日志的最新内容（增量）"""
    try:
        log_file = PROJECT_ROOT / 'runtime.log'
        if not log_file.exists():
            return jsonify({'logs': [], 'error': '日志文件不存在'})

        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                last_lines = deque(f, maxlen=10)

                logs = []
                for line in last_lines:
                    line = line.strip()
                    if line:
                        is_tool_log = '[TOOL]' in line
                        if log_type == 'tool' and is_tool_log:
                            logs.append(line)
                        elif log_type == 'pet' and not is_tool_log:
                            logs.append(line)

                return jsonify({'logs': logs})
        except Exception as e:
            return jsonify({'logs': [], 'error': str(e)})
    except Exception as e:
        return jsonify({'logs': [], 'error': str(e)})


# ============ Live2D 动作管理 API ============
# 注意：这些 API 已在 config_manager.py 中定义，此处注释掉避免冲突

# @log_bp.route('/api/live2d/singing/start', methods=['POST'])
# def start_singing():
#     """开始唱歌"""
#     try:
#         try:
#             json_data = json.dumps({'action': 'trigger_emotion', 'emotion_name': '唱歌'}).encode('utf-8')
#             req = urllib.request.Request('http://localhost:3002/control-motion', data=json_data, method='POST')
#             req.add_header('Content-Type', 'application/json')
#             with urllib.request.urlopen(req, timeout=2) as response:
#                 if response.status == 200:
#                     return jsonify({'success': True, 'message': '已开始唱歌'})
#         except Exception:
#             pass
#         return jsonify({'success': True, 'message': '唱歌请求已发送'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#
# @log_bp.route('/api/live2d/singing/stop', methods=['POST'])
# def stop_singing():
#     """停止唱歌"""
#     try:
#         try:
#             json_data = json.dumps({'action': 'trigger_emotion', 'emotion_name': '停止'}).encode('utf-8')
#             req = urllib.request.Request('http://localhost:3002/control-motion', data=json_data, method='POST')
#             req.add_header('Content-Type', 'application/json')
#             with urllib.request.urlopen(req, timeout=2) as response:
#                 if response.status == 200:
#                     return jsonify({'success': True, 'message': '已停止唱歌'})
#         except Exception:
#             pass
#         return jsonify({'success': True, 'message': '停止请求已发送'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#
# @log_bp.route('/api/live2d/motion/reset', methods=['POST'])
# def reset_motion():
#     """复位动作配置（从备份恢复）"""
#     try:
#         import re
#         
#         # 从 main.js 读取当前模型名
#         live2d_path = PROJECT_ROOT / 'live-2d'
#         main_js_path = live2d_path / 'main.js'
#         model_name = '肥牛'  # 默认
#         
#         if main_js_path.exists():
#             with open(main_js_path, 'r', encoding='utf-8') as f:
#                 content = f.read()
#             match = re.search(r"const priorityFolders = \['([^']+)'", content)
#             if match:
#                 model_name = match.group(1)
#         
#         # 从备份配置恢复
#         backup_path = live2d_path / 'character_backups.json'
#         config_path = live2d_path / 'emotion_actions.json'
#
#         if backup_path.exists():
#             with open(backup_path, 'r', encoding='utf-8') as f:
#                 backup = json.load(f)
#
#             # 读取现有配置（保留其他模型的数据）
#             existing_config = {}
#             if config_path.exists():
#                 with open(config_path, 'r', encoding='utf-8') as f:
#                     existing_config = json.load(f)
#
#             # 从备份中提取当前模型的动作配置
#             if model_name in backup:
#                 model_backup = backup[model_name]
#                 if 'original_config' in model_backup:
#                     emotion_actions = model_backup['original_config'].get('emotion_actions', {})
#                     existing_config[model_name] = {
#                         'emotion_actions': emotion_actions
#                     }
#                 else:
#                     existing_config[model_name] = model_backup
#
#             with open(config_path, 'w', encoding='utf-8') as f:
#                 json.dump(existing_config, f, ensure_ascii=False, indent=2)
#
#             logger.info(f'动作配置已从备份恢复（模型：{model_name}）')
#             return jsonify({'success': True, 'message': '动作配置已重置'})
#         else:
#             logger.error(f'备份文件不存在：{backup_path}')
#             return jsonify({'success': False, 'error': '备份文件不存在'})
#     except Exception as e:
#         logger.error(f'重置动作配置失败：{str(e)}')
#         return jsonify({'success': False, 'error': str(e)}), 500
#
#
# @log_bp.route('/api/live2d/motion/preview', methods=['POST'])
# def preview_motion():
#     """预览动作"""
#     try:
#         data = request.get_json()
#         motion_name = data.get('motion', '')
#         
#         # 使用 trigger_emotion action 来触发情绪对应的动作
#         try:
#             json_data = json.dumps({
#                 'action': 'trigger_emotion',
#                 'emotion_name': motion_name
#             }).encode('utf-8')
#             req = urllib.request.Request('http://localhost:3002/control-motion', data=json_data, method='POST')
#             req.add_header('Content-Type', 'application/json')
#             with urllib.request.urlopen(req, timeout=2) as response:
#                 if response.status == 200:
#                     return jsonify({'success': True, 'message': f'正在预览动作：{motion_name}'})
#         except Exception as http_error:
#             logger.warning(f'HTTP 请求失败：{http_error}')
#
#         return jsonify({'success': True, 'message': f'预览请求已发送：{motion_name}'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# ============ 声音克隆 API ============

@log_bp.route('/api/voice-clone/generate-bat', methods=['POST'])
def generate_tts_bat():
    """生成 TTS 的 bat 文件"""
    try:
        # 获取上传的文件
        model_file = request.files.get('model_file')
        audio_file = request.files.get('audio_file')
        role_name = request.form.get('role_name', '')
        language = request.form.get('language', 'zh')
        text = request.form.get('text', '')

        if not model_file or not audio_file or not role_name or not text:
            return jsonify({'success': False, 'error': '缺少必要参数'}), 400

        # 保存到 Voice_Model_Factory 目录
        voice_model_dir = PROJECT_ROOT / 'Voice_Model_Factory'
        voice_model_dir.mkdir(parents=True, exist_ok=True)

        # 保存模型文件
        model_filename = f'{role_name}.pth'
        model_path = voice_model_dir / model_filename
        model_file.save(model_path)

        # 保存音频文件
        audio_filename = f'{role_name}.wav'
        audio_path = voice_model_dir / audio_filename
        audio_file.save(audio_path)

        # 生成 bat 文件
        bat_content = f'''@echo off
chcp 65001 >nul
echo.
echo ========================================
echo  TTS 声音克隆 - {role_name}
echo ========================================
echo.
echo 正在生成 TTS...
echo.

python -m tools.tts_inference \\
    --model_path "Voice_Model_Factory/{model_filename}" \\
    --audio_path "Voice_Model_Factory/{audio_filename}" \\
    --language {language} \\
    --text "{text}"

echo.
echo 生成完成！
echo.
pause
'''

        bat_path = voice_model_dir / f'{role_name}.bat'
        with open(bat_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)

        return jsonify({
            'success': True,
            'message': f'已生成 TTS 的 bat 文件：{role_name}.bat',
            'bat_path': str(bat_path)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ 对话历史 API ============

@log_bp.route('/api/chat-history')
def get_chat_history():
    """获取对话历史记录（支持分页，从MySQL数据库读取）"""
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 50, type=int)
        # 优先从数据库加载，如果数据库不可用则回退到本地文件（AI记录室）
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) as count FROM chat_messages')
            total = cursor.fetchone()['count']

            start = (page - 1) * page_size
            end = start + page_size

            cursor.execute('''
                SELECT id, session_id, role, content, emotion, created_at 
                FROM chat_messages 
                ORDER BY created_at ASC 
                LIMIT %s OFFSET %s
            ''', (page_size, start))

            rows = cursor.fetchall()
            messages = []
            for row in rows:
                messages.append({
                    'id': row['id'],
                    'session_id': row['session_id'],
                    'role': row['role'],
                    'content': row['content'],
                    'emotion': row['emotion'],
                    'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S') if row['created_at'] else None
                })

            cursor.close()
            conn.close()

            logger.info(f'获取对话历史成功: 总数={total}, 当前页={page}, 返回={len(messages)}条')

            return jsonify({
                'messages': messages,
                'has_more': end < total,
                'has_prev': page > 1,
                'total': total
            })

        except Exception as db_err:
            # 数据库不可用时回退到本地文件
            logger.warning(f'无法连接数据库，使用本地对话历史文件作为回退: {db_err}')

            # 从 config.json 中读取 history_file 配置，如果没有则使用默认路径
            history_rel = 'AI记录室/对话历史.json'
            try:
                cfg_path = PROJECT_ROOT / 'config.json'
                if cfg_path.exists():
                    import json as _json
                    with open(cfg_path, 'r', encoding='utf-8') as cf:
                        cfg = _json.load(cf)
                        history_rel = cfg.get('context', {}).get('history_file', history_rel)
            except Exception:
                pass

            history_path = PROJECT_ROOT / history_rel
            messages = []
            total = 0

            if history_path.exists():
                try:
                    with open(history_path, 'r', encoding='utf-8') as hf:
                        import json as _json
                        text = hf.read().strip()
                        # 先尝试作为 JSON 数组解析
                        try:
                            data = _json.loads(text)
                            if isinstance(data, list):
                                messages = data
                        except Exception:
                            # 作为 jsonl 逐行解析
                            hf.seek(0)
                            for line in hf:
                                line = line.strip()
                                if not line:
                                    continue
                                try:
                                    obj = _json.loads(line)
                                    messages.append(obj)
                                except Exception:
                                    # 如果不是有效 json，按文本行作为 content
                                    messages.append({'role': 'assistant', 'content': line, 'created_at': None})

                except Exception as e:
                    logger.error(f'读取本地对话历史失败: {e}')

            total = len(messages)
            start = (page - 1) * page_size
            end = start + page_size
            page_messages = messages[start:end]

            return jsonify({
                'messages': page_messages,
                'has_more': end < total,
                'has_prev': page > 1,
                'total': total
            })
    except Exception as e:
        logger.error(f'获取对话历史失败: {e}')
        return jsonify({'error': str(e)}), 500


@log_bp.route('/api/chat-history/clear', methods=['POST'])
def clear_chat_history():
    """清空对话历史记录"""
    try:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM chat_messages')
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True, 'message': '对话历史已清空'})
        except Exception as db_err:
            logger.warning(f'清空数据库历史失败，尝试清空本地文件: {db_err}')

            # 回退到清空本地历史文件
            try:
                cfg_path = PROJECT_ROOT / 'config.json'
                history_rel = 'AI记录室/对话历史.json'
                if cfg_path.exists():
                    import json as _json
                    with open(cfg_path, 'r', encoding='utf-8') as cf:
                        cfg = _json.load(cf)
                        history_rel = cfg.get('context', {}).get('history_file', history_rel)

                history_path = PROJECT_ROOT / history_rel
                if history_path.exists():
                    # 覆盖为空数组
                    with open(history_path, 'w', encoding='utf-8') as hf:
                        hf.write('[]')
                    return jsonify({'success': True, 'message': '本地对话历史已清空'})
                else:
                    return jsonify({'success': True, 'message': '没有找到本地对话历史文件'})
            except Exception as e:
                logger.error(f'清空本地对话历史失败: {e}')
                return jsonify({'success': False, 'error': str(e)}), 500
    except Exception as e:
        logger.error(f'清空对话历史失败: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500
