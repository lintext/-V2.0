// 屏幕共享和截图功能模块

let screenShareStream = null;
let currentScreenshotBlob = null;

function toggleToolbarMenu() {
    const toolbar = document.getElementById('floatingToolbar');
    if (toolbar) {
        toolbar.classList.toggle('menu-open');
    }
}

document.addEventListener('click', function(e) {
    const toolbar = document.getElementById('floatingToolbar');
    if (toolbar && !toolbar.contains(e.target)) {
        toolbar.classList.remove('menu-open');
    }
});

async function startScreenShare() {
    try {
        toggleToolbarMenu();
        
        if (screenShareStream) {
            showToast('屏幕共享已在进行中', 'warning');
            return;
        }

        const stream = await navigator.mediaDevices.getDisplayMedia({
            video: {
                cursor: 'always'
            },
            audio: false
        });

        screenShareStream = stream;

        const preview = document.getElementById('screenSharePreview');
        const video = document.getElementById('screenShareVideo');
        
        if (preview && video) {
            video.srcObject = stream;
            preview.style.display = 'block';
        }

        stream.getVideoTracks()[0].onended = function() {
            stopScreenShare();
        };

        showToast('屏幕共享已开始', 'success');
        
    } catch (error) {
        console.error('屏幕共享失败:', error);
        if (error.name === 'NotAllowedError') {
            showToast('用户取消了屏幕共享', 'warning');
        } else {
            showToast('屏幕共享失败: ' + error.message, 'error');
        }
    }
}

function stopScreenShare() {
    if (screenShareStream) {
        screenShareStream.getTracks().forEach(track => track.stop());
        screenShareStream = null;
    }

    const preview = document.getElementById('screenSharePreview');
    const video = document.getElementById('screenShareVideo');
    
    if (preview) {
        preview.style.display = 'none';
    }
    if (video) {
        video.srcObject = null;
    }

    showToast('屏幕共享已停止', 'info');
}

async function takeScreenshot() {
    try {
        toggleToolbarMenu();
        
        const stream = await navigator.mediaDevices.getDisplayMedia({
            video: {
                displaySurface: 'monitor'
            },
            audio: false
        });

        const video = document.createElement('video');
        video.srcObject = stream;
        await video.play();

        await new Promise(resolve => setTimeout(resolve, 100));

        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        stream.getTracks().forEach(track => track.stop());

        canvas.toBlob(function(blob) {
            currentScreenshotBlob = blob;
            const url = URL.createObjectURL(blob);
            
            const modal = document.getElementById('screenshotModal');
            const img = document.getElementById('screenshotImage');
            
            if (modal && img) {
                img.src = url;
                modal.style.display = 'flex';
            }
        }, 'image/png');

        showToast('截图成功', 'success');
        
    } catch (error) {
        console.error('截图失败:', error);
        if (error.name === 'NotAllowedError') {
            showToast('用户取消了截图', 'warning');
        } else {
            showToast('截图失败: ' + error.message, 'error');
        }
    }
}

async function takeWindowScreenshot() {
    try {
        toggleToolbarMenu();
        
        const stream = await navigator.mediaDevices.getDisplayMedia({
            video: {
                displaySurface: 'window'
            },
            audio: false
        });

        const video = document.createElement('video');
        video.srcObject = stream;
        await video.play();

        await new Promise(resolve => setTimeout(resolve, 100));

        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        stream.getTracks().forEach(track => track.stop());

        canvas.toBlob(function(blob) {
            currentScreenshotBlob = blob;
            const url = URL.createObjectURL(blob);
            
            const modal = document.getElementById('screenshotModal');
            const img = document.getElementById('screenshotImage');
            
            if (modal && img) {
                img.src = url;
                modal.style.display = 'flex';
            }
        }, 'image/png');

        showToast('窗口截图成功', 'success');
        
    } catch (error) {
        console.error('窗口截图失败:', error);
        if (error.name === 'NotAllowedError') {
            showToast('用户取消了截图', 'warning');
        } else {
            showToast('窗口截图失败: ' + error.message, 'error');
        }
    }
}

