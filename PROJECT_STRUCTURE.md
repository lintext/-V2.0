# 桌面宠物AI应用程序 - 项目结构说明

## 📁 标准目录结构

```
live-2d/
│
├── 🎯 一键启动脚本（核心）
│   ├── 一键启动.bat              # 主启动脚本 - 一键运行所有服务
│   ├── stop_services.bat         # 服务停止脚本
│   ├── 项目清理工具.bat          # 清理临时文件和优化项目
│   └── 系统诊断工具.bat          # 系统环境检测和诊断
│
├── ⚙️ 配置文件
│   ├── config.json               # 主配置文件（模型、AI、UI设置）
│   ├── package.json              # Node.js项目配置
│   ├── package-lock.json         # 依赖锁定文件
│   ├── emotion_actions.json      # 情绪动作映射
│   └── emotion_expressions.json  # 表情配置
│
├── 🖥️ Electron主程序
│   ├── main.js                   # Electron主进程
│   ├── app.js                    # 应用初始化
│   ├── index.html                # 主界面HTML
│   └── go.bat                    # 传统启动方式（备用）
│
├── 🌐 WebUI控制面板
│   └── webui/                    # Flask Web应用
│       ├── main_app.py           # 主应用入口
│       ├── templates/            # HTML模板
│       ├── static/               # 静态资源
│       └── routes/               # 路由处理
│
├── 🎨 前端资源
│   ├── css/                      # 样式表
│   │   └── styles.css
│   ├── libs/                     # 第三方库
│   │   ├── live2d.min.js
│   │   ├── pixi.min.js
│   │   └── ...
│   └── js/                       # JavaScript源码
│       ├── core/                 # 核心框架
│       ├── ai/                   # AI功能模块
│       ├── ui/                   # UI控制器
│       ├── model/                # 模型管理
│       ├── services/             # 服务层
│       ├── voice/                # 语音处理
│       └── utils/                # 工具函数
│
├── 🎭 角色模型
│   ├── 2D/                       # Live2D模型
│   │   ├── xiaoai/               # 小艾同学（默认角色）
│   │   │   ├── hiyori_pro_t11.model3.json
│   │   │   ├── motions/          # 动作文件
│   │   │   ├── expressions/      # 表情文件
│   │   │   └── hiyori_pro_t11.2048/  # 纹理贴图
│   │   └── 小艾/                 # 备用角色（肥牛）
│   │       └── feiniu.model3.json
│   └── 3D/                       # VRM模型
│       └── Sample_A.vrm
│
├── 🔌 插件系统
│   └── plugins/
│       ├── built-in/             # 内置插件
│       │   ├── auto-chat/        # 自动聊天
│       │   ├── memos/            # 记忆系统
│       │   ├── mood-chat/        # 情绪聊天
│       │   ├── diary/            # 日记功能
│       │   └── ...
│       └── community/            # 社区插件
│           ├── check-in/         # 签到系统
│           ├── notes/            # 笔记功能
│           └── ...
│
├── 🤖 MCP工具集成
│   └── mcp/
│       ├── mcp_config.json       # MCP配置
│       ├── tools/                # 工具定义
│       └── update-config.js      # 配置更新器
│
├── 💾 数据存储
│   ├── data/                     # 运行时数据
│   │   ├── model_state.json      # 模型状态
│   │   └── webui_port.txt        # WebUI端口记录
│   ├── logs/                     # 日志文件
│   ├── AI记录室/                  # 对话历史和记忆库
│   └── Voice_Model_Factory/      # 语音模型工厂
│
├── 🔧 辅助工具脚本
│   ├── start.py                  # Python启动器
│   ├── run_webui.py              # WebUI独立运行
│   ├── set_live2d.py             # Live2D设置
│   ├── AI_set_live2d.py          # AI配置Live2D
│   ├── init_mysql.py             # MySQL初始化
│   └── test-panel.html           # 测试面板
│
└── 📚 文档
    ├── BODY_MOTION_SYSTEM.md     # 身体动作系统说明
    ├── DEBUG_GUIDE.md            # 调试指南
    └── TESTING_GUIDE.md          # 测试指南
```

## 🚀 快速开始指南

### 方法1：一键启动（推荐）

**双击运行 `一键启动.bat`**

该脚本将自动完成以下操作：
1. ✅ 检查Python、Node.js、npm环境
2. ✅ 验证项目文件完整性
3. ✅ 检查端口占用情况
4. ✅ 安装/更新依赖包
5. ✅ 清理临时文件
6. ✅ 启动WebUI控制面板（端口5001）
7. ✅ 启动Electron桌面宠物
8. ✅ 自动打开浏览器访问控制面板

### 方法2：手动分步启动

#### 步骤1：启动WebUI控制面板
```bash
cd live-2d
python -c "from webui import run_app; run_app()"
```
或双击：`启动 WebUI 控制面板.bat`

