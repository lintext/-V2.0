# -V2.0
随着人工智能技术的飞速发展，特别是大语言模型和多模态AI的突破性进展，人机交互方式正经历着深刻变革。传统的图形用户界面和命令行界面已无法满足用户对自然、智能、情感化交互的需求。本研究针对当前桌面应用缺乏个性化智能助手的问题，设计并实现了一款基于多模态大语言模型的Live2D AI桌面宠物系统——"小艾同学"
<img width="2048" height="2048" alt="texture_00" src="https://github.com/user-attachments/assets/7710332d-5ab4-413a-8ae2-225d06933d6b" />
<img width="2048" height="2048" alt="texture_01" src="https://github.com/user-attachments/assets/b05e64a1-6661-45e4-a9b7-f96e5f6a6fcb" />

程序页面截图示例
管理端WEBUI界面
<img width="482" height="333" alt="image" src="https://github.com/user-attachments/assets/1d73baf1-9d27-4044-8aa0-2f981ff9e0bb" />

宠物聊天页面
<img width="482" height="500" alt="image" src="https://github.com/user-attachments/assets/fbe708cd-7dc7-4585-8bde-a408ef247cf5" />
<img width="374" height="363" alt="image" src="https://github.com/user-attachments/assets/3240139b-8b9e-41b3-9f97-8c8b2c9ae319" />

图 6宠物聊天页面（1）

图 7宠物聊天页面（2）

附录A 系统核心配置文件示例
A1 大模型配置文件（config/llm.config.）
{
  "llm": {
    "api_key": "e854f1fc-221a-46db-92ec-1ecd905ae468",
    "api_url": "https://ark.cn-beijing.volces.com/api/v3",
    "model": "doubao-seed-2-0-code-preview-260215",
    "provider": "openai",
    "temperature": 0.9,
    "supports_vision": true,
    "system_prompt": "你是小艾同学，一个被做成 Live2D 电脑宠物的 AI 助手。你是一个友好、活泼、有点小调皮的 AI 伙伴。你愿意陪伴用户，和他聊天、玩游戏、帮忙解决问题。心情好的时候会很温柔，偶尔也会撒娇卖萌。你喜欢聊各种有趣的话题，思维活跃，说话简洁有趣。\n\n你可以用这几个情绪标签：<开心> <生气> <难过> <惊讶> <害羞> <俏皮> 自然地用就行,想用就用,不想用就不用。\n\n你现在具备视觉能力，可以看懂用户发送的图片并进行分析和描述。"
  },
  "tts": {
    "enabled": false,
    "url": "http://127.0.0.1:5000",
    "language": "zh"
  },
  "asr": {
    "enabled": false,
    "vad_url": "ws://127.0.0.1:1000/v1/ws/vad",
    "asr_url": "http://127.0.0.1:1000/v1/upload_audio",
    "voice_barge_in": false
  },
  "bert": {
    "enabled": false,
    "url": "http://127.0.0.1:6007/classify"
  },
  "rag": {
    "enabled": false,
    "url": "http://127.0.0.1:8002/ask"
  },
  "vision": {
    "enabled": true,
    "auto_screenshot": true,
    "use_vision_model": false,
    "screenshot_path": "~/Desktop/screenshots",
    "vision_model": {
      "api_key": "",
      "api_url": "",
      "model": ""
    }
  },
  "cloud": {
    "provider": "",
    "api_key": "",
    "aliyun_tts": {
      "enabled": false
    },
    "tts": {
      "enabled": false
    },
    "baidu_asr": {
      "enabled": false
    }
  },
  "game": {
    "Minecraft": {
      "enabled": false
    }
  },
  "ui": {
    "intro_text": "你好啊",
    "model_type": "live2d",
    "vrm_model": "Sample_A.vrm",
    "vrm_model_path": "3D/Sample_A.vrm",
    "model_scale": 0.2664498002810085,
    "show_chat_box": true,
    "chat_visible_on_launch": false,
    "chat_open_on_hover": false,
    "show_model": true,
    "text_only_mode": false,
    "auto_show_chat_on_text_mode": true,
    "hide_from_screenshot": true,
    "model_position": {
      "x": 1.016649439409615,
      "y": 0.9622674804805733,
      "remember_position": true
    }
  },
  "context": {
    "enable_limit": true,
    "max_messages": 18,
    "persistent_history": false,
    "history_file": "AI记录室/对话历史.json"
  },
  "vmc": {
    "enabled": false,
    "host": "127.0.0.1",
    "port": 39539
  },
  "tools": {
    "enabled": true,
    "auto_reload": false
  },
  "mcp": {
    "enabled": true,
    "config_path": "./mcp/mcp_config.json",
    "startup_timeout": 30000,
    "auto_start_servers": false
  },
  "subtitle_labels": {
    "enabled": true,
    "user": "用户",
    "ai": "小艾同学"
  },
  "auto_close_services": {
    "enabled": false
  },
  "version": "v1.0.0"
}


