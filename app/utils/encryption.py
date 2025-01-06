from cryptography.fernet import Fernet
from flask import current_app

def get_encryption_key():
    """获取加密密钥"""
    return current_app.config['ENCRYPTION_KEY'].encode()

def encrypt_content(content):
    """加密内容"""
    if not content:
        return None
    f = Fernet(get_encryption_key())
    return f.encrypt(content.encode()).decode()

def decrypt_content(encrypted_content):
    """解密内容"""
    if not encrypted_content:
        return None
    f = Fernet(get_encryption_key())
    return f.decrypt(encrypted_content.encode()).decode() 