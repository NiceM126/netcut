from flask import Blueprint, render_template, abort, request, jsonify, redirect, url_for
from .services.paste_service import PasteService

bp = Blueprint('main', __name__)
paste_service = PasteService()

@bp.route('/')
def index():
    """渲染首页"""
    return render_template('index.html')

@bp.route('/pages/<page_name>')
def static_page(page_name):
    """处理静态页面"""
    try:
        return render_template(f'pages/{page_name}.html')
    except:
        abort(404)

@bp.route('/<paste_name>', methods=['GET', 'POST'])
def paste(paste_name):
    """处理剪贴板的创建和访问"""
    # 验证剪贴板名称
    if not paste_name.replace('-', '').replace('_', '').isalnum():
        abort(404)
        
    if request.method == 'POST':
        # 处理保存请求
        data = request.get_json()
        try:
            result = paste_service.create_paste(
                paste_name=paste_name,
                content=data.get('content'),
                expiration=data.get('expiration'),
                password=data.get('password'),
                burn_after_read=data.get('burn_after_read', False),
                syntax=data.get('syntax')
            )
            return jsonify(result)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    else:
        # 处理获取请求
        try:
            paste = paste_service.get_paste(paste_name)
            if paste is None:
                # 如果剪贴板不存在，返回编辑页面
                return render_template('edit.html', paste_name=paste_name)
                
            # 如果需要密码
            if paste.get('has_password') and not paste.get('content'):
                return render_template('password.html', paste_name=paste_name)
                
            # 直接显示编辑页面
            return render_template('edit.html', paste_name=paste_name, paste=paste)
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 401

@bp.route('/<paste_name>/raw')
def raw(paste_name):
    """获取原始内容"""
    try:
        paste = paste_service.get_paste(paste_name)
        if paste is None:
            abort(404)
            
        if paste.get('has_password'):
            password = request.args.get('password')
            if not password:
                return jsonify({'error': 'Password required'}), 401
                
        return paste.get('content', ''), 200, {
            'Content-Type': 'text/plain; charset=utf-8'
        }
    except ValueError as e:
        return jsonify({'error': str(e)}), 401