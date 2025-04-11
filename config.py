import os
from datetime import timedelta


class Config:
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    
    # CSRF配置
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY', 'csrf-key')
    WTF_CSRF_TIME_LIMIT = 3600  # CSRF token有效期：1小时
    
    # 粘贴内容配置
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 最大50MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # 加密和安全配置
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', 'your-encryption-key')
    ENABLE_ENCRYPTION = True
    
    # 过期时间配置（秒）
    DEFAULT_EXPIRATION = 7 * 24 * 60 * 60  # 7天
    MAX_EXPIRATION = 30 * 24 * 60 * 60     # 30天
    
    # 访问控制
    MAX_VIEWS = 100  # 最大访问次数
    ENABLE_PASSWORD_PROTECTION = True

    # Redis配置
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_PORT = int(os.environ.get('REDIS_PORT') or 6379)
    REDIS_DB = int(os.environ.get('REDIS_DB') or 0)
    
    # 邮件服务器配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-app-password'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'your-email@gmail.com'
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL') or 'your-email@gmail.com'

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 2592000  # 30天
    PREFERRED_URL_SCHEME = 'https'
    # 确保跨域请求安全
    CORS_SUPPORTS_CREDENTIALS = True
    # 强制重定向到HTTPS
    FORCE_HTTPS = True

def get_config():
    """根据环境变量返回适当的配置"""
    env = os.environ.get('FLASK_ENV', 'production')
    if env == 'development':
        return DevelopmentConfig
    return ProductionConfig 