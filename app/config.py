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

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False