#### 步骤2：启动桌面宠物
```bash
npm start
```
或双击：`go.bat`

## ⌨️ 可用快捷键

| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Ctrl+Q` | 退出应用 | 安全关闭所有服务 |
| `Ctrl+G` | 打断语音 | 中止当前TTS播放 |
| `Ctrl+T` | 强制置顶 | 将窗口置于最前 |
| `Ctrl+Shift+1~9` | 触发动作 | 执行预设动作1-9 |
| `Ctrl+Shift+0` | 停止动作 | 停止所有正在执行的动作 |
| `Ctrl+Shift+6` | 随机音乐 | 播放随机背景音乐 |
| `Ctrl+M` | 切换气泡框 | 显示/隐藏聊天对话框 |

## 🔧 维护工具

### 项目清理
**运行 `项目清理工具.bat`**
- 删除临时文件（.tmp, .bak等）
- 清理缓存目录（__pycache__, .cache等）
- 清空日志文件
- 整理目录结构
- 生成清理报告

### 系统诊断
**运行 `系统诊断工具.bat`**
- 检查操作系统信息
- 验证Python/Node.js环境
- 检测项目文件完整性
- 监控端口占用情况
- 查看进程运行状态
- 分析系统资源使用
- 生成详细诊断报告

### 停止服务
**运行 `stop_services.bat`**
- 安全停止Electron进程
- 终止WebUI服务
- 关闭Node.js后台进程
- 清理临时PID文件

## 📊 服务架构图

```
用户界面层
├── Electron桌面宠物 (透明窗口)
│   ├── Live2D模型渲染
│   ├── UI交互控制
│   └── 全局快捷键监听
│
└── WebUI控制面板 (浏览器)
    ├── 配置管理
    ├── 插件管理
    ├── 日志查看
    └── 系统监控
    
业务逻辑层
├── AI对话引擎 (LLM)
│   ├── 上下文管理
│   ├── 记忆系统
│   └── 多模态处理
│
├── 动作控制系统
│   ├── Live2D动作播放
│   ├── 表情切换
│   └── 身体动作
│
└── 语音处理
    ├── ASR语音识别
    ├── TTS语音合成
    └── 音乐播放

数据持久层
├── SQLite数据库
├── JSON配置文件
└── 文本日志
```

## ⚠️ 注意事项

### 首次运行
1. **确保已安装**：
   - Python 3.8+
   - Node.js 16+
   - npm 7+

2. **安装Python依赖**：
   ```bash
   pip install flask requests numpy pillow
   ```

3. **安装Node.js依赖**：
   ```bash
   npm install
   ```

### 常见问题解决

#### 问题1：端口被占用
**症状**：WebUI无法启动，提示端口5001已被占用  
**解决方案**：
1. 运行 `系统诊断工具.bat` 查看占用进程
2. 运行 `stop_services.bat` 停止相关服务
3. 或修改 `config.json` 中的端口号

#### 问题2：Python未找到
**症状**：提示"python不是内部或外部命令"  
**解决方案**：
1. 确认Python已正确安装
2. 将Python添加到系统PATH环境变量
3. 重启命令行窗口

#### 问题3：桌面宠物不显示
**症状**：Electron启动但看不到宠物  
**解决方案**：
1. 检查 `config.json` 中的 `model_type` 设置
2. 确认模型文件存在于 `2D/xiaoai/` 目录
3. 尝试切换为VRM模式：将 `model_type` 改为 `"vrm"`

#### 问题4：内存占用过高
**症状**：系统运行缓慢，任务管理器显示高内存使用  
**解决方案**：
1. 运行 `项目清理工具.bat` 清理缓存
2. 关闭不必要的浏览器标签页
3. 在 `config.json` 中禁用不需要的功能

## 📈 性能优化建议

1. **禁用不必要的插件**：在WebUI中关闭未使用的插件
2. **调整模型质量**：降低Live2D模型精度以节省GPU
3. **限制对话历史**：减少上下文消息数量
4. **定期清理日志**：每周运行一次清理工具
5. **监控资源使用**：定期运行诊断工具检查系统健康状态

## 🔄 更新与维护

### 更新依赖
```bash
# 更新Node.js依赖
npm update

# 更新Python依赖
pip install --upgrade flask requests numpy pillow
```

### 备份重要数据
- `config.json` - 自定义配置
- `data/model_state.json` - 模型状态
- `AI记录室/` - 对话历史和记忆
- `plugins/` - 自定义插件配置

### 版本回滚
如遇新版本问题，可从Git仓库恢复：
```bash
git checkout <previous-version-tag>
npm install
```

---

## 📞 技术支持

如遇到问题：
1. 查看 `logs/` 目录下的日志文件
2. 运行 `系统诊断工具.bat` 生成诊断报告
3. 检查 `error_log.txt` 错误日志
4. 参考项目文档解决问题

---

**最后更新时间**：2026-04-04  
**脚本版本**：v2.0  
**适用平台**：Windows 10/11