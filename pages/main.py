#!/usr/bin/python3
from flask import Flask, make_response, url_for, redirect, render_template, session, abort
from authlib.integrations.flask_client import OAuth
app = Flask(__name__)
app.secret_key = "secret_key"
oauth = OAuth(app)
oauth.register(
    "google",
    client_id='179378167801-28sqsjfef75o1aumirn09o8fp8c9d6db.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri = "https://www.googleapis.com/oauth2/v3/certs",
    prompt='consent',
)

@app.route("/login", strict_slashes=False)
def login():
    try:
        if 'user' in session:
            abort(404)
    except KeyError:
        abort(401)
    return oauth.google.authorize_redirect(redirect_uri=url_for('authorize', _external=True))

@app.route("/home", strict_slashes=False)
def home():
    if 'user' not in session:
        return oauth.google.authorize_redirect(redirect_uri=url_for('authorize', _external=True))
    return render_template('index.html', user=session['user'])


@app.route("/authorize", strict_slashes=False)
def authorize():
    token = oauth.google.authorize_access_token()
    session['user'] = token
    return redirect(url_for("home"))


@app.route("/logout", strict_slashes=False)
def logout():
    if 'user' in session:
        id_token = session['user']['id_token']
    else:
        abort(401)
    session.clear()
    return redirect(url_for('login'))


@app.route("/session", strict_slashes=False)
def get_session():
    return(make_response(session['user']), 200)


if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=5002)   