function takeRegionScreenshot() {
    toggleToolbarMenu();
    
    const selector = document.createElement('div');
    selector.className = 'region-selector';
    selector.innerHTML = `
        <div class="region-selector-overlay"></div>
        <div class="region-selector-box" style="display: none;"></div>
        <div class="region-selector-hint">按住鼠标拖动选择截图区域，按 ESC 取消</div>
    `;
    document.body.appendChild(selector);

    let isSelecting = false;
    let startX = 0;
    let startY = 0;
    const box = selector.querySelector('.region-selector-box');

    function onMouseDown(e) {
        if (e.target.classList.contains('region-selector-overlay')) {
            isSelecting = true;
            startX = e.clientX;
            startY = e.clientY;
            box.style.display = 'block';
            box.style.left = startX + 'px';
            box.style.top = startY + 'px';
            box.style.width = '0px';
            box.style.height = '0px';
        }
    }

    function onMouseMove(e) {
        if (!isSelecting) return;

        const currentX = e.clientX;
        const currentY = e.clientY;

        const left = Math.min(startX, currentX);
        const top = Math.min(startY, currentY);
        const width = Math.abs(currentX - startX);
        const height = Math.abs(currentY - startY);

        box.style.left = left + 'px';
        box.style.top = top + 'px';
        box.style.width = width + 'px';
        box.style.height = height + 'px';
    }

    async function onMouseUp(e) {
        if (!isSelecting) return;
        isSelecting = false;

        const currentX = e.clientX;
        const currentY = e.clientY;

        const left = Math.min(startX, currentX);
        const top = Math.min(startY, currentY);
        const width = Math.abs(currentX - startX);
        const height = Math.abs(currentY - startY);

        selector.remove();

        if (width < 10 || height < 10) {
            showToast('选择的区域太小', 'warning');
            return;
        }

        try {
            const stream = await navigator.mediaDevices.getDisplayMedia({
                video: true,
                audio: false
            });

            const video = document.createElement('video');
            video.srcObject = stream;
            await video.play();

            await new Promise(resolve => setTimeout(resolve, 100));

            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            
            const ctx = canvas.getContext('2d');
            
            const scaleX = video.videoWidth / window.innerWidth;
            const scaleY = video.videoHeight / window.innerHeight;
            
            ctx.drawImage(
                video,
                left * scaleX,
                top * scaleY,
                width * scaleX,
                height * scaleY,
                0,
                0,
                width,
                height
            );

            stream.getTracks().forEach(track => track.stop());

            canvas.toBlob(function(blob) {
                currentScreenshotBlob = blob;
                const url = URL.createObjectURL(blob);
                
                const modal = document.getElementById('screenshotModal');
                const img = document.getElementById('screenshotImage');
                
                if (modal && img) {
                    img.src = url;
                    modal.style.display = 'flex';
                }
            }, 'image/png');

            showToast('区域截图成功', 'success');
            
        } catch (error) {
            console.error('区域截图失败:', error);
            if (error.name === 'NotAllowedError') {
                showToast('用户取消了截图', 'warning');
            } else {
                showToast('区域截图失败: ' + error.message, 'error');
            }
        }
    }

    function onKeyDown(e) {
        if (e.key === 'Escape') {
            selector.remove();
            showToast('已取消区域截图', 'info');
            document.removeEventListener('keydown', onKeyDown);
        }
    }

    selector.addEventListener('mousedown', onMouseDown);
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp, { once: true });
    document.addEventListener('keydown', onKeyDown);
}

function closeScreenshotModal() {
    const modal = document.getElementById('screenshotModal');
    const img = document.getElementById('screenshotImage');
    
    if (modal) {
        modal.style.display = 'none';
    }
    if (img) {
        URL.revokeObjectURL(img.src);
        img.src = '';
    }
    currentScreenshotBlob = null;
}

function downloadScreenshot() {
    if (!currentScreenshotBlob) {
        showToast('没有可保存的截图', 'error');
        return;
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const filename = `screenshot-${timestamp}.png`;

    const url = URL.createObjectURL(currentScreenshotBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showToast('截图已保存: ' + filename, 'success');
}

async function copyScreenshot() {
    if (!currentScreenshotBlob) {
        showToast('没有可复制的截图', 'error');
        return;
    }

    try {
        await navigator.clipboard.write([
            new ClipboardItem({
                'image/png': currentScreenshotBlob
            })
        ]);
        showToast('截图已复制到剪贴板', 'success');
    } catch (error) {
        console.error('复制截图失败:', error);
        showToast('复制截图失败，请尝试保存', 'error');
    }
}

function sendToAI() {
    if (!currentScreenshotBlob) {
        showToast('没有可发送的截图', 'error');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        const base64 = e.target.result;
        
        console.log('截图准备发送给AI，base64长度:', base64.length);
        
        if (typeof window.sendImageToAI === 'function') {
            window.sendImageToAI(base64);
        } else {
            showToast('AI功能暂未连接，请先启动对话服务', 'warning');
        }
    };
    reader.readAsDataURL(currentScreenshotBlob);
    
    closeScreenshotModal();
    showToast('截图已发送给AI', 'success');
}

function openSettings() {
    toggleToolbarMenu();
    
    const basicConfigTab = document.querySelector('[onclick="switchTab(\'basic-config\')"]');
    if (basicConfigTab) {
        basicConfigTab.click();
    }
}

window.toggleToolbarMenu = toggleToolbarMenu;
window.startScreenShare = startScreenShare;
window.stopScreenShare = stopScreenShare;
window.takeScreenshot = takeScreenshot;
window.takeWindowScreenshot = takeWindowScreenshot;
window.takeRegionScreenshot = takeRegionScreenshot;
window.closeScreenshotModal = closeScreenshotModal;
window.downloadScreenshot = downloadScreenshot;
window.copyScreenshot = copyScreenshot;
window.sendToAI = sendToAI;
window.openSettings = openSettings;

console.log('✅ 工具栏功能模块已加载');