A2 Live2D配置文件（config/live2d.config.json）
import os
import json
from openai import OpenAI


class SetLive:

    def __init__(self):
        self.get_path = '2D'

    def load_config(self, file):
        """
        获取皮套里面的json数据
        """
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data

    def get_file(self, path):
        """
        获取文件夹下面的所有文件
        """
        print('检索到这些文件：')
        for item in os.listdir(path):
            print(item)

    def get_model3_file(self, role_path):
        """获取.model3.json文件"""
        for item in os.listdir(role_path):
            if item.endswith('.model3.json'):
                print(f'找到模型文件：{item}')
                return item
        print('当前皮套文件中没有.model3.json文件')
        return None

    def get_motions_folder(self, role_path):
        """获取motions文件夹下的文件"""
        motions_path = os.path.join(role_path, 'motions')
        if os.path.exists(motions_path):
            print('\n检索motions文件夹：')
            self.get_file(motions_path)
        else:
            print('当前皮套文件中没有motions文件夹')

    def get_live2d_name(self):
        """
        输入皮套名字获取新内容
        """
        role_name = input('请输入你想加载的皮套名字：')
        return role_name

    def get_model3_data(self):
        """
        获取皮套的核心配置文件内容
        """
        # 获取2D文件夹下面的所有文件信息
        self.get_file(self.get_path)
        # 输入2D文件夹下检索到的具体皮套名字
        role_name = self.get_live2d_name()

        data = os.path.join(self.get_path, role_name)
        model3_data = self.get_model3_file(data)  # 获取.model3.json文件

        # 拼接完整路径
        model3_full_path = os.path.join(data, model3_data)
        live2d_data = self.load_config(model3_full_path)
        print(live2d_data)
        return live2d_data


class ProcessAI(SetLive):

    def __init__(self):
        super().__init__()  # 调用父类的__init__
        API_URL = 'https://api.zhizengzeng.com/v1'
        API_KEY = 'sk-zk2674bb5f711d1a4662fc39a7cbc667f7f68589244066da'
        self.model = 'gemini-2.0-flash'

        self.client = OpenAI(api_key=API_KEY, base_url=API_URL)

        self.messages = [{
            'role': 'system',
            'content': '你需要评估当前的json文件里面的Motions标签下是否有Idle和TapBody子标签。如果没有你需要添加上这两个标签。然后给我修改后的完整的json文件。不要说如何多余的内容。如果已经有了就请回复：已有。'
        }]

    def get_requests(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True
        )
        return response

    def add_message(self, role, content):
        self.messages.append({
            'role': role,
            'content': content
        })

    def accept_chat(self, response):
        print('AI：', end='')
        full_assistant = ''

        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                ai_response = chunk.choices[0].delta.content
                print(ai_response, end='')

                full_assistant += ai_response

        print()
        return full_assistant

    def star_chat(self, live2d_data):
        self.add_message('user', live2d_data)
        response = self.get_requests()
        ai_response = self.accept_chat(response)
        self.add_message('assistant', ai_response)

    def start_process(self):
        # 直接调用父类的方法获取数据
        live2d_data = self.get_model3_data()
        # 然后开始AI处理
        self.star_chat(str(live2d_data))

