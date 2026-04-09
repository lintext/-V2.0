// debug-test-script.js - 完整的调试测试脚本
// 用于系统性测试肢体动作系统和设置按钮功能

console.log('🚀 开始调试测试...\n');

// 初始化调试监控
let debugMonitor;
try {
    // 尝试加载调试监控器（如果在浏览器环境中）
    if (typeof window !== 'undefined') {
        debugMonitor = new DebugMonitor();
        console.log('✅ 调试监控器已初始化');
    }
} catch (error) {
    console.log('⚠️ 调试监控器未加载，使用基础日志');
}

// 调试配置
const DEBUG_CONFIG = {
    testMotions: ['wave', 'happy', 'thinking', 'dance', 'singing'],
    testGestures: ['peace', 'thumbsUp', 'fist', 'ok'],
    testPostures: ['standing', 'sitting', 'walking', 'leaning'],
    motionDuration: 1500,
    gestureDuration: 500,
    postureDuration: 1000,
    waitBetweenTests: 1000
};

// 测试结果收集
const testResults = {
    systemInit: { status: 'pending', errors: [], warnings: [] },
    controllerInit: { status: 'pending', errors: [], warnings: [] },
    motionPlayback: { status: 'pending', results: [], errors: [] },
    gestureControl: { status: 'pending', results: [], errors: [] },
    postureSwitching: { status: 'pending', results: [], errors: [] },
    settingsButton: { status: 'pending', errors: [], warnings: [] },
    performance: { metrics: [] }
};

async function runDebugTest() {
    console.log('═══════════════════════════════════════');
    console.log('🔍 开始完整调试流程');
    console.log(`⏰ 开始时间: ${new Date().toLocaleString()}`);
    console.log('═══════════════════════════════════════\n');
    
    try {
        // 阶段1: 系统初始化检查
        await phase1_SystemInitialization();
        
        // 阶段2: 控制器初始化检查
        await phase2_ControllerInitialization();
        
        // 阶段3: 动作播放测试
        await phase3_MotionPlaybackTest();
        
        // 阶段4: 手势控制测试
        await phase4_GestureControlTest();
        
        // 阶段5: 姿态切换测试
        await phase5_PostureSwitchingTest();
        
        // 阶段6: 设置按钮功能测试
        await phase6_SettingsButtonTest();
        
        // 阶段7: 性能监控
        await phase7_PerformanceMonitoring();
        
        // 生成最终报告
        await generateFinalReport();
        
    } catch (error) {
        console.error('❌ 调试过程中发生严重错误:', error);
        console.error(error.stack);
        
        testResults.systemInit.status = 'failed';
        testResults.systemInit.errors.push({
            error: error.message,
            stack: error.stack,
            timestamp: Date.now()
        });
    }
}

// 阶段1: 系统初始化检查
async function phase1_SystemInitialization() {
    console.log('\n📋 阶段1: 系统初始化检查');
    console.log('─'.repeat(50));
    
    const startTime = performance.now();
    
    try {
        // 检查全局对象
        console.log('检查全局对象...');
        
        const checks = [
            { name: 'window对象', check: typeof window !== 'undefined' },
            { name: 'document对象', check: typeof document !== 'undefined' },
            { name: 'console对象', check: typeof console !== 'undefined' },
            { name: 'global对象', check: typeof global !== 'undefined' }
        ];
        
        for (const item of checks) {
            if (item.check) {
                console.log(`  ✅ ${item.name} - 正常`);
            } else {
                console.error(`  ❌ ${item.name} - 缺失`);
                testResults.systemInit.warnings.push(`${item.name}缺失`);
            }
        }
        
        // 检查DOM元素
        console.log('\n检查关键DOM元素...');
        const domElements = [
            { id: 'canvas', desc: '画布元素' },
            { id: 'btn-open-webui', desc: '设置按钮' },
            { id: 'model-controls', desc: '模型控制容器' }
        ];
        
        for (const element of domElements) {
            const el = document.getElementById(element.id);
            if (el) {
                console.log(`  ✅ ${element.desc} (#${element.id}) - 存在`);
                
                // 记录元素的详细信息
                if (element.id === 'btn-open-webui') {
                    const style = window.getComputedStyle(el.parentElement);
                    console.log(`     z-index: ${style.zIndex}`);
                    console.log(`     position: ${style.position}`);
                    console.log(`     pointer-events: ${style.pointerEvents}`);
                }
            } else {
                console.error(`  ❌ ${element.desc} (#${element.id}) - 未找到`);
                testResults.systemInit.warnings.push(`DOM元素 #${element.id} 未找到`);
            }
        }
        
        const endTime = performance.now();
        testResults.systemInit.duration = endTime - startTime;
        testResults.systemInit.status = 'passed';
        
        console.log(`\n✅ 系统初始化检查完成 (${(endTime - startTime).toFixed(2)}ms)`);
        
    } catch (error) {
        console.error(`❌ 系统初始化检查失败: ${error.message}`);
        testResults.systemInit.status = 'failed';
        testResults.systemInit.errors.push({
            error: error.message,
            stack: error.stack,
            timestamp: Date.now()
        });
    }
    
    await sleep(DEBUG_CONFIG.waitBetweenTests / 2);
}

