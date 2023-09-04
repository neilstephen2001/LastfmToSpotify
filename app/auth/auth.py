from flask import Blueprint, redirect, url_for, request, session

from app.auth import services

auth_blueprint = Blueprint('auth_bp', __name__)


@auth_blueprint.route('/')
def login():
    sp_oauth = services.create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@auth_blueprint.route('/callback')
def callback():
    code = request.args.get('code')
    sp_oauth = services.create_spotify_oauth()
    session.clear()
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))
