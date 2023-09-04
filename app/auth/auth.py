from flask import Blueprint, redirect, url_for, request, session, render_template

from app.auth import services

auth_blueprint = Blueprint('auth_bp', __name__)


@auth_blueprint.route('/')
def login():
    try:
        # Set up Spotify user authentication
        sp_oauth = services.create_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    except AttributeError as e:
        # Error generating authentication
        return render_template('error.html')


@auth_blueprint.route('/callback')
def callback():
    try:
        code = request.args.get('code')
        sp_oauth = services.create_spotify_oauth()
        session.clear()
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info
        return redirect(url_for('home_bp.index'))

    except AttributeError as e:
        # Error generating authentication
        return render_template('error.html')