// 阶段2: 控制器初始化检查
async function phase2_ControllerInitialization() {
    console.log('\n📋 阶段2: 控制器初始化检查');
    console.log('─'.repeat(50));
    
    const startTime = performance.now();
    
    try {
        // 检查bodyMotionController
        console.log('检查bodyMotionController...');
        
        let controller = null;
        if (typeof global !== 'undefined' && global.bodyMotionController) {
            controller = global.bodyMotionController;
            console.log('  ✅ bodyMotionController 已在global中找到');
        } else if (typeof window !== 'undefined' && window.bodyMotionController) {
            controller = window.bodyMotionController;
            console.log('  ✅ bodyMotionController 已在window中找到');
        } else {
            throw new Error('bodyMotionController 未初始化');
        }
        
        // 检查控制器属性
        console.log('\n检查控制器属性...');
        const properties = [
            { prop: 'modelType', type: 'string' },
            { prop: 'model', type: 'object' },
            { prop: 'currentMotion', type: 'any' },
            { prop: 'motionQueue', type: 'array' },
            { prop: 'isTransitioning', type: 'boolean' }
        ];
        
        for (const property of properties) {
            if (controller[property.prop] !== undefined) {
                const value = controller[property.prop];
                const actualType = Array.isArray(value) ? 'array' : typeof value;
                console.log(`  ✅ ${property.prop}: ${actualType}`);
            } else {
                console.warn(`  ⚠️ ${property.prop}: 未定义`);
                testResults.controllerInit.warnings.push(`属性 ${property.prop} 未定义`);
            }
        }
        
        // 检查方法
        console.log('\n检查控制器方法...');
        const methods = [
            'playMotion',
            'setHandGesture',
            'setPosture',
            'resetPose',
            'getAvailableMotions',
            'getAvailableGestures',
            'getAvailablePostures'
        ];
        
        for (const method of methods) {
            if (typeof controller[method] === 'function') {
                console.log(`  ✅ ${method}() - 方法存在`);
            } else {
                console.error(`  ❌ ${method}() - 方法缺失`);
                testResults.controllerInit.warnings.push(`方法 ${method} 缺失`);
            }
        }
        
        // 获取可用动作列表
        console.log('\n获取可用动作列表...');
        try {
            const motions = controller.getAvailableMotions();
            console.log(`  ✅ 可用动作: ${motions.length}个`);
            console.log(`     ${motions.join(', ')}`);
            
            const gestures = controller.getAvailableGestures();
            console.log(`  ✅ 可用手势: ${gestures.length}个`);
            console.log(`     ${gestures.join(', ')}`);
            
            const postures = controller.getAvailablePostures();
            console.log(`  ✅ 可用姿态: ${postures.length}个`);
            console.log(`     ${postures.join(', ')}`);
            
        } catch (error) {
            console.error(`  ❌ 获取可用动作列表失败: ${error.message}`);
            testResults.controllerInit.errors.push({
                error: error.message,
                context: '获取可用动作列表',
                timestamp: Date.now()
            });
        }
        
        const endTime = performance.now();
        testResults.controllerInit.duration = endTime - startTime;
        testResults.controllerInit.status = 'passed';
        testResults.controllerInit.modelType = controller.modelType;
        
        console.log(`\n✅ 控制器初始化检查完成 (${(endTime - startTime).toFixed(2)}ms)`);
        
    } catch (error) {
        console.error(`❌ 控制器初始化检查失败: ${error.message}`);
        testResults.controllerInit.status = 'failed';
        testResults.controllerInit.errors.push({
            error: error.message,
            stack: error.stack,
            timestamp: Date.now()
        });
    }
    
    await sleep(DEBUG_CONFIG.waitBetweenTests / 2);
}

