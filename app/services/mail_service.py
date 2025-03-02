"""邮件服务"""
from flask_mail import Mail, Message
from flask import current_app
import traceback

mail = Mail()

class MailService:
    def send_contact_email(self, name, email, subject, message):
        """发送联系表单邮件"""
        try:
            # 检查每个必需的配置项
            required_configs = {
                'MAIL_SERVER': current_app.config.get('MAIL_SERVER'),
                'MAIL_PORT': current_app.config.get('MAIL_PORT'),
                'MAIL_USERNAME': current_app.config.get('MAIL_USERNAME'),
                'MAIL_PASSWORD': current_app.config.get('MAIL_PASSWORD'),
                'CONTACT_EMAIL': current_app.config.get('CONTACT_EMAIL')
            }
            
            # 检查缺失的配置项
            missing_configs = [key for key, value in required_configs.items() if not value]
            if missing_configs:
                raise ValueError(f"邮件服务器配置不完整，缺少以下配置项: {', '.join(missing_configs)}")

            # 记录发送邮件的配置信息
            current_app.logger.info(f'准备发送邮件，配置信息：\n'
                                  f'MAIL_SERVER: {current_app.config.get("MAIL_SERVER")}\n'
                                  f'MAIL_PORT: {current_app.config.get("MAIL_PORT")}\n'
                                  f'MAIL_USE_TLS: {current_app.config.get("MAIL_USE_TLS")}\n'
                                  f'MAIL_USERNAME: {current_app.config.get("MAIL_USERNAME")}\n'
                                  f'CONTACT_EMAIL: {current_app.config.get("CONTACT_EMAIL")}\n'
                                  f'发件人: {current_app.config.get("MAIL_USERNAME")}\n'
                                  f'收件人: {current_app.config.get("CONTACT_EMAIL")}')
            
            # 创建邮件内容
            body = f"""
来自联系表单的新消息：

发送者：{name}
邮箱：{email}
主题：{subject}

消息内容：
{message}
            """
            
            # 创建邮件对象
            msg = Message(
                subject=f'[NetCut] 新的联系表单消息: {subject}',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[current_app.config['CONTACT_EMAIL']],
                body=body,
                reply_to=email
            )
            
            # 发送邮件
            mail.send(msg)
            current_app.logger.info('邮件发送成功')
            return True, None
            
        except Exception as e:
            error_info = traceback.format_exc()
            current_app.logger.error(f'发送邮件失败: {str(e)}\n堆栈跟踪:\n{error_info}')
            return False, str(e) 