from flask import Flask, render_template, jsonify, request, session
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
import sys
import os

# 确保能够正确导入根目录的配置文件
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import get_config

from .api.paste_routes import bp as paste_bp
from .api.page_routes import bp as page_bp
from dotenv import find_dotenv, load_dotenv
from .extensions import init_extensions, mail
from datetime import datetime

# 初始化 CSRF 保护
csrf = CSRFProtect()

def create_app(config_class=None):
    """应用工厂函数"""
    app = Flask(__name__, static_url_path='/static')
    
    # 加载配置文件
    load_dotenv(find_dotenv('.env'))
    
    # 加载配置
    if config_class is None:
        config_class = get_config()
    
    app.config.from_object(config_class)
    
    # 检查是否在生产环境
    is_production = not app.config.get('DEBUG', False)
    
    # 如果在生产环境，确保安全设置
    if is_production:
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
    
    # 注册蓝图
    app.register_blueprint(page_bp, url_prefix='/pages')
    app.register_blueprint(paste_bp, url_prefix='/')

    # 打印邮件配置信息（调试用）
    # print("邮件配置信息:")
    # print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    # print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
    # print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    # print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    # print(f"CONTACT_EMAIL: {app.config.get('CONTACT_EMAIL')}")
    
    # 初始化扩展
    CORS(app)
    csrf.init_app(app)
    
    # 排除特定路由的CSRF保护
    csrf.exempt("paste.delete_paste")
    
    init_extensions(app)
    
    # 添加安全响应头
    def add_security_headers(response):
        # 防止MIME类型嗅探攻击
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # 替代Expires使用Cache-Control
        if 'Expires' in response.headers:
            del response.headers['Expires']
        # 设置缓存控制
        if 'Cache-Control' not in response.headers:
            response.headers['Cache-Control'] = 'no-store, max-age=0'
        # 使用CSP替代X-Frame-Options
        if 'X-Frame-Options' in response.headers:
            del response.headers['X-Frame-Options']
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response
    
    app.after_request(add_security_headers)
    
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
                self.expire_times = {}
                print("初始化内存数据库")
            
            def get(self, key):
                # 检查是否过期
                if key in self.expire_times:
                    if datetime.now().timestamp() > self.expire_times[key]:
                        self.delete(key)
                        return None
                value = self.data.get(key)
                print(f"获取键 {key}: {value}")
                return value
            
            def set(self, key, value, ex=None):
                print(f"设置键 {key}: {value}")
                self.data[key] = value
                # 如果之前设置了过期时间，需要清除
                if key in self.expire_times:
                    del self.expire_times[key]
            
            def delete(self, key):
                print(f"删除键 {key}")
                self.data.pop(key, None)
                if key in self.expire_times:
                    del self.expire_times[key]
            
            def expire(self, key, time):
                print(f"设置过期时间 {key}: {time}")
                if key in self.data:
                    self.expire_times[key] = datetime.now().timestamp() + time
            
            def ping(self):
                return True
        app.db = DictDB()
    
    # 注册错误处理
    def not_found_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': '接口未找到'}), 404
        return render_template('error.html', error='页面未找到'), 404
    app.errorhandler(404)(not_found_error)
        
    def internal_error(error):
        import traceback
        error_info = traceback.format_exc()
        print(f"500错误: {error_info}")
        return jsonify({
            'error': '服务器内部错误',
            'details': str(error),
            'traceback': error_info
        }), 500
    app.errorhandler(500)(internal_error)
    
    # 使用装饰器前先定义函数，然后再用装饰器注册
    def set_cookie_path():
        session.permanent = True
        app.config.update(
            SESSION_COOKIE_PATH = '/',
            SESSION_COOKIE_NAME = 'netcut_session',
            SESSION_COOKIE_SECURE = True,  # 只在HTTPS连接上发送cookie
            SESSION_COOKIE_HTTPONLY = True,  # 防止JavaScript访问Cookie
            SESSION_COOKIE_SAMESITE = 'Lax',  # 限制跨站请求时发送Cookie
            PERMANENT_SESSION_LIFETIME = 86400 * 30  # 30天，以秒为单位
        )
        # 确保应用识别到HTTPS
        if request.headers.get('X-Forwarded-Proto') == 'https':
            request.environ['HTTPS'] = 'on'
    
    app.before_request(set_cookie_path)
    
    return app