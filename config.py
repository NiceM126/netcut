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

    # 邮件服务器配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-app-password'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'your-email@gmail.com'
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL') or 'your-email@gmail.com' 