// 阶段3: 动作播放测试
async function phase3_MotionPlaybackTest() {
    console.log('\n📋 阶段3: 动作播放测试');
    console.log('─'.repeat(50));
    
    const startTime = performance.now();
    const controller = getController();
    
    if (!controller) {
        console.error('❌ 无法进行动作测试：控制器未初始化');
        testResults.motionPlayback.status = 'skipped';
        return;
    }
    
    try {
        for (const motion of DEBUG_CONFIG.testMotions) {
            console.log(`\n测试动作: ${motion}`);
            const motionStart = performance.now();
            
            try {
                // 设置断点
                if (debugMonitor) {
                    debugMonitor.setBreakpoint(`motion_${motion}`, () => true);
                }
                
                // 执行动作
                await controller.playMotion(motion, {
                    duration: DEBUG_CONFIG.motionDuration
                });
                
                const motionEnd = performance.now();
                const duration = motionEnd - motionStart;
                
                testResults.motionPlayback.results.push({
                    motion: motion,
                    success: true,
                    duration: duration,
                    timestamp: Date.now()
                });
                
                console.log(`  ✅ ${motion} - 成功 (${duration.toFixed(2)}ms)`);
                
                // 触发断点
                if (debugMonitor) {
                    debugMonitor.checkBreakpoint(`motion_${motion}`, {
                        motion: motion,
                        duration: duration
                    });
                }
                
            } catch (error) {
                console.error(`  ❌ ${motion} - 失败: ${error.message}`);
                testResults.motionPlayback.results.push({
                    motion: motion,
                    success: false,
                    error: error.message,
                    timestamp: Date.now()
                });
                testResults.motionPlayback.errors.push({
                    motion: motion,
                    error: error.message,
                    stack: error.stack,
                    timestamp: Date.now()
                });
            }
            
            await sleep(DEBUG_CONFIG.waitBetweenTests);
        }
        
        const endTime = performance.now();
        testResults.motionPlayback.duration = endTime - startTime;
        testResults.motionPlayback.status = 'completed';
        
        const successCount = testResults.motionPlayback.results.filter(r => r.success).length;
        const totalCount = testResults.motionPlayback.results.length;
        
        console.log(`\n✅ 动作播放测试完成 (${successCount}/${totalCount} 成功, ${(endTime - startTime).toFixed(2)}ms)`);
        
    } catch (error) {
        console.error(`❌ 动作播放测试失败: ${error.message}`);
        testResults.motionPlayback.status = 'failed';
    }
}

// 阶段4: 手势控制测试
async function phase4_GestureControlTest() {
    console.log('\n📋 阶段4: 手势控制测试');
    console.log('─'.repeat(50));
    
    const startTime = performance.now();
    const controller = getController();
    
    if (!controller) {
        console.error('❌ 无法进行手势测试：控制器未初始化');
        testResults.gestureControl.status = 'skipped';
        return;
    }
    
    try {
        const hands = ['left', 'right'];
        
        for (const hand of hands) {
            console.log(`\n测试${hand === 'left' ? '左' : '右'}手手势:`);
            
            for (const gesture of DEBUG_CONFIG.testGestures) {
                console.log(`  测试手势: ${gesture}`);
                const gestureStart = performance.now();
                
                try {
                    controller.setHandGesture(hand, gesture, DEBUG_CONFIG.gestureDuration);
                    
                    const gestureEnd = performance.now();
                    const duration = gestureEnd - gestureStart;
                    
                    testResults.gestureControl.results.push({
                        hand: hand,
                        gesture: gesture,
                        success: true,
                        duration: duration,
                        timestamp: Date.now()
                    });
                    
                    console.log(`    ✅ ${hand}-${gesture} - 成功 (${duration.toFixed(2)}ms)`);
                    
                } catch (error) {
                    console.error(`    ❌ ${hand}-${gesture} - 失败: ${error.message}`);
                    testResults.gestureControl.results.push({
                        hand: hand,
                        gesture: gesture,
                        success: false,
                        error: error.message,
                        timestamp: Date.now()
                    });
                    testResults.gestureControl.errors.push({
                        hand: hand,
                        gesture: gesture,
                        error: error.message,
                        timestamp: Date.now()
                    });
                }
                
                await sleep(DEBUG_CONFIG.waitBetweenTests / 2);
            }
        }
        
        const endTime = performance.now();
        testResults.gestureControl.duration = endTime - startTime;
        testResults.gestureControl.status = 'completed';
        
        const successCount = testResults.gestureControl.results.filter(r => r.success).length;
        const totalCount = testResults.gestureControl.results.length;
        
        console.log(`\n✅ 手势控制测试完成 (${successCount}/${totalCount} 成功, ${(endTime - startTime).toFixed(2)}ms)`);
        
    } catch (error) {
        console.error(`❌ 手势控制测试失败: ${error.message}`);
        testResults.gestureControl.status = 'failed';
    }
}

