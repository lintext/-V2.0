// test-body-motion.js - 肢体动作系统测试脚本（浏览器环境）
// 此脚本应在浏览器控制台中运行

console.log('=== 肢体动作系统测试脚本 ===');
console.log('请在浏览器控制台中运行此脚本');
console.log('');

// 测试函数
async function testBodyMotionSystem() {
    try {
        console.log('🚀 开始测试肢体动作系统...\n');
        
        // 测试1: 检查全局实例
        console.log('📋 测试1: 检查全局实例');
        if (typeof global !== 'undefined' && global.bodyMotionController) {
            console.log('✅ bodyMotionController 已初始化');
            console.log(`   模型类型: ${global.bodyMotionController.modelType}`);
        } else if (typeof window !== 'undefined' && window.bodyMotionController) {
            console.log('✅ bodyMotionController 已初始化（window）');
            console.log(`   模型类型: ${window.bodyMotionController.modelType}`);
        } else {
            console.error('❌ bodyMotionController 未初始化');
            console.log('💡 提示: 请确保应用已完全启动');
            return;
        }
        
        const controller = global.bodyMotionController || window.bodyMotionController;
        
        // 测试2: 获取可用动作列表
        console.log('\n📋 测试2: 获取可用动作列表');
        const availableMotions = controller.getAvailableMotions();
        console.log(`✅ 可用动作 (${availableMotions.length}个): ${availableMotions.join(', ')}`);
        
        const availableGestures = controller.getAvailableGestures();
        console.log(`✅ 可用手势 (${availableGestures.length}个): ${availableGestures.join(', ')}`);
        
        const availablePostures = controller.getAvailablePostures();
        console.log(`✅ 可用姿态 (${availablePostures.length}个): ${availablePostures.join(', ')}`);
        
        // 测试3: 测试基础动作
        console.log('\n📋 测试3: 测试基础动作');
        
        console.log('🎭 测试招手动作...');
        await controller.playMotion('wave', { duration: 1500 });
        await sleep(2000);
        
        console.log('😊 测试开心动作...');
        await controller.playMotion('happy', { duration: 1500 });
        await sleep(2000);
        
        console.log('🤔 测试思考动作...');
        await controller.playMotion('thinking', { duration: 2000 });
        await sleep(2500);
        
        // 测试4: 测试手部精细动作
        console.log('\n📋 测试4: 测试手部精细动作');
        
        console.log('✌️ 测试左手和平手势...');
        controller.setHandGesture('left', 'peace', 500);
        await sleep(1000);
        
        console.log('👍 测试右手点赞手势...');
        controller.setHandGesture('right', 'thumbsUp', 500);
        await sleep(1000);
        
        // 测试5: 测试姿态切换
        console.log('\n📋 测试5: 测试姿态切换');
        
        console.log('🪑 切换到坐姿...');
        controller.setPosture('sitting', 1000);
        await sleep(1500);
        
        console.log('🧍 恢复站立姿态...');
        controller.setPosture('standing', 1000);
        await sleep(1500);
        
        // 测试6: 测试重置姿态
        console.log('\n📋 测试6: 测试重置姿态');
        controller.resetPose(800);
        await sleep(1000);
        
        console.log('\n✅ === 所有测试完成 ===');
        console.log('🎉 肢体动作系统测试通过！');
        
    } catch (error) {
        console.error('❌ 测试失败:', error);
        console.error(error.stack);
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 测试设置按钮功能
function testSettingsButton() {
    console.log('\n📋 测试设置按钮功能');
    
    const btn = document.getElementById('btn-open-webui');
    if (btn) {
        console.log('✅ 设置按钮找到');
        console.log(`   按钮文本: ${btn.textContent}`);
        console.log(`   按钮标题: ${btn.title}`);
        
        const parentStyle = window.getComputedStyle(btn.parentElement);
        console.log(`   容器z-index: ${parentStyle.zIndex}`);
        console.log(`   容器position: ${parentStyle.position}`);
        
        // 模拟点击
        console.log('🖱️ 模拟点击设置按钮...');
        btn.click();
        
        console.log('✅ 设置按钮测试完成');
    } else {
        console.error('❌ 设置按钮未找到');
    }
}

// 运行所有测试
async function runAllTests() {
    await testBodyMotionSystem();
    testSettingsButton();
}

console.log('💡 使用方法:');
console.log('   1. 等待应用完全启动');
console.log('   2. 在控制台输入: runAllTests()');
console.log('   3. 或分别运行: testBodyMotionSystem() 和 testSettingsButton()');
console.log('');