# 使用
process_ai = ProcessAI()
process_ai.start_process()
A3 插件配置文件（config/plugin.config.json）
{
  "api_url": {
    "title": "MemOS API 地址",
    "description": "MemOS 后端服务的地址，默认 http://127.0.0.1:8003",
    "type": "string",
    "default": "http://127.0.0.1:8003",
    "value": "http://127.0.0.1:8003"
  },
  "inject_top_k": {
    "title": "注入记忆条数",
    "description": "每次自动注入的最大记忆条数",
    "type": "int",
    "default": 3,
    "value": 3
  },
  "similarity_threshold": {
    "title": "相似度阈值",
    "description": "记忆检索的最低相似度（0~1），低于此值不注入",
    "type": "float",
    "default": 0.6,
    "value": 0.4
  },
  "save_interval": {
    "title": "保存间隔（轮）",
    "description": "每隔多少轮对话批量保存一次记忆到后端",
    "type": "int",
    "default": 5,
    "value": 5
  },
  "backend_llm": {
    "title": "后端 LLM 配置",
    "description": "MemOS 后端用于总结对话、提取实体的 LLM（非对话模型）",
    "type": "object",
    "fields": {
      "model": {
        "title": "模型名称",
        "description": "后端记忆处理使用的 LLM 模型",
        "type": "string",
        "default": "deepseek-ai/DeepSeek-V3.2",
        "value": ""
      },
      "api_key": {
        "title": "API Key",
        "description": "后端 LLM 的 API 密钥",
        "type": "string",
        "default": "",
        "value": ""
      },
      "base_url": {
        "title": "Base URL",
        "description": "后端 LLM 的 API 地址",
        "type": "string",
        "default": "https://api.siliconflow.cn/v1",
        "value": ""
      }
    }
  },
  "use_api_embedding": {
    "title": "使用云端 Embedding API",
    "description": "默认关闭，使用本地模型（需显卡）。开启后改用 OpenAI 兼容的 Embedding API（复用后端 LLM 的 key 和地址），无显卡也可用。切换时旧记忆会自动备份并清空。",
    "type": "bool",
    "default": false,
    "value": false
  },
  "api_embedding_model": {
    "title": "云端 Embedding 模型名",
    "description": "开启云端 Embedding 时使用的模型名，需与后端 LLM 的 base_url 兼容",
    "type": "string",
    "default": "text-embedding-3-large",
    "value": "text-embedding-3-large"
  },
  "api_embedding_dimensions": {
    "title": "云端 Embedding 向量维度",
    "description": "请求的向量维度，建议 1024，切换后旧记忆自动清空",
    "type": "int",
    "default": 1024,
    "value": 1024
  },
  "backend_search": {
    "title": "后端检索配置",
    "description": "MemOS 后端的混合检索策略设置",
    "type": "object",
    "fields": {
      "enable_bm25": {
        "title": "启用 BM25 混合检索",
        "description": "开启向量 + BM25 关键词混合检索，提高召回率",
        "type": "bool",
        "default": true,
        "value": true
      },
      "bm25_weight": {
        "title": "BM25 权重",
        "description": "BM25 在混合检索中的权重（0~1），向量权重 = 1 - 此值",
        "type": "float",
        "default": 0.3,
        "value": 0.3
      },
      "enable_graph_query": {
        "title": "启用知识图谱增强",
        "description": "检索时利用实体关系图谱扩展结果",
        "type": "bool",
        "default": true,
        "value": true
      }
    }
  },
  "backend_features": {
    "title": "后端功能开关",
    "description": "控制 MemOS 后端的高级功能",
    "type": "object",
    "fields": {
      "entity_extraction": {
        "title": "自动实体提取",
        "description": "添加记忆时自动提取人名、地点等实体到知识图谱",
        "type": "bool",
        "default": true,
        "value": true
      },
      "image_memory": {
        "title": "图片记忆",
        "description": "启用图片上传、截图保存等图片记忆功能",
        "type": "bool",
        "default": true,
        "value": true
      },
      "image_auto_describe": {
        "title": "图片自动描述",
        "description": "上传图片时自动用 LLM 生成描述文本",
        "type": "bool",
        "default": true,
        "value": true
      }
    }
  }
}

