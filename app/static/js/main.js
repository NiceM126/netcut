document.addEventListener('DOMContentLoaded', function() {

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
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (response.ok) {
                    // 跳转到查看页面
                    window.location.href = `/${data.id}`;
                } else {
                    showToast(data.error || '创建失败，请重试', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showToast('发生错误，请重试', 'error');
            }
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