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
                const response = await fetch('/api/paste', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();
                
                if (response.ok) {
                    // 跳转到查看页面
                    window.location.href = `/paste/${data.id}`;
                } else {
                    alert(data.error || '创建失败，请重试');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('发生错误，请重试');
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
});