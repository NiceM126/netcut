from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from config import Config
from .api.paste_routes import bp as paste_bp
from .api.page_routes import bp as page_bp

# 初始化 CSRF 保护
csrf = CSRFProtect()

def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__)
    CORS(app)
    
    # 加载配置
    app.config.from_object(config_class)
    
    # 开启调试模式
    app.config['DEBUG'] = True
    
    # 初始化 CSRF 保护
    csrf.init_app(app)
    
    # 初始化 Redis 或使用内存存储
    try:
        import redis
        app.db = redis.Redis(
            host=app.config.get('REDIS_HOST', 'localhost'),
            port=app.config.get('REDIS_PORT', 6379),
            db=app.config.get('REDIS_DB', 0),
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1
        )
        app.db.ping()
        print("成功连接到 Redis 服务器")
    except Exception as e:
        print(f"无法连接到 Redis（{str(e)}），使用内存存储作为临时数据库")
        class DictDB:
            def __init__(self):
                self.data = {}
                print("初始化内存数据库")
            
            def get(self, key):
                value = self.data.get(key)
                print(f"获取键 {key}: {value}")
                return value
            
            def set(self, key, value, ex=None):
                print(f"设置键 {key}: {value}")
                self.data[key] = value
            
            def delete(self, key):
                print(f"删除键 {key}")
                self.data.pop(key, None)
            
            def expire(self, key, time):
                print(f"设置过期时间 {key}: {time}")
                pass
            
            def ping(self):
                return True
        app.db = DictDB()
    
    # 注册蓝图
    app.register_blueprint(paste_bp)
    app.register_blueprint(page_bp)  # 注册页面路由蓝图
    
    # 注册错误处理
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', error='页面未找到'), 404
        
    @app.errorhandler(500)
    def internal_error(error):
        import traceback
        error_info = traceback.format_exc()
        print(f"500错误: {error_info}")
        return jsonify({
            'error': '服务器内部错误',
            'details': str(error),
            'traceback': error_info
        }), 500
    
    return app