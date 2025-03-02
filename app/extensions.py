"""Flask扩展初始化"""
from flask_cors import CORS
from flask_mail import Mail

# 初始化CORS
cors = CORS()

# 初始化邮件服务
mail = Mail()

def init_extensions(app):
    """初始化所有Flask扩展"""
    cors.init_app(app)
    mail.init_app(app)