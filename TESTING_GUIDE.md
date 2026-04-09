# 测试肢体动作系统指南

## 🚀 启动应用

### 方法1: 使用npm脚本（推荐）
```bash
cd d:\RuanJian\TRAE\Project\my-neuro-main\my-neuro-main
npm start
```

### 方法2: 直接运行
```bash
cd d:\RuanJian\TRAE\Project\my-neuro-main\my-neuro-main
npx electron .
```

## 🧪 运行测试

### 步骤1: 启动应用
按照上面的方法启动应用程序

### 步骤2: 打开开发者工具
- 按 `F12` 或 `Ctrl+Shift+I`
- 或右键点击应用 → 选择"检查"

### 步骤3: 在控制台中运行测试

#### 运行所有测试
```javascript
runAllTests()
```

#### 分别运行测试
```javascript
// 测试肢体动作系统
testBodyMotionSystem()

// 测试设置按钮
testSettingsButton()
```

## 📋 手动测试命令

### 测试肢体动作
```javascript
// 播放招手动作
await global.bodyMotionController.playMotion('wave', { duration: 1500 })

// 播放开心动作
await global.bodyMotionController.playMotion('happy', { duration: 1500 })

// 播放思考动作
await global.bodyMotionController.playMotion('thinking', { duration: 2000 })

// 播放跳舞动作
await global.bodyMotionController.playMotion('dance', { duration: 2000 })
```

### 测试手势
```javascript
// 左手比耶
global.bodyMotionController.setHandGesture('left', 'peace', 500)

// 右手点赞
global.bodyMotionController.setHandGesture('right', 'thumbsUp', 500)

// 左手握拳
global.bodyMotionController.setHandGesture('left', 'fist', 500)

// 右手OK手势
global.bodyMotionController.setHandGesture('right', 'ok', 500)
```

### 测试姿态
```javascript
// 切换到坐姿
global.bodyMotionController.setPosture('sitting', 1000)

// 恢复站立
global.bodyMotionController.setPosture('standing', 1000)

// 倚靠姿态
global.bodyMotionController.setPosture('leaning', 1000)
```

### 重置姿态
```javascript
// 重置到默认姿态
global.bodyMotionController.resetPose(800)
```

### 测试设置按钮
```javascript
// 点击设置按钮
document.getElementById('btn-open-webui').click()
```

## 🔍 检查系统状态

### 检查控制器是否初始化
```javascript
// 检查全局实例
console.log('bodyMotionController:', global.bodyMotionController)

// 检查模型类型
console.log('模型类型:', global.bodyMotionController?.modelType)

// 获取可用动作
console.log('可用动作:', global.bodyMotionController?.getAvailableMotions())

// 获取可用手势
console.log('可用手势:', global.bodyMotionController?.getAvailableGestures())

// 获取可用姿态
console.log('可用姿态:', global.bodyMotionController?.getAvailablePostures())
```

## ⚠️ 常见问题

### 1. bodyMotionController 未初始化
**原因**: 应用还未完全启动
**解决**: 等待几秒钟，确保模型加载完成

### 2. 设置按钮无法点击
**原因**: 可能被其他元素遮挡
**解决**: 检查控制台是否有错误信息

### 3. 动作不流畅
**原因**: 动作持续时间太短
**解决**: 增加duration参数（建议1000-2000毫秒）

### 4. 手势不显示
**原因**: 模型可能不支持某些参数
**解决**: 检查控制台日志，确认模型类型

## 📊 预期输出

### 成功的测试输出
```
🚀 开始测试肢体动作系统...

📋 测试1: 检查全局实例
✅ bodyMotionController 已初始化
   模型类型: live2d

📋 测试2: 获取可用动作列表
✅ 可用动作 (9个): wave, happy, thinking, dance, singing, shy, angry, sad, surprised
✅ 可用手势 (7个): open, fist, point, peace, thumbsUp, rock, ok
✅ 可用姿态 (4个): standing, walking, sitting, leaning

📋 测试3: 测试基础动作
🎭 测试招手动作...
😊 测试开心动作...
🤔 测试思考动作...

📋 测试4: 测试手部精细动作
✌️ 测试左手和平手势...
👍 测试右手点赞手势...

📋 测试5: 测试姿态切换
🪑 切换到坐姿...
🧍 恢复站立姿态...

📋 测试6: 测试重置姿态
✅ === 所有测试完成 ===
🎉 肢体动作系统测试通过！

📋 测试设置按钮功能
✅ 设置按钮找到
   按钮文本: ⚙
   按钮标题: 打开设置
   容器z-index: 100002
   容器position: fixed
🖱️ 模拟点击设置按钮...
✅ 设置按钮测试完成
```

## 🎯 下一步

1. ✅ 启动应用
2. ✅ 打开开发者工具
3. ✅ 运行测试脚本
4. ✅ 验证所有功能
5. ✅ 享受流畅的肢体动作！

祝测试顺利！🎉
