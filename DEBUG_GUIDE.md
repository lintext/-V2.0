# 🔧 调试模式启动指南

## 🚀 快速开始（3步完成）

### 步骤1: 确认应用已运行
应用程序应该在后台运行中。如果未运行，请执行：
```bash
cd d:\RuanJian\TRAE\Project\my-neuro-main\my-neuro-main\live-2d
npm start
```

### 步骤2: 打开开发者工具
在Electron窗口中按：
- **Windows/Linux**: `F12` 或 `Ctrl+Shift+I`
- **Mac**: `Cmd+Option+I`

### 步骤3: 运行调试测试
在控制台（Console标签页）中输入以下命令之一：

#### 选项A: 运行完整调试测试（推荐）
```javascript
// 复制并粘贴到控制台，然后按回车
runDebugTest()
```
**预计时间**: 30-60秒  
**输出内容**: 完整的调试报告

#### 选项B: 运行基础功能测试
```javascript
// 测试肢体动作系统
testBodyMotionSystem()

// 测试设置按钮
testSettingsButton()
```

#### 选项C: 使用可视化面板
在浏览器中打开：
```
file:///d:/RuanJian/TRAE/Project/my-neuro-main/my-neuro-main/live-2d/test-panel.html
```

---

## 📊 调试输出说明

### 日志格式
所有调试日志都带有 `[DEBUG]` 标记，便于识别：

```
🔧 [DEBUG] BodyMotionController 构造函数开始
   模型类型: live2d
   模型对象: 已提供
🔧 [DEBUG] BodyMotionController 构造函数完成
```

### 图标含义
| 图标 | 含义 |
|------|------|
| 🔧 | 调试断点/构造函数 |
| 🎬 | 动作播放 |
| ✋ | 手势控制 |
| ⚙️ | 设置按钮 |
| 🎯 | 目标/调用 |
| ✅ | 成功 |
| ❌ | 错误/失败 |
| ⚠️ | 警告 |
| ⏳ | 进行中 |
| ▶️ | 开始执行 |
| 📡 | IPC通信 |

---

## 🔍 关键监控点

### 1. 控制器初始化
**监控位置**: body-motion-controller.js 第7-25行  
**关键日志**:
```
🔧 [DEBUG] BodyMotionController 构造函数开始
🔧 [DEBUG] BodyMotionController 构造函数完成
```
**预期结果**: 无错误，模型类型正确识别

### 2. 动作播放
**监控位置**: body-motion-controller.js 第158-180行  
**关键日志**:
```
🎬 [DEBUG] playMotion() 被调用 (第N次)
▶️ [DEBUG] 开始播放动作: wave
```
**预期结果**: 动作名称正确，无队列阻塞

### 3. 手势设置
**监控位置**: body-motion-controller.js 第517-560行  
**关键日志**:
```
✋ [DEBUG] setHandGesture() 被调用 (第N次)
✅ [DEBUG] 手势数据找到
🎯 [DEBUG] 调用Live2D手势设置
```
**预期结果**: 手势参数有效，执行成功

### 4. 设置按钮
**监控位置**: ui-controller.js 第38-150行  
**关键日志**:
```
⚙️ [DEBUG] setupOpenWebUIButton() 被调用
✅ [DEBUG] 设置按钮找到:
🎯 [DEBUG] 设置按钮点击事件触发！
📡 [DEBUG] 开始执行IPC调用: open-web-ui
```
**预期结果**: 按钮找到，点击成功，IPC返回成功

---

## 🛠️ 常见问题排查

### 问题1: bodyMotionController 未定义
**症状**: `ReferenceError: bodyMotionController is not defined`  
**原因**: 应用未完全加载或控制器初始化失败  
**解决**: 
1. 等待5-10秒让应用完全加载
2. 检查控制台是否有JavaScript错误
3. 刷新页面重试

### 问题2: 设置按钮无法点击
**症状**: 点击按钮无反应  
**原因**: 
- z-index层级问题
- 事件绑定失败
- 元素被遮挡

**解决**:
1. 查看控制台是否有 `❌ [DEBUG]` 错误
2. 检查按钮的 `pointer-events` 是否为 `auto`
3. 验证 `webuiIpcBound` 标记是否为 `1`

