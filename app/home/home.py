from flask import Blueprint, redirect, url_for, session, render_template, request, flash

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/')
def home():
    session['top_tracks'] = []
    session['playlist'] = None
    token_info = session.get('token_info', None)
    error_message = session.pop('home_form_error', None)
    if not token_info:
        return redirect(url_for('auth_bp.login'))
    else:
        return render_template('home.html', error_message=error_message)


@home_blueprint.route('/return-home', methods=['POST'])
def return_home():
    return redirect(url_for('home_bp.home'))


@home_blueprint.route('/error', methods=['POST'])
def error():
    return render_template('error.html')