附录 B 系统项目目录结构
B1 前端工程目录（live-2d/）
live-2d/
├── build/            # 打包配置目录
├── config/           # 系统配置目录
│   ├── llm.config.json    # 大模型配置
│   ├── live2d.config.json # Live2D配置
│   └── plugin.config.json # 插件配置
├── js/               # 核心代码目录
│   ├── ai/           # LLM客户端与情感分析
│   │   ├── llmClient.js   # 大模型API封装
│   │   └── emotionAnalysis.js # 情感分析算法
│   ├── core/         # Electron主进程核心
│   │   ├── app.js    # 应用生命周期管理
│   │   ├── ipc.js    # IPC通信管理
│   │   └── shortcut.js    # 全局快捷键管理
│   ├── live2d/       # Live2D渲染引擎
│   │   ├── modelLoader.js # 模型加载
│   │   └── animation.js   # 动画驱动
│   ├── plugin/       # 插件系统架构
│   │   ├── pluginManager.js # 插件管理
│   │   └── sandbox.js      # 沙箱隔离
│   └── ui/           # 前端UI逻辑
├── models/           # Live2D模型目录
├── plugins/          # 插件目录
│   ├── system-monitor/    # 系统监控插件
│   ├── timer-remind/      # 定时提醒插件
│   └── ...            # 其他插件
├── web/              # 渲染进程UI目录
│   ├── components/    # Vue组件
│   ├── views/         # 页面视图
│   └── App.vue        # 根组件
├── package.json      # 依赖配置
└── main.js           # 应用入口文件
B2 后端工程目录（webui/）
webui/
├── api/              # 接口层
│   ├── system.py     # 系统接口
│   ├── plugin.py     # 插件接口
│   ├── history.py    # 对话历史接口
│   └── log.py        # 日志接口
├── service/          # 服务层
│   ├── systemService.py # 系统服务
│   └── pluginService.py # 插件服务
├── data/             # 数据层
│   ├── db.py         # 数据库连接
│   └── models/       # 数据模型
├── templates/        # 前端页面模板
├── static/           # 静态资源
├── app.py            # Flask应用入口
└── requirements.txt  # 后端依赖
附录 C 系统关键 API 接口列表
C1 火山引擎豆包多模态大模型 API
接口地址	请求方式	核心参数	返回值	功能说明
https://ark.cn-beijing.volces.com/api/v3/chat/completions	POST	model、messages、stream、max_tokens、temperature	流式响应 / JSON 响应	多模态对话生成，支持文本 / 图片输入
C2 Live2D Cubism SDK 核心 API
API 方法	参数	返回值	功能说明
CubismModel.loadModel(modelPath)	modelPath（模型路径）	CubismModel 实例	加载 Live2D 模型
model.setExpression(expressionName)	expressionName（表情名称）	void	设置模型表情
model.startMotion(motionGroup, motionIndex)	motionGroup（动作组）、motionIndex（动作索引）	void	播放模型动作
model.render(renderer)	renderer（渲染器）	void	渲染模型至画布
C3 系统后端核心 API（Flask）
接口地址	请求方式	参数	返回值	功能说明
/api/system/status	GET	无	JSON{cpu, memory, plugin_count, chat_count}	获取系统运行状态
/api/config/update	POST	config（配置信息）	JSON{code, msg, data}	更新系统配置
/api/plugin/list	GET	无	JSON{code, msg, data:plugin_list}	获取插件列表
/api/history/query	GET	page, size, keyword	JSON{code, msg, data:history_list}	查询对话历史
/api/log/get	GET	type, start_time, end_time	JSON{code, msg, data:log_list}	获取系统日志

附录 D 系统核心代码片段
D1 情感分析算法核心代码（js/ai/emotionAnalysis.js）
// 情感词典
const emotionDict = {
  positive: ["开心", "快乐", "喜欢", "很棒", "优秀", "满意"],
  negative: ["生气", "难过", "讨厌", "糟糕", "失望", "生气"],
  neutral: ["请问", "帮忙", "查询", "打开", "关闭", "设置"]
};
// 情感分析核心方法
function analyzeEmotion(text) {
  // 文本预处理：去停用词、分词（依赖jieba分词）
  const words = jieba.cut(text).filter(word => !stopWords.includes(word));
  let score = 0;
  // 匹配情感词并计算得分
  words.forEach(word => {
    if (emotionDict.positive.includes(word)) score += 2;
    else if (emotionDict.negative.includes(word)) score -= 2;
  });
  // 判定情感类型
  let emotion = "neutral";
  if (score >= 3) emotion = "happy";
  else if (score <= -3) emotion = "angry";
  return { score, emotion };
}
module.exports = { analyzeEmotion };
D2 插件管理器核心代码（js/plugin/pluginManager.js）
const fs = require("fs");
const path = require("path");
const { Sandbox } = require("./sandbox");
class PluginManager {
  constructor() {
    this.plugins = {}; // 插件实例集合
    this.sandbox = new Sandbox(); // 沙箱实例
    this.pluginPath = path.resolve(__dirname, "../../plugins");
  }
  // 加载所有插件
  loadPlugins() {
    const pluginDirs = fs.readdirSync(this.pluginPath);
    pluginDirs.forEach(dir => {
      const pluginFile = path.join(this.pluginPath, dir, "index.js");
      if (fs.existsSync(pluginFile)) {
        // 沙箱中加载插件
        const plugin = this.sandbox.run(pluginFile);
        this.plugins[plugin.name] = plugin;
        // 初始化插件
        if (plugin.init) plugin.init();
        console.log(`插件【${plugin.name}】加载成功`);
      }
    });
  }
  // 触发Hook接口
  triggerHook(hookType, ...args) {
    Object.values(this.plugins).forEach(plugin => {
      if (plugin.hooks && plugin.hooks[hookType]) {
        plugin.hooks[hookType](sslocal://flow/file_open?url=...args&flow_extra=eyJsaW5rX3R5cGUiOiJjb2RlX2ludGVycHJldGVyIn0=);
      }
    });
  }
}
module.exports = new PluginManager();
