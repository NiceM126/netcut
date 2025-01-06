from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from ..utils.encryption import encrypt_content, decrypt_content
from ..utils.password import hash_password, verify_password
from flask import current_app
import json

class PasteService:
    @property
    def db(self):
        """延迟获取数据库实例"""
        return current_app.db

    def create_paste(self, paste_name, content, expiration=604800, password=None, burn_after_read=False):
        """创建或更新剪贴板"""
        # 验证输入
        if not content:
            raise ValueError('内容不能为空')
            
        if not paste_name:
            raise ValueError('剪贴板名称不能为空')
            
        # 计算过期时间
        expires_at = datetime.now() + timedelta(seconds=expiration)
        
        try:
            # 加密内容
            encrypted_content = encrypt_content(content)
            if encrypted_content is None:
                raise ValueError('内容加密失败')
            
            # 如果有密码，记录状态并存储哈希密码
            has_password = bool(password)
            password_hash = hash_password(password) if password else None
            
            # 准备数据
            paste_data = {
                'name': paste_name,
                'content': None,  # 明文内容始终为空
                'encrypted_content': encrypted_content,
                'has_password': has_password,
                'password_hash': password_hash,  # 存储密码哈希
                'burn_after_read': burn_after_read,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'expires_at': expires_at.strftime('%Y-%m-%d %H:%M:%S'),
                'views': 0
            }
            
            # 保存到数据库
            self.db.set(f'paste:{paste_name}', json.dumps(paste_data))
            if expiration:
                self.db.expire(f'paste:{paste_name}', expiration)
                
            return {'status': 'success'}
            
        except Exception as e:
            raise ValueError(f'创建剪贴板失败: {str(e)}')
        
    def verify_paste_password(self, paste_name: str, password: str) -> bool:
        """验证剪贴板密码"""
        try:
            paste_data = self.db.get(f'paste:{paste_name}')
            if not paste_data:
                return False
            
            paste = json.loads(paste_data)
            if not paste.get('has_password'):
                return True
                
            stored_password_hash = paste.get('password_hash')
            return bool(stored_password_hash and verify_password(password, stored_password_hash))
            
        except Exception:
            return False
            
    def get_paste(self, paste_name, password=None):
        """获取剪贴板内容"""
        try:
            # 从数据库获取数据
            paste_data = self.db.get(f'paste:{paste_name}')
            if not paste_data:
                return None
            
            paste = json.loads(paste_data)
            
            # 处理阅后即焚
            if paste.get('burn_after_read'):
                self.db.delete(f'paste:{paste_name}')
            
            # 更新访问次数
            paste['views'] += 1
            self.db.set(f'paste:{paste_name}', json.dumps(paste))
            
            # 解密内容
            encrypted_content = paste.get('encrypted_content')
            if encrypted_content:
                try:
                    # 如果有密码保护，先验证密码
                    if paste.get('has_password'):
                        if not password:
                            # 如果需要密码但没有提供，返回提示
                            return {
                                'name': paste_name,
                                'has_password': True,
                                'created_at': paste.get('created_at'),
                                'expires_at': paste.get('expires_at'),
                                'views': paste.get('views', 0)
                            }
                        
                        # 验证密码
                        if not self.verify_paste_password(paste_name, password):
                            raise ValueError('密码错误')
                    
                    # 解密内容
                    content = decrypt_content(encrypted_content)
                    if content is None:
                        raise ValueError('内容解密失败')
                    
                    paste['content'] = content
                    
                except Exception as e:
                    raise ValueError(f'解密失败: {str(e)}')
            
            return paste
            
        except Exception as e:
            raise ValueError(f'获取剪贴板失败: {str(e)}')
        
    def _format_paste_response(self, paste: Dict[str, Any]) -> Dict[str, Any]:
        """格式化响应数据"""
        return {
            'name': paste['name'],
            'created_at': paste['created_at'],
            'expires_at': paste['expires_at'],
            'burn_after_read': paste['burn_after_read'],
            'views': paste['views'],
            'has_password': paste.get('has_password', False),
            'content': paste.get('content')
        }