from flask import Blueprint, render_template, request, jsonify, abort, current_app, session
from ..services.paste_service import PasteService

bp = Blueprint('paste', __name__)

@bp.route('/')
def index():
    """渲染首页"""
    return render_template('index.html')

@bp.route('/<paste_name>', methods=['GET', 'POST'])
def paste(paste_name):
    """处理剪贴板的创建和访问"""
    try:
        # 验证剪贴板名称
        if not paste_name.replace('-', '').replace('_', '').isalnum():
            abort(404)
            
        paste_service = PasteService()
        
        if request.method == 'POST':
            # 处理保存请求
            data = request.get_json()
            if not data:
                return jsonify({'error': '无效的请求数据'}), 400
                
            try:
                print(f"创建剪贴板: {paste_name}")
                print(f"请求数据: {data}")
                result = paste_service.create_paste(
                    paste_name=paste_name,
                    content=data.get('content'),
                    expiration=data.get('expiration'),
                    password=data.get('password'),
                    burn_after_read=data.get('burn_after_read', False)
                )
                print(f"创建结果: {result}")
                return jsonify(result)
            except ValueError as e:
                print(f"创建失败: {str(e)}")
                return jsonify({'error': str(e)}), 400
        else:
            # 处理获取请求
            try:
                print(f"获取剪贴板: {paste_name}")
                # 检查是否已通过密码验证
                is_authenticated = session.get(f'paste_auth_{paste_name}', False)
                
                # 尝试获取剪贴板内容
                paste = paste_service.get_paste(paste_name, None if not is_authenticated else '')
                
                if paste is None:
                    print("剪贴板不存在，返回编辑页面")
                    return render_template('edit.html', paste_name=paste_name)
                
                if paste.get('has_password'):
                    if not is_authenticated:
                        print("需要密码访问")
                        return render_template('password.html', paste_name=paste_name)
                    else:
                        # 从会话中获取已解密的内容
                        paste['content'] = session.get(f'paste_content_{paste_name}')
                
                print("返回编辑页面")
                return render_template('edit.html', paste_name=paste_name, paste=paste)
                
            except ValueError as e:
                print(f"获取失败: {str(e)}")
                return jsonify({'error': str(e)}), 401
    except Exception as e:
        import traceback
        error_info = traceback.format_exc()
        print(f"处理请求时出错: {error_info}")
        return jsonify({
            'error': '服务器内部错误',
            'details': str(e),
            'traceback': error_info
        }), 500

@bp.route('/<paste_name>/raw')
def raw(paste_name):
    """获取原始内容"""
    paste_service = PasteService()
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

@bp.route('/<paste_name>/verify', methods=['POST'])
def verify_password(paste_name):
    """验证剪贴板密码"""
    try:
        print(f"收到密码验证请求: {paste_name}")
        data = request.get_json()
        print(f"请求数据: {data}")
        
        if not data or 'password' not in data:
            print("未提供密码")
            return jsonify({'error': '请提供密码'}), 400
            
        paste_service = PasteService()
        print("验证密码...")
        
        # 先验证密码
        if not paste_service.verify_paste_password(paste_name, data['password']):
            print("密码验证失败")
            return jsonify({'error': '密码错误'}), 401
            
        print("密码验证成功")
        # 获取完整的剪贴板内容
        paste = paste_service.get_paste(paste_name, data['password'])
        if not paste:
            return jsonify({'error': '剪贴板不存在'}), 404
            
        # 设置会话标记，表示已通过密码验证
        session[f'paste_auth_{paste_name}'] = True
        session[f'paste_content_{paste_name}'] = paste.get('content')
        
        return jsonify({
            'status': 'success',
            'content': paste.get('content'),
            'name': paste.get('name'),
            'created_at': paste.get('created_at'),
            'expires_at': paste.get('expires_at'),
            'burn_after_read': paste.get('burn_after_read'),
            'views': paste.get('views')
        })
            
    except Exception as e:
        print(f"验证过程出错: {str(e)}")
        return jsonify({'error': str(e)}), 500