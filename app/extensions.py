from flask_cors import CORS
from flask_assets import Environment

# 初始化CORS
cors = CORS()

# 初始化Assets
assets = Environment()

def init_extensions(app):
    """初始化所有Flask扩展"""
    cors.init_app(app)
    assets.init_app(app)