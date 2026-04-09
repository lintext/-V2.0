# 肢体动作系统使用文档

## 概述

本次更新为Live2D和VRM模型实现了完整的肢体动作系统，包括手部精细动作和全身协调运动。同时修复了右下角设置按钮无法打开WebUI界面的问题。

## 功能特性

### 1. 肢体动作系统

#### 支持的动作类型

**情绪动作：**
- `happy` - 开心：双臂张开，身体微微晃动
- `angry` - 生气：双臂抱胸，身体紧绷
- `sad` - 难过：头部低垂，身体放松
- `surprised` - 惊讶：双臂举起，身体后仰
- `shy` - 害羞：头部偏转，双臂交叉

**交互动作：**
- `wave` - 招手：右手挥动
- `thinking` - 思考：手托下巴，头部倾斜

**表演动作：**
- `dance` - 跳舞：全身律动，手臂摆动
- `singing` - 唱歌：身体摇摆，手臂挥舞

#### 手部精细动作

支持7种手势：
- `open` - 张开手掌
- `fist` - 握拳
- `point` - 指向
- `peace` - 比耶（剪刀手）
- `thumbsUp` - 点赞
- `rock` - 摇滚手势
- `ok` - OK手势

#### 姿态系统

支持4种基础姿态：
- `standing` - 站立：自然直立姿态
- `sitting` - 坐姿：放松坐姿
- `walking` - 行走：行走姿态
- `leaning` - 倚靠：倚靠姿态

### 2. 设置按钮修复

**修复内容：**
- 增强了事件绑定逻辑，添加详细调试日志
- 提高了按钮z-index至100002，确保在最上层
- 添加了完整的错误处理和用户反馈
- 增加了鼠标悬停事件监听

## API使用指南

### 基础用法

```javascript
// 播放动作
await global.bodyMotionController.playMotion('wave', {
    duration: 1500,  // 持续时间（毫秒）
    easing: 'easeInOutQuad',  // 缓动函数
    loop: false  // 是否循环
});

// 设置手势
global.bodyMotionController.setHandGesture('left', 'peace', 500);  // 左手比耶
global.bodyMotionController.setHandGesture('right', 'thumbsUp', 500);  // 右手点赞

// 切换姿态
global.bodyMotionController.setPosture('sitting', 1000);  // 切换到坐姿

// 重置姿态
global.bodyMotionController.resetPose(800);  // 恢复默认姿态
```

### 高级用法

```javascript
// 获取可用动作列表
const motions = global.bodyMotionController.getAvailableMotions();
console.log('可用动作:', motions);

// 获取可用手势
const gestures = global.bodyMotionController.getAvailableGestures();
console.log('可用手势:', gestures);

// 获取可用姿态
const postures = global.bodyMotionController.getAvailablePostures();
console.log('可用姿态:', postures);

// 检查模型类型
const modelType = global.bodyMotionController.modelType;  // 'live2d' 或 'vrm'
```

### 缓动函数

支持多种缓动函数：
- `linear` - 线性
- `easeInQuad` - 二次方缓入
- `easeOutQuad` - 二次方缓出
- `easeInOutQuad` - 二次方缓入缓出（默认）
- `easeInCubic` - 三次方缓入
- `easeOutCubic` - 三次方缓出
- `easeInOutCubic` - 三次方缓入缓出

## 测试方法

### 1. 运行测试脚本

```bash
cd d:\RuanJian\TRAE\Project\my-neuro-main\my-neuro-main\live-2d
node test-body-motion.js
```

### 2. 手动测试

在浏览器控制台中执行：

```javascript
// 测试招手动作
await global.bodyMotionController.playMotion('wave', { duration: 1500 });

// 测试手势
global.bodyMotionController.setHandGesture('right', 'peace', 500);

// 测试姿态切换
global.bodyMotionController.setPosture('sitting', 1000);

// 测试设置按钮
document.getElementById('btn-open-webui').click();
```

## 技术实现

### Live2D模型

通过操作Live2D的核心参数实现：
- `ParamAngleX/Y/Z` - 头部旋转
- `ParamBodyAngleX/Y/Z` - 身体旋转
- `ParamArmLeftAngle` - 左臂角度
- `ParamArmRightAngle` - 右臂角度
- `ParamHandLeft/Right` - 手部形态

### VRM模型

通过操作VRM的骨骼节点实现：
- `head` - 头部骨骼
- `spine` - 脊椎骨骼
- `leftUpperArm/rightUpperArm` - 上臂骨骼
- `leftLowerArm/rightLowerArm` - 前臂骨骼
- `leftHand/rightHand` - 手部骨骼
- 手指骨骼（拇指、食指、中指、无名指、小指）

## 文件结构

```
live-2d/
├── js/
│   └── model/
│       ├── body-motion-controller.js  # 肢体动作控制器（新增）
│       ├── model-setup.js             # Live2D模型设置（已修改）
│       └── vrm-model-setup.js         # VRM模型设置（已修改）
├── css/
│   └── styles.css                     # 样式文件（已修改）
├── js/ui/
│   └── ui-controller.js               # UI控制器（已修改）
└── test-body-motion.js                # 测试脚本（新增）
```

## 注意事项

1. **模型兼容性**
   - Live2D模型需要支持相应的参数
   - VRM模型需要完整的骨骼系统
   - 某些模型可能不支持所有动作

2. **性能优化**
   - 动作过渡使用requestAnimationFrame
   - 避免同时播放过多动作
   - 合理设置动作持续时间

3. **调试建议**
   - 检查控制台日志确认初始化状态
   - 使用测试脚本验证功能
   - 查看浏览器开发者工具中的错误信息

## 更新日志

### v1.0.0 (2026-04-01)

**新增功能：**
- ✨ 实现完整的肢体动作系统
- ✨ 支持Live2D和VRM两种模型类型
- ✨ 实现9种情绪和交互动作
- ✨ 实现7种手部精细手势
- ✨ 实现4种基础姿态

**修复问题：**
- 🐛 修复设置按钮无法打开WebUI界面的问题
- 🐛 修复按钮z-index层级问题
- 🐛 增强事件绑定的可靠性

**优化改进：**
- ⚡ 添加详细的调试日志
- ⚡ 优化动作过渡动画
- ⚡ 提高系统响应速度

## 技术支持

如有问题，请检查：
1. 控制台日志输出
2. 模型是否正确加载
3. 参数是否正确设置
4. 浏览器兼容性

## 未来计划

- [ ] 添加更多动作类型
- [ ] 实现动作序列播放
- [ ] 支持自定义动作
- [ ] 添加动作编辑器
- [ ] 优化VRM手指动作
