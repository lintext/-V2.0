#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Live2D 设置管理模块
整合所有 Live2D 设置相关的 API，包括：
- 唱歌控制
- 模型配置
- 动作管理
- 表情管理
"""

import json
import urllib.request
import re
from flask import Blueprint, request, jsonify

from .utils import PROJECT_ROOT, logger

# 创建 Live2D 管理蓝图
live2d_bp = Blueprint('live2d', __name__)

# 固定的情绪分类键名
EMOTION_CATEGORIES = ['开心', '生气', '难过', '惊讶', '害羞', '俏皮']


def _get_current_model_name():
    """从 main.js 读取当前模型名称"""
    main_js_path = PROJECT_ROOT / 'main.js'
    if main_js_path.exists():
        content = main_js_path.read_text(encoding='utf-8')
        match = re.search(r"const priorityFolders = \['([^']+)'", content)
        if match:
            return match.group(1)
    return '肥牛'  # 默认角色


def load_emotion_actions():
    """加载 emotion_actions.json 配置"""
    config_path = PROJECT_ROOT / 'emotion_actions.json'
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_emotion_actions(data):
    """保存 emotion_actions.json 配置"""
    config_path = PROJECT_ROOT / 'emotion_actions.json'
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============ 唱歌控制 ============

@live2d_bp.route('/api/live2d/singing/start', methods=['POST'])
def start_singing():
    """开始唱歌"""
    try:
        json_data = json.dumps({'action': 'trigger_emotion', 'emotion_name': '唱歌'}).encode('utf-8')
        req = urllib.request.Request('http://localhost:3002/control-motion', data=json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                return jsonify({'success': True, 'message': '已开始唱歌'})
        return jsonify({'success': True, 'message': '唱歌请求已发送'})
    except Exception as e:
        logger.warning(f'开始唱歌 HTTP 请求失败：{e}')
        return jsonify({'success': True, 'message': '唱歌请求已发送'})


@live2d_bp.route('/api/live2d/singing/stop', methods=['POST'])
def stop_singing():
    """停止唱歌"""
    try:
        json_data = json.dumps({'action': 'trigger_emotion', 'emotion_name': '停止'}).encode('utf-8')
        req = urllib.request.Request('http://localhost:3002/control-motion', data=json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                return jsonify({'success': True, 'message': '已停止唱歌'})
        return jsonify({'success': True, 'message': '停止请求已发送'})
    except Exception as e:
        logger.warning(f'停止唱歌 HTTP 请求失败：{e}')
        return jsonify({'success': True, 'message': '停止请求已发送'})


# ============ 模型配置 ============

@live2d_bp.route('/api/live2d/model/save', methods=['POST'])
def save_live2d_model():
    """保存 Live2D 模型选择"""
    try:
        data = request.get_json()
        model_name = data.get('model', '')

        if not model_name:
            return jsonify({'success': False, 'error': '未提供模型名称'})

        main_js_path = PROJECT_ROOT / 'main.js'
        if main_js_path.exists():
            with open(main_js_path, 'r', encoding='utf-8') as f:
                main_content = f.read()

            # 将选中的模型放在第一位
            new_priority = f"const priorityFolders = ['{model_name}', 'Hiyouri', 'Default', 'Main']"
            main_content = re.sub(r"const priorityFolders = \[.*?\]", new_priority, main_content)

            with open(main_js_path, 'w', encoding='utf-8') as f:
                f.write(main_content)

            logger.info(f'已设置当前模型为：{model_name}')
            return jsonify({'success': True, 'message': f'已应用模型：{model_name}'})
        else:
            logger.error(f'main.js 不存在：{main_js_path}')
            return jsonify({'success': False, 'error': 'main.js 文件不存在'})
    except Exception as e:
        logger.error(f'保存模型失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/live2d/model/position/save', methods=['POST'])
def save_model_position():
    """保存 Live2D 模型位置"""
    try:
        from .config_manager import load_config, save_config

        data = request.get_json()
        x = data.get('x', 1.35)
        y = data.get('y', 0.8)

        config = load_config()
        if 'ui' not in config:
            config['ui'] = {}
        if 'model_position' not in config['ui']:
            config['ui']['model_position'] = {}

        config['ui']['model_position']['x'] = x
        config['ui']['model_position']['y'] = y
        config['ui']['model_position']['remember_position'] = True

        if save_config(config):
            return jsonify({'success': True, 'message': '皮套位置已保存，请重启桌宠生效'})
        return jsonify({'error': '保存失败'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@live2d_bp.route('/api/live2d/model/reset-position', methods=['POST'])
def reset_model_position():
    """复位 Live2D 模型位置到默认值"""
    try:
        from .config_manager import load_config, save_config

        config = load_config()

        default_x = 1.35
        default_y = 0.8

        if 'ui' not in config:
            config['ui'] = {}
        if 'model_position' not in config['ui']:
            config['ui']['model_position'] = {}

        config['ui']['model_position']['x'] = default_x
        config['ui']['model_position']['y'] = default_y
        config['ui']['model_position']['remember_position'] = True

        if save_config(config):
            return jsonify({'success': True, 'message': '皮套位置已保存，请重启桌宠生效'})
        return jsonify({'error': '保存失败'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ 动作管理 ============

@live2d_bp.route('/api/live2d/motions/categorized', methods=['GET'])
def get_categorized_motions():
    """获取已分类的动作列表（返回情绪分类及其绑定的文件路径）"""
    try:
        current_model = _get_current_model_name()
        all_data = load_emotion_actions()

        categorized = {}
        if current_model in all_data:
            emotion_actions = all_data[current_model].get('emotion_actions', {})
            for emotion in EMOTION_CATEGORIES:
                if emotion in emotion_actions:
                    categorized[emotion] = emotion_actions[emotion]

        return jsonify({'success': True, 'categorized': categorized})
    except Exception as e:
        logger.error(f'获取已分类动作失败：{str(e)}')
        return jsonify({'success': True, 'categorized': {}})


@live2d_bp.route('/api/live2d/motions/uncategorized', methods=['GET'])
def get_uncategorized_motions():
    """获取未分类的动作列表（返回键名是文件路径的映射）"""
    try:
        current_model = _get_current_model_name()
        all_data = load_emotion_actions()

        motion_map = {}
        if current_model in all_data:
            emotion_actions = all_data[current_model].get('emotion_actions', {})
            for key, motions in emotion_actions.items():
                if key not in EMOTION_CATEGORIES and motions:
                    motion_map[key] = motions[0]  # 取第一个文件路径

        return jsonify({'success': True, 'motions': motion_map})
    except Exception as e:
        logger.error(f'获取动作列表失败：{str(e)}')
        return jsonify({'success': True, 'motions': {}})


@live2d_bp.route('/api/live2d/motions/save', methods=['POST'])
def save_motions_config():
    """保存动作配置"""
    try:
        data = request.get_json()
        categories = data.get('categories', [])
        model_name = get_current_model()

        # 读取现有配置
        all_data = load_emotion_actions()

        # 初始化当前模型的数据
        if model_name not in all_data:
            all_data[model_name] = {}
        if 'emotion_actions' not in all_data[model_name]:
            all_data[model_name]['emotion_actions'] = {}

        # 更新情绪分类
        for category in categories:
            name = category.get('name')
            emotion = category.get('emotion')
            motions = category.get('motions', [])

            if name in EMOTION_CATEGORIES:
                all_data[model_name]['emotion_actions'][name] = motions

        save_emotion_actions(all_data)
        logger.info(f'已保存动作配置（模型：{model_name}）')

        return jsonify({'success': True, 'message': '动作配置已保存'})
    except Exception as e:
        logger.error(f'保存动作配置失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/live2d/motion/reset', methods=['POST'])
def reset_motion_config():
    """复位动作配置（从备份恢复）"""
    try:
        model_name = get_current_model()
        backup_path = PROJECT_ROOT / 'character_backups.json'
        config_path = PROJECT_ROOT / 'emotion_actions.json'

        if backup_path.exists():
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup = json.load(f)

            # 读取现有配置（保留其他模型的数据）
            existing_config = load_emotion_actions()

            # 从备份中提取当前模型的动作配置
            if model_name in backup:
                model_backup = backup[model_name]
                if 'original_config' in model_backup:
                    emotion_actions = model_backup['original_config'].get('emotion_actions', {})
                    existing_config[model_name] = {
                        'emotion_actions': emotion_actions
                    }
                else:
                    existing_config[model_name] = model_backup

                save_emotion_actions(existing_config)
                logger.info(f'动作配置已从备份恢复（模型：{model_name}）')
                return jsonify({'success': True, 'message': '动作配置已重置'})
            else:
                logger.warning(f'备份中没有模型 {model_name} 的数据')
                return jsonify({'success': False, 'error': '备份中没有该模型的数据'})
        else:
            logger.error(f'备份文件不存在：{backup_path}')
            return jsonify({'success': False, 'error': '备份文件不存在'})
    except Exception as e:
        logger.error(f'重置动作配置失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/live2d/motion/preview', methods=['POST'])
def preview_motion():
    """预览动作"""
    try:
        data = request.get_json()
        motion_name = data.get('motion', '')

        if not motion_name:
            return jsonify({'success': False, 'error': '未提供动作名称'})

        # 使用 trigger_emotion action 来触发情绪对应的动作
        json_data = json.dumps({
            'action': 'trigger_emotion',
            'emotion_name': motion_name
        }).encode('utf-8')
        req = urllib.request.Request('http://localhost:3002/control-motion', data=json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                return jsonify({'success': True, 'message': f'正在预览动作：{motion_name}'})

        return jsonify({'success': True, 'message': f'预览请求已发送：{motion_name}'})
    except Exception as e:
        logger.error(f'预览动作失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ 表情管理 ============

def get_current_model_for_expressions():
    """从 main.js 读取当前模型名称（用于表情配置）"""
    main_js_path = PROJECT_ROOT / 'main.js'
    if main_js_path.exists():
        content = main_js_path.read_text(encoding='utf-8')
        match = re.search(r"const priorityFolders = \['([^']+)'", content)
        if match:
            return match.group(1)
    return '肥牛'  # 默认角色


@live2d_bp.route('/api/live2d/expressions/config', methods=['GET'])
def get_expressions_config():
    """获取 Live2D 表情配置（从 emotion_expressions.json 读取当前模型的配置）"""
    try:
        config_path = PROJECT_ROOT / 'emotion_expressions.json'
        
        # 获取当前模型
        current_model = get_current_model_for_expressions()
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
            
            if current_model in all_data:
                model_data = all_data[current_model]
                emotion_expressions = model_data.get('emotion_expressions', {})
                
                # 分离情绪分类和可用表情
                expressions = {}
                available_expressions = {}
                
                for key, files in emotion_expressions.items():
                    if key in ['开心', '生气', '难过', '惊讶', '害羞', '俏皮']:
                        expressions[key] = files
                    else:
                        # 自定义表情（如"表情 1"）放入 available_expressions
                        if files:
                            available_expressions[key] = files[0]
                
                return jsonify({
                    'expressions': expressions,
                    'available_expressions': available_expressions
                })
        
        return jsonify({'expressions': {}, 'available_expressions': {}})
    except Exception as e:
        logger.error(f'获取表情配置失败：{str(e)}')
        return jsonify({'error': str(e)}), 500


@live2d_bp.route('/api/live2d/expressions/save', methods=['POST'])
def save_expressions():
    """保存 Live2D 表情配置到 emotion_expressions.json"""
    try:
        data = request.get_json()
        expressions = data.get('expressions', {})
        
        # 获取当前模型
        current_model = get_current_model_for_expressions()
        
        # 读取现有配置
        config_path = PROJECT_ROOT / 'emotion_expressions.json'
        all_data = {}
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
        
        # 初始化当前模型的数据
        if current_model not in all_data:
            all_data[current_model] = {}
        if 'emotion_expressions' not in all_data[current_model]:
            all_data[current_model]['emotion_expressions'] = {}
        
        # 合并情绪分类和自定义表情
        emotion_categories = ['开心', '生气', '难过', '惊讶', '害羞', '俏皮']
        
        # 保存情绪分类
        for emotion in emotion_categories:
            if emotion in expressions:
                all_data[current_model]['emotion_expressions'][emotion] = expressions[emotion]
        
        # 保存自定义表情（从 available_expressions 或 expressions 中提取）
        available_expressions = data.get('available_expressions', {})
        for key, files in expressions.items():
            if key not in emotion_categories and files:
                all_data[current_model]['emotion_expressions'][key] = files
        
        # 保存额外提供的 available_expressions
        for key, files in available_expressions.items():
            if isinstance(files, str):
                files = [files]
            all_data[current_model]['emotion_expressions'][key] = files
        
        # 保存配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f'已保存表情配置（模型：{current_model}）')
        return jsonify({'success': True, 'message': '表情配置已保存'})
    except Exception as e:
        logger.error(f'保存表情配置失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/live2d/expressions/reset', methods=['POST'])
def reset_expressions():
    """重置 Live2D 表情配置（从 character_backups.json 恢复）"""
    try:
        # 获取当前模型
        current_model = get_current_model_for_expressions()
        
        backup_path = PROJECT_ROOT / 'character_backups.json'
        config_path = PROJECT_ROOT / 'emotion_expressions.json'
        
        if backup_path.exists():
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup = json.load(f)
            
            # 读取现有配置（保留其他模型的数据）
            existing_config = {}
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)
            
            # 从备份中提取当前模型的表情配置
            if current_model in backup:
                model_backup = backup[current_model]
                if 'original_config' in model_backup:
                    emotion_expressions = model_backup['original_config'].get('emotion_expressions', {})
                    existing_config[current_model] = {
                        'emotion_expressions': emotion_expressions
                    }
                else:
                    # 兼容旧格式
                    existing_config[current_model] = model_backup
                
                # 保存配置
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(existing_config, f, indent=2, ensure_ascii=False)
                
                logger.info(f'表情配置已从备份恢复（模型：{current_model}）')
                return jsonify({'success': True, 'message': '表情配置已重置'})
            else:
                logger.warning(f'备份中没有模型 {current_model} 的数据')
                return jsonify({'success': False, 'error': '备份中没有该模型的数据'})
        else:
            logger.error(f'备份文件不存在：{backup_path}')
            return jsonify({'success': False, 'error': '备份文件不存在'})
    except Exception as e:
        logger.error(f'重置表情配置失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/live2d/expression/preview', methods=['POST'])
def preview_expression():
    """预览表情"""
    try:
        data = request.get_json()
        expression = data.get('expression', '')

        if not expression:
            return jsonify({'success': False, 'error': '未提供表情名称'})

        json_data = json.dumps({
            'action': 'trigger_expression',
            'expression_name': expression
        }).encode('utf-8')
        req = urllib.request.Request('http://localhost:3002/control-expression', data=json_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                return jsonify({'success': True, 'message': f'正在预览表情：{expression}'})

        return jsonify({'success': True, 'message': f'预览请求已发送：{expression}'})
    except Exception as e:
        logger.error(f'预览表情失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ 趣味面板 ============

@live2d_bp.route('/api/fun-panel/open', methods=['GET'])
def open_fun_panel():
    """在桌面应用中打开趣味面板"""
    try:
        # 尝试通过IPC发送消息到主应用
        # 这里我们返回成功，因为实际的IPC通信需要主应用配合
        logger.info('趣味面板打开请求已收到')
        return jsonify({'success': True, 'message': '趣味面板打开请求已发送'})
    except Exception as e:
        logger.error(f'打开趣味面板失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/fun-panel/switch-gender', methods=['POST'])
def switch_gender():
    """切换角色性别"""
    try:
        data = request.get_json()
        gender = data.get('gender', 'female')
        
        logger.info(f'切换角色请求：{gender}')
        
        # 尝试通过HTTP请求发送到主应用
        try:
            json_data = json.dumps({
                'action': 'switch_gender',
                'gender': gender
            }).encode('utf-8')
            req = urllib.request.Request('http://localhost:3002/control-fun-panel', data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return jsonify({'success': True, 'message': f'已切换为{"小艾" if gender == "female" else "小阳"}'})
        except Exception as e:
            logger.warning(f'通过HTTP切换角色失败：{e}')
        
        return jsonify({'success': True, 'message': '角色切换请求已发送'})
    except Exception as e:
        logger.error(f'切换角色失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/fun-panel/change-costume', methods=['POST'])
def change_costume():
    """换装"""
    try:
        data = request.get_json()
        costume = data.get('costume', 'default')
        
        logger.info(f'换装请求：{costume}')
        
        try:
            json_data = json.dumps({
                'action': 'change_costume',
                'costume': costume
            }).encode('utf-8')
            req = urllib.request.Request('http://localhost:3002/control-fun-panel', data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return jsonify({'success': True, 'message': '换装成功'})
        except Exception as e:
            logger.warning(f'通过HTTP换装失败：{e}')
        
        return jsonify({'success': True, 'message': '换装请求已发送'})
    except Exception as e:
        logger.error(f'换装失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/fun-panel/play-action', methods=['POST'])
def play_action():
    """播放动作"""
    try:
        data = request.get_json()
        motion = data.get('motion', '')
        
        if not motion:
            return jsonify({'success': False, 'error': '未提供动作名称'})
        
        logger.info(f'播放动作请求：{motion}')
        
        try:
            json_data = json.dumps({
                'action': 'play_motion',
                'motion': motion
            }).encode('utf-8')
            req = urllib.request.Request('http://localhost:3002/control-fun-panel', data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return jsonify({'success': True, 'message': '动作已播放'})
        except Exception as e:
            logger.warning(f'通过HTTP播放动作失败：{e}')
        
        return jsonify({'success': True, 'message': '动作播放请求已发送'})
    except Exception as e:
        logger.error(f'播放动作失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/fun-panel/set-expression', methods=['POST'])
def set_expression():
    """设置表情"""
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        
        if not expression:
            return jsonify({'success': False, 'error': '未提供表情名称'})
        
        logger.info(f'设置表情请求：{expression}')
        
        try:
            json_data = json.dumps({
                'action': 'set_expression',
                'expression': expression
            }).encode('utf-8')
            req = urllib.request.Request('http://localhost:3002/control-fun-panel', data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return jsonify({'success': True, 'message': '表情已设置'})
        except Exception as e:
            logger.warning(f'通过HTTP设置表情失败：{e}')
        
        return jsonify({'success': True, 'message': '表情设置请求已发送'})
    except Exception as e:
        logger.error(f'设置表情失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/fun-panel/play-effect', methods=['POST'])
def play_effect():
    """播放特效"""
    try:
        data = request.get_json()
        effect = data.get('effect', '')
        
        if not effect:
            return jsonify({'success': False, 'error': '未提供特效名称'})
        
        logger.info(f'播放特效请求：{effect}')
        
        try:
            json_data = json.dumps({
                'action': 'play_effect',
                'effect': effect
            }).encode('utf-8')
            req = urllib.request.Request('http://localhost:3002/control-fun-panel', data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return jsonify({'success': True, 'message': '特效已播放'})
        except Exception as e:
            logger.warning(f'通过HTTP播放特效失败：{e}')
        
        return jsonify({'success': True, 'message': '特效播放请求已发送'})
    except Exception as e:
        logger.error(f'播放特效失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/fun-panel/quick-interact', methods=['POST'])
def quick_interact():
    """快捷互动"""
    try:
        data = request.get_json()
        interact = data.get('interact', '')
        
        if not interact:
            return jsonify({'success': False, 'error': '未提供互动类型'})
        
        logger.info(f'快捷互动请求：{interact}')
        
        try:
            json_data = json.dumps({
                'action': 'quick_interact',
                'interact': interact
            }).encode('utf-8')
            req = urllib.request.Request('http://localhost:3002/control-fun-panel', data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return jsonify({'success': True, 'message': '互动已触发'})
        except Exception as e:
            logger.warning(f'通过HTTP触发互动失败：{e}')
        
        return jsonify({'success': True, 'message': '互动触发请求已发送'})
    except Exception as e:
        logger.error(f'触发互动失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ 模型切换管理 ============

@live2d_bp.route('/api/models/available', methods=['GET'])
def get_available_models():
    """获取所有可用模型列表"""
    try:
        models = {
            'live2d': [],
            'vrm': []
        }
        
        live2d_dir = PROJECT_ROOT / '2D'
        if live2d_dir.exists():
            for model_dir in live2d_dir.iterdir():
                if model_dir.is_dir():
                    model3_json = None
                    for f in model_dir.iterdir():
                        if f.suffix == '.json' and 'model3' in f.name:
                            model3_json = f.name
                            break
                    
                    if model3_json:
                        model_info = {
                            'name': model_dir.name,
                            'path': f'2D/{model_dir.name}/{model3_json}',
                            'type': 'live2d'
                        }
                        
                        vrm_file = list(model_dir.glob('*.vrm'))
                        if vrm_file:
                            model_info['vrm_path'] = f'2D/{model_dir.name}/{vrm_file[0].name}'
                        
                        models['live2d'].append(model_info)
        
        vrm_dir = PROJECT_ROOT / '3D'
        if vrm_dir.exists():
            for vrm_file in vrm_dir.glob('*.vrm'):
                models['vrm'].append({
                    'name': vrm_file.stem,
                    'path': f'3D/{vrm_file.name}',
                    'type': 'vrm'
                })
        
        return jsonify({'success': True, 'models': models})
    except Exception as e:
        logger.error(f'获取模型列表失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/models/current', methods=['GET'])
def get_current_model_info():
    """获取当前模型信息"""
    try:
        current_model = _get_current_model_name()
        
        config_path = PROJECT_ROOT / 'config.json'
        model_type = 'live2d'
        vrm_path = ''
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                model_type = config.get('ui', {}).get('model_type', 'live2d')
                vrm_path = config.get('ui', {}).get('vrm_model_path', '')
        
        return jsonify({
            'success': True,
            'current': {
                'name': current_model,
                'type': model_type,
                'vrm_path': vrm_path
            }
        })
    except Exception as e:
        logger.error(f'获取当前模型失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/models/switch', methods=['POST'])
def switch_model():
    """切换模型"""
    try:
        data = request.get_json()
        model_name = data.get('model', '')
        model_type = data.get('type', 'live2d')
        
        if not model_name:
            return jsonify({'success': False, 'error': '未提供模型名称'})
        
        logger.info(f'切换模型请求: {model_name} (类型: {model_type})')
        
        config_path = PROJECT_ROOT / 'config.json'
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if 'ui' not in config:
                config['ui'] = {}
            
            config['ui']['model_type'] = model_type
            
            if model_type == 'live2d':
                main_js_path = PROJECT_ROOT / 'main.js'
                if main_js_path.exists():
                    with open(main_js_path, 'r', encoding='utf-8') as f:
                        main_content = f.read()
                    
                    new_priority = f"const priorityFolders = ['{model_name}', 'Hiyouri', 'Default', 'Main']"
                    main_content = re.sub(r"const priorityFolders = \[.*?\]", new_priority, main_content)
                    
                    with open(main_js_path, 'w', encoding='utf-8') as f:
                        f.write(main_content)
                
                live2d_dir = PROJECT_ROOT / '2D' / model_name
                if live2d_dir.exists():
                    for f in live2d_dir.iterdir():
                        if f.suffix == '.json' and 'model3' in f.name:
                            config['ui']['live2d_model_path'] = f'2D/{model_name}/{f.name}'
                            break
            
            elif model_type == 'vrm':
                vrm_path = data.get('path', f'3D/{model_name}.vrm')
                config['ui']['vrm_model_path'] = vrm_path
                config['ui']['vrm_model'] = model_name
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        
        try:
            json_data = json.dumps({
                'action': 'switch_model',
                'model': model_name,
                'type': model_type
            }).encode('utf-8')
            req = urllib.request.Request('http://localhost:3002/control-model', data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return jsonify({'success': True, 'message': f'已切换到模型: {model_name}'})
        except Exception as e:
            logger.warning(f'通过HTTP切换模型失败：{e}')
        
        return jsonify({'success': True, 'message': f'模型切换配置已保存，请重启桌宠生效'})
    except Exception as e:
        logger.error(f'切换模型失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/models/state', methods=['GET'])
def get_model_state():
    """获取模型状态（用于实时同步）"""
    try:
        state_file = PROJECT_ROOT / 'data' / 'model_state.json'
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
            return jsonify({'success': True, 'state': state})
        
        return jsonify({
            'success': True,
            'state': {
                'type': 'live2d',
                'name': get_current_model(),
                'visible': True,
                'motion': None,
                'expression': None
            }
        })
    except Exception as e:
        logger.error(f'获取模型状态失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/models/state', methods=['POST'])
def update_model_state():
    """更新模型状态（由前端调用）"""
    try:
        data = request.get_json()
        state_file = PROJECT_ROOT / 'data' / 'model_state.json'
        
        state_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f'更新模型状态失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/models/visibility', methods=['POST'])
def set_model_visibility():
    """设置模型可见性"""
    try:
        data = request.get_json()
        visible = data.get('visible', True)
        
        try:
            json_data = json.dumps({
                'action': 'set_visibility',
                'visible': visible
            }).encode('utf-8')
            req = urllib.request.Request('http://localhost:3002/control-model', data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return jsonify({'success': True, 'message': f'模型已{"显示" if visible else "隐藏"}'})
        except Exception as e:
            logger.warning(f'通过HTTP设置可见性失败：{e}')
        
        return jsonify({'success': True, 'message': '可见性设置请求已发送'})
    except Exception as e:
        logger.error(f'设置模型可见性失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/models/motion', methods=['POST'])
def play_model_motion():
    """播放模型动作"""
    try:
        data = request.get_json()
        motion = data.get('motion', '')
        
        if not motion:
            return jsonify({'success': False, 'error': '未提供动作名称'})
        
        try:
            json_data = json.dumps({
                'action': 'play_motion',
                'motion': motion
            }).encode('utf-8')
            req = urllib.request.Request('http://localhost:3002/control-model', data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return jsonify({'success': True, 'message': f'动作已播放: {motion}'})
        except Exception as e:
            logger.warning(f'通过HTTP播放动作失败：{e}')
        
        return jsonify({'success': True, 'message': '动作播放请求已发送'})
    except Exception as e:
        logger.error(f'播放动作失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@live2d_bp.route('/api/models/expression', methods=['POST'])
def set_model_expression():
    """设置模型表情"""
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        
        if not expression:
            return jsonify({'success': False, 'error': '未提供表情名称'})
        
        try:
            json_data = json.dumps({
                'action': 'set_expression',
                'expression': expression
            }).encode('utf-8')
            req = urllib.request.Request('http://localhost:3002/control-model', data=json_data, method='POST')
            req.add_header('Content-Type', 'application/json')
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    return jsonify({'success': True, 'message': f'表情已设置: {expression}'})
        except Exception as e:
            logger.warning(f'通过HTTP设置表情失败：{e}')
        
        return jsonify({'success': True, 'message': '表情设置请求已发送'})
    except Exception as e:
        logger.error(f'设置表情失败：{str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500
