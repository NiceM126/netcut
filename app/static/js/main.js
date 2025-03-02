document.addEventListener('DOMContentLoaded', function() {
    // 主题切换
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // 表单提交
    const pasteForm = document.getElementById('pasteForm');
    if (pasteForm) {
        pasteForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                content: document.getElementById('content').value,
                expiration: parseInt(document.getElementById('expiration').value),
                syntax: document.getElementById('syntax').value,
                password: document.getElementById('password').value,
                burn_after_read: document.getElementById('burnAfterRead').checked
            };

            try {
                const response = await fetch('/netcut/api/paste', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();
                
                if (response.ok) {
                    // 跳转到查看页面
                    window.location.href = `/netcut/${data.id}`;
                } else {
                    showToast(data.error || '创建失败，请重试', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showToast('发生错误，请重试', 'error');
            }
        });
    }

    // 复制按钮
    const copyButton = document.querySelector('.btn-copy');
    if (copyButton) {
        copyButton.addEventListener('click', function() {
            const content = document.querySelector('.paste-content pre').textContent;
            navigator.clipboard.writeText(content).then(function() {
                copyButton.textContent = '已复制！';
                setTimeout(() => {
                    copyButton.textContent = '复制内容';
                }, 2000);
            });
        });
    }

    // 显示提示信息
    function showToast(message, type = 'success') {
        const toast = document.getElementById('toast');
        if (toast) {
            toast.textContent = message;
            toast.className = `toast ${type}`;
            toast.style.display = 'block';
            setTimeout(() => {
                toast.style.display = 'none';
            }, 3000);
        }
    }
});