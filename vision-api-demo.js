/**
 * 多模态API使用示例
 * 演示如何使用豆包视觉模型进行图片理解
 */

const { LLMClient } = require('./js/ai/llm-client.js');
const config = require('./config.json');

async function testVisionAPI() {
    console.log('🚀 初始化多模态LLM客户端...\n');

    const llmClient = new LLMClient({
        llm: {
            api_key: config.llm.api_key,
            api_url: config.llm.api_url,
            model: config.llm.model,
            temperature: config.llm.temperature,
            supports_vision: true
        }
    });

    try {
        // 示例1：使用URL格式的图片
        console.log('📸 示例1：使用URL格式图片\n');
        console.log('-'.repeat(50));

        const result1 = await llmClient.chatWithImage(
            '这张图片主要讲了什么？',
            {
                url: 'https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg',
                format: 'url',  // URL格式
                detail: 'auto'  // 自动选择细节级别
            }
        );

        console.log('\n✅ AI回复（URL图片）:');
        console.log(result1.content);
        console.log('\n' + '='.repeat(50) + '\n');

        // 示例2：使用Base64格式的本地截图
        console.log('📸 示例2：使用Base64格式图片（本地截图）\n');
        console.log('-'.repeat(50));
        console.log('提示：此处需要提供真实的base64图片数据\n');

        // 模拟base64数据（实际使用时替换为真实数据）
        const fakeBase64 = '/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMCAgMDAwMEAwME...';

        const result2 = await llmClient.chatWithImage(
            '请描述这张截图的内容',
            {
                url: fakeBase64,
                format: 'base64',  // Base64格式
                detail: 'high'     // 高细节模式
            },
            [] // 可选的历史消息上下文
        );

        console.log('\n✅ AI回复（Base64图片）:');
        console.log(result2.content);
        console.log('\n' + '='.repeat(50) + '\n');

    } catch (error) {
        console.error('❌ 测试失败:', error.message);
    }
}

// 手动构建多模态消息的示例
function manualMultimodalExample() {
    console.log('\n📝 手动构建多模态消息示例\n');
    console.log('-'.repeat(50));

    const llmClient = new LLMClient({ llm: config.llm });

    // 使用createMultimodalContent方法
    const content = llmClient.createMultimodalContent(
        '请分析这张图片中的文字内容',
        {
            url: 'https://example.com/image.jpg',
            format: 'url'
        }
    );

    console.log('生成的多模态消息结构:');
    console.log(JSON.stringify(content, null, 2));

    /*
    输出结果：
    [
      {
        "type": "image_url",
        "image_url": {
          "url": "https://example.com/image.jpg",
          "detail": "auto"
        }
      },
      {
        "type": "text",
        "text": "请分析这张图片中的文字内容"
      }
    ]
    */
}

// 运行测试
if (require.main === module) {
    console.log('╔══════════════════════════════════════════╗');
    console.log('║   豆包多模态API测试 - Vision Demo       ║');
    console.log('╚══════════════════════════════════════════╝\n');

    testVisionAPI().then(() => {
        manualMultimodalExample();
        console.log('\n✅ 所有测试完成！');
    }).catch(err => {
        console.error('❌ 测试出错:', err);
    });
}

module.exports = { testVisionAPI, manualMultimodalExample };
