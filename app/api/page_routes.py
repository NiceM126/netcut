from flask import Blueprint, render_template

bp = Blueprint('pages', __name__, url_prefix='/pages')

@bp.route('/about')
def about():
    """关于页面"""
    return render_template('pages/about.html')

@bp.route('/help')
def help():
    """帮助页面"""
    return render_template('pages/help.html')

@bp.route('/terms')
def terms():
    """服务条款页面"""
    return render_template('pages/terms.html')

@bp.route('/privacy')
def privacy():
    """隐私政策页面"""
    return render_template('pages/privacy.html')

@bp.route('/contact')
def contact():
    """联系我们页面"""
    return render_template('pages/contact.html') 