// 阶段5: 姿态切换测试
async function phase5_PostureSwitchingTest() {
    console.log('\n📋 阶段5: 姿态切换测试');
    console.log('─'.repeat(50));
    
    const startTime = performance.now();
    const controller = getController();
    
    if (!controller) {
        console.error('❌ 无法进行姿态测试：控制器未初始化');
        testResults.postureSwitching.status = 'skipped';
        return;
    }
    
    try {
        for (const posture of DEBUG_CONFIG.testPostures) {
            console.log(`\n测试姿态: ${posture}`);
            const postureStart = performance.now();
            
            try {
                controller.setPosture(posture, DEBUG_CONFIG.postureDuration);
                
                const postureEnd = performance.now();
                const duration = postureEnd - postureStart;
                
                testResults.postureSwitching.results.push({
                    posture: posture,
                    success: true,
                    duration: duration,
                    timestamp: Date.now()
                });
                
                console.log(`  ✅ ${posture} - 成功 (${duration.toFixed(2)}ms)`);
                
            } catch (error) {
                console.error(`  ❌ ${posture} - 失败: ${error.message}`);
                testResults.postureSwitching.results.push({
                    posture: posture,
                    success: false,
                    error: error.message,
                    timestamp: Date.now()
                });
                testResults.postureSwitching.errors.push({
                    posture: posture,
                    error: error.message,
                    timestamp: Date.now()
                });
            }
            
            await sleep(DEBUG_CONFIG.waitBetweenTests);
        }
        
        // 测试重置姿态
        console.log('\n测试重置姿态...');
        const resetStart = performance.now();
        
        try {
            controller.resetPose(800);
            
            const resetEnd = performance.now();
            const duration = resetEnd - resetStart;
            
            testResults.postureSwitching.results.push({
                posture: 'reset',
                success: true,
                duration: duration,
                timestamp: Date.now()
            });
            
            console.log(`  ✅ 重置姿态 - 成功 (${duration.toFixed(2)}ms)`);
            
        } catch (error) {
            console.error(`  ❌ 重置姿态 - 失败: ${error.message}`);
            testResults.postureSwitching.results.push({
                posture: 'reset',
                success: false,
                error: error.message,
                timestamp: Date.now()
            });
        }
        
        const endTime = performance.now();
        testResults.postureSwitching.duration = endTime - startTime;
        testResults.postureSwitching.status = 'completed';
        
        const successCount = testResults.postureSwitching.results.filter(r => r.success).length;
        const totalCount = testResults.postureSwitching.results.length;
        
        console.log(`\n✅ 姿态切换测试完成 (${successCount}/${totalCount} 成功, ${(endTime - startTime).toFixed(2)}ms)`);
        
    } catch (error) {
        console.error(`❌ 姿态切换测试失败: ${error.message}`);
        testResults.postureSwitching.status = 'failed';
    }
}

