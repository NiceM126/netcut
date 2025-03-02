from flask import Blueprint, render_template, request, jsonify, abort, session
from ..services.mail_service import MailService
from ..services.paste_service import PasteService

bp = Blueprint('paste', __name__)
# bp = Blueprint('paste', __name__, url_prefix='/netcut')

mail_service = MailService()
paste_service = PasteService()

@bp.route('/')
def index():
    """渲染首页"""
    return render_template('index.html')

@bp.route('/<paste_name>', methods=['GET', 'POST'])
def paste(paste_name):
    """处理剪贴板的创建和访问"""
    try:
        # 验证剪贴板名称
        if not paste_name or len(paste_name) < 2:  # 至少2个字符
            return jsonify({'error': '剪贴板名称太短'}), 400
            
        if len(paste_name) > 50:  # 最多50个字符
            return jsonify({'error': '剪贴板名称太长'}), 400
            
        # 检查是否是纯数字
        if paste_name.isdigit():
            return jsonify({'error': '剪贴板名称不能是纯数字'}), 400
            
        # 检查字符是否合法（允许字母、数字、连字符和下划线）
        if not all(c.isalnum() or c in '-_' for c in paste_name):
            return jsonify({'error': '剪贴板名称只能包含字母、数字、连字符和下划线'}), 400
        
        if request.method == 'POST':
            # 处理保存请求
            data = request.get_json()
            if not data:
                return jsonify({'error': '无效的请求数据'}), 400

            # 如果是创建/更新请求（包含content字段   
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
                
                # 如果剪贴板存在且有密码，但未认证，则跳转到密码页
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
            'views': paste.get('views'),
            'redirect_url': f'/netcut/{paste_name}'
        })
            
    except Exception as e:
        print(f"验证过程出错: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@bp.route('/api/contact', methods=['POST'])
def handle_contact():
    """处理联系表单提交"""
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['name', 'email', 'subject', 'message']
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                'status': 'error',
                'message': f'{field} 是必填项'
            }), 400
    
    # 发送邮件
    success, error_message = mail_service.send_contact_email(
        name=data['name'],
        email=data['email'],
        subject=data['subject'],
        message=data['message']
    )
    
    if success:
        return jsonify({
            'status': 'success',
            'message': '消息已发送，我们会尽快回复您'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f'发送失败: {error_message}，请稍后重试'
        }), 500    