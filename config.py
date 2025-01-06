import os
from datetime import timedelta

class Config:
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    
    # Redis配置
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_PORT = int(os.environ.get('REDIS_PORT') or 6379)
    REDIS_DB = int(os.environ.get('REDIS_DB') or 0)
    
    # 加密配置
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or 'your-encryption-key-here'
    
    # 剪贴板配置
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    DEFAULT_EXPIRATION = int(timedelta(days=7).total_seconds())
    MAX_EXPIRATION = int(timedelta(days=30).total_seconds())
    
    # CSRF配置
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = False  # 只在表单提交时检查CSRF 