// 阶段6: 设置按钮功能测试
async function phase6_SettingsButtonTest() {
    console.log('\n📋 阶段6: 设置按钮功能测试');
    console.log('─'.repeat(50));
    
    const startTime = performance.now();
    
    try {
        // 查找设置按钮
        console.log('查找设置按钮...');
        const btn = document.getElementById('btn-open-webui');
        
        if (!btn) {
            throw new Error('设置按钮元素未找到');
        }
        
        console.log('✅ 设置按钮找到\n');
        
        // 检查按钮属性
        console.log('检查按钮属性:');
        console.log(`  标签名: ${btn.tagName}`);
        console.log(`  文本内容: ${btn.textContent}`);
        console.log(`  标题: ${btn.title}`);
        console.log(`  类型: ${btn.type || 'button'}`);
        console.log(`  是否禁用: ${btn.disabled}`);
        
        // 检查父容器样式
        console.log('\n检查容器样式:');
        const parentStyle = window.getComputedStyle(btn.parentElement);
        console.log(`  position: ${parentStyle.position}`);
        console.log(`  z-index: ${parentStyle.zIndex}`);
        console.log(`  display: ${parentStyle.display}`);
        console.log(`  visibility: ${parentStyle.visibility}`);
        console.log(`  pointer-events: ${parentStyle.pointerEvents}`);
        console.log(`  opacity: ${parentStyle.opacity}`);
        
        // 检查按钮是否可见
        const rect = btn.getBoundingClientRect();
        console.log('\n检查按钮可见性:');
        console.log(`  位置: top=${rect.top}, left=${rect.left}`);
        console.log(`  尺寸: width=${rect.width}, height=${rect.height}`);
        console.log(`  是否在视口内: ${isElementInViewport(btn)}`);
        
        // 检查事件监听器
        console.log('\n检查事件监听器:');
        const hasClickHandler = btn.onclick !== null || 
                               btn.dataset.webuiIpcBound === '1';
        console.log(`  点击事件绑定: ${hasClickHandler ? '✅ 是' : '❌ 否'}`);
        console.log(`  IPC绑定标记: ${btn.dataset.webuiIpcBound || '未设置'}`);
        
        // 模拟点击
        console.log('\n模拟点击设置按钮...');
        const clickStart = performance.now();
        
        try {
            btn.click();
            
            const clickEnd = performance.now();
            const clickDuration = clickEnd - clickStart;
            
            testResults.settingsButton.clickSuccess = true;
            testResults.settingsButton.clickDuration = clickDuration;
            
            console.log(`✅ 点击成功 (${clickDuration.toFixed(2)}ms)`);
            
        } catch (clickError) {
            console.error(`❌ 点击失败: ${clickError.message}`);
            testResults.settingsButton.clickSuccess = false;
            testResults.settingsButton.errors.push({
                error: clickError.message,
                context: '点击事件',
                timestamp: Date.now()
            });
        }
        
        const endTime = performance.now();
        testResults.settingsButton.duration = endTime - startTime;
        testResults.settingsButton.status = 'completed';
        
        console.log(`\n✅ 设置按钮测试完成 (${(endTime - startTime).toFixed(2)}ms)`);
        
    } catch (error) {
        console.error(`❌ 设置按钮测试失败: ${error.message}`);
        testResults.settingsButton.status = 'failed';
        testResults.settingsButton.errors.push({
            error: error.message,
            stack: error.stack,
            timestamp: Date.now()
        });
    }
    
    await sleep(DEBUG_CONFIG.waitBetweenTests);
}

// 阶段7: 性能监控
async function phase7_PerformanceMonitoring() {
    console.log('\n📋 阶段7: 性能监控');
    console.log('─'.repeat(50));
    
    try {
        // 内存使用情况
        console.log('内存使用情况:');
        if (performance.memory) {
            const memory = {
                usedJSHeapSize: (performance.memory.usedJSHeapSize / 1024 / 1024).toFixed(2),
                totalJSHeapSize: (performance.memory.totalJSHeapSize / 1024 / 1024).toFixed(2),
                jsHeapSizeLimit: (performance.memory.jsHeapSizeLimit / 1024 / 1024).toFixed(2)
            };
            
            console.log(`  已使用堆大小: ${memory.usedJSHeapSize} MB`);
            console.log(`  总堆大小: ${memory.totalJSHeapSize} MB`);
            console.log(`  堆大小限制: ${memory.jsHeapSizeLimit} MB`);
            
            testResults.performance.metrics.push({
                metric: 'memory_usage',
                value: memory,
                timestamp: Date.now()
            });
        } else {
            console.log('  ⚠️ 内存API不可用（非Chrome浏览器）');
        }
        
        // 性能条目
        console.log('\n性能条目:');
        const entries = performance.getEntriesByType('measure');
        console.log(`  性能测量数量: ${entries.length}`);
        
        entries.slice(-5).forEach(entry => {
            console.log(`  - ${entry.name}: ${entry.duration.toFixed(2)}ms`);
        });
        
        // DOM节点统计
        console.log('\nDOM统计:');
        const totalNodes = document.querySelectorAll('*').length;
        console.log(`  总节点数: ${totalNodes}`);
        
        testResults.performance.metrics.push({
            metric: 'dom_nodes',
            value: totalNodes,
            timestamp: Date.now()
        });
        
        console.log('\n✅ 性能监控完成');
        
    } catch (error) {
        console.error(`❌ 性能监控失败: ${error.message}`);
        testResults.performance.errors = [error.message];
    }
}

