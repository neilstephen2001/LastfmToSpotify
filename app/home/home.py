from flask import Blueprint, redirect, url_for, session, render_template

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/home')
def index():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('auth_bp.login'))
    else:
        return render_template('index.html')


@home_blueprint.route('/return-home', methods=['POST'])
def return_home():
    return redirect(url_for('home_bp.index'))