### 问题3: 动作播放失败
**症状**: `Error: Cannot read property 'x' of undefined`  
**原因**: VRM/Live2D模型骨骼或参数未正确初始化  
**解决**:
1. 确认模型文件路径正确
2. 检查 `_initModelSpecifics()` 是否报错
3. 查看 `vrmBones` 或 `live2dParams` 是否为空

### 问题4: 性能问题
**症状**: 页面卡顿、内存占用高  
**原因**: 
- 动画循环未停止
- 内存泄漏
- DOM节点过多

**解决**:
1. 检查是否有无限循环的动画
2. 监控内存使用情况
3. 清理不必要的DOM元素

---

## 📈 性能基准

### 正常范围参考值
| 指标 | 正常范围 | 警告阈值 | 危险阈值 |
|------|----------|----------|----------|
| 动作播放耗时 | < 500ms | 500-1000ms | > 1000ms |
| 手势切换耗时 | < 300ms | 300-500ms | > 500ms |
| 姿态切换耗时 | < 800ms | 800-1200ms | > 1200ms |
| 内存占用 | < 200MB | 200-400MB | > 400MB |
| DOM节点数 | < 1000 | 1000-3000 | > 3000 |
| FPS | > 55 | 45-55 | < 45 |

---

## 📝 调试命令速查表

### 快速检查命令
```javascript
// 检查控制器状态
console.log(global.bodyMotionController)

// 检查可用动作列表
global.bodyMotionController.getAvailableMotions()

// 检查当前动作
global.bodyMotionController.currentMotion

// 检查是否正在过渡
global.bodyMotionController.isTransitioning

// 检查动作队列长度
global.bodyMotionController.motionQueue.length

// 检查设置按钮
document.getElementById('btn-open-webui')

// 检查按钮样式
window.getComputedStyle(document.getElementById('btn-open-webui').parentElement)
```

### 测试命令
```javascript
// 测试单个动作
await global.bodyMotionController.playMotion('wave', { duration: 1000 })

// 测试单个手势
global.bodyMotionController.setHandGesture('left', 'peace', 500)

// 测试单个姿态
global.bodyMotionController.setPosture('sitting', 1000)

// 重置姿态
global.bodyMotionController.resetPose(800)

// 点击设置按钮
document.getElementById('btn-open-webui').click()
```

### 调试信息收集
```javascript
// 收集性能数据
performance.getEntriesByType('measure')

// 收集内存数据
performance.memory

// 统计DOM节点
document.querySelectorAll('*').length

// 导出调试报告（如果使用debugMonitor）
debugMonitor.exportReport('my-debug-report.json')
```

---

## 📂 生成的文件

调试完成后会自动生成以下文件：

| 文件名 | 内容 | 用途 |
|--------|------|------|
| debug-report.json | 完整的JSON格式报告 | 自动分析、存档 |
| DEBUG_REPORT_TEMPLATE.md | Markdown格式报告模板 | 人工阅读、文档化 |
| console-output.txt | 控制台输出副本 | 详细日志分析 |

---

## 💡 最佳实践

### 1. 定期清理
```javascript
// 清理调试数据
if (debugMonitor) {
    debugMonitor.clear()
}
```

### 2. 分阶段测试
不要一次性测试所有功能，建议分阶段进行：
1. 先测试系统初始化
2. 再测试基本功能
3. 最后测试复杂交互

### 3. 记录基线
首次运行时记录正常状态的指标作为基线：
- 内存占用基线
- 执行时间基线
- FPS基线

### 4. 版本对比
每次修改代码后重新运行调试，对比前后差异。

---

## 🆘 需要帮助？

如果遇到问题：

1. **查看控制台错误** - 大部分问题都有详细的错误消息
2. **检查此文档** - 可能已有解决方案
3. **导出调试报告** - 运行 `debugMonitor.exportReport()` 并分享
4. **提供复现步骤** - 描述如何触发问题

---

## 🎯 下一步

完成调试后：

1. ✅ 查看生成的调试报告
2. ✅ 分析发现的问题
3. ✅ 制定修复计划
4. ✅ 实施改进措施
5. ✅ 重新验证

祝调试顺利！🚀