// 生成最终报告
async function generateFinalReport() {
    console.log('\n' + '═'.repeat(60));
    console.log('📊 最终调试报告');
    console.log('═'.repeat(60));
    
    const reportTime = new Date().toLocaleString();
    const totalTime = Date.now() - (testResults.startTime || Date.now());
    
    // 统计信息
    console.log(`\n⏰ 报告时间: ${reportTime}`);
    console.log(`⏱️ 总耗时: ${(totalTime / 1000).toFixed(2)}秒`);
    
    // 各阶段结果
    console.log('\n📋 各阶段测试结果:');
    
    const phases = [
        { name: '系统初始化', result: testResults.systemInit },
        { name: '控制器初始化', result: testResults.controllerInit },
        { name: '动作播放', result: testResults.motionPlayback },
        { name: '手势控制', result: testResults.gestureControl },
        { name: '姿态切换', result: testResults.postureSwitching },
        { name: '设置按钮', result: testResults.settingsButton }
    ];
    
    phases.forEach(phase => {
        const status = phase.result.status;
        const icon = status === 'passed' || status === 'completed' ? '✅' :
                     status === 'failed' ? '❌' : 
                     status === 'skipped' ? '⏭️' : '⏳';
        
        console.log(`  ${icon} ${phase.name}: ${status.toUpperCase()}`);
        
        if (phase.result.errors?.length > 0) {
            console.log(`     错误数: ${phase.result.errors.length}`);
        }
        if (phase.result.warnings?.length > 0) {
            console.log(`     警告数: ${phase.result.warnings.length}`);
        }
        if (phase.result.results) {
            const success = phase.result.results.filter(r => r.success).length;
            const total = phase.result.results.length;
            console.log(`     通过率: ${success}/${total}`);
        }
    });
    
    // 错误汇总
    const allErrors = [
        ...(testResults.systemInit.errors || []),
        ...(testResults.controllerInit.errors || []),
        ...(testResults.motionPlayback.errors || []),
        ...(testResults.gestureControl.errors || []),
        ...(testResults.postureSwitching.errors || []),
        ...(testResults.settingsButton.errors || [])
    ];
    
    if (allErrors.length > 0) {
        console.log(`\n❌ 发现 ${allErrors.length} 个错误:`);
        allErrors.forEach((err, index) => {
            console.log(`  ${index + 1}. ${err.error || err.message}`);
            if (err.context) console.log(`     上下文: ${err.context}`);
            if (err.motion) console.log(`     动作: ${err.motion}`);
            if (err.gesture) console.log(`     手势: ${err.gesture}`);
            if (err.posture) console.log(`     姿态: ${err.posture}`);
        });
    } else {
        console.log('\n✅ 未发现任何错误！');
    }
    
    // 建议和结论
    console.log('\n💡 建议:');
    
    if (allErrors.length > 0) {
        console.log('  • 查看上述错误详情，定位问题根源');
        console.log('  • 检查模型文件是否正确加载');
        console.log('  • 验证浏览器控制台是否有其他错误');
    }
    
    if (testResults.settingsButton.status === 'failed') {
        console.log('  • 设置按钮问题可能原因:');
        console.log('    - IPC通信异常');
        console.log('    - WebUI服务未启动');
        console.log('    - 权限或路径问题');
    }
    
    if (testResults.controllerInit.status === 'failed') {
        console.log('  • 控制器初始化失败可能原因:');
        console.log('    - 模型加载失败');
        console.log('    - 依赖模块缺失');
        console.log('    - JavaScript执行错误');
    }
    
    console.log('\n' + '═'.repeat(60));
    console.log('🎉 调试流程结束');
    console.log('═'.repeat(60));
    
    // 导出报告
    if (debugMonitor) {
        console.log('\n正在导出详细调试报告...');
        await debugMonitor.exportReport('debug-report.json');
    }
    
    // 返回完整结果
    return testResults;
}

// 辅助函数
function getController() {
    if (typeof global !== 'undefined' && global.bodyMotionController) {
        return global.bodyMotionController;
    } else if (typeof window !== 'undefined' && window.bodyMotionController) {
        return window.bodyMotionController;
    }
    return null;
}

function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 启动调试测试
runDebugTest().catch(console.error);

console.log('\n💡 提示: 调试测试已在后台运行，请查看上方输出');
