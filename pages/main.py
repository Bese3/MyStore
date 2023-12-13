#!/usr/bin/python3
"""
main WSGI for rendering HTML pages
"""
from flask import Flask, make_response, url_for, redirect, render_template, session, abort
from authlib.integrations.flask_client import OAuth
from os import getenv
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = "secret"
oauth = OAuth(app)
# registering my oauth in `https://accounts.google.com`
oauth.register(
    "google",
    client_id=getenv('client_id'),
    client_secret=getenv('client_secret'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri = "https://www.googleapis.com/oauth2/v3/certs",
    prompt='consent',
    redirect_uri='https://www.besufikadyilma.tech'
)


@app.route("/login", strict_slashes=False)
def login():
    """
    The login function checks if the user is already logged in
    and redirects them to the home page if they are, otherwise
    it redirects them to the Google authorization page.
    """
    try:
        if 'user' in session:
            return redirect(url_for('home'))
    except KeyError:
        return oauth.google.authorize_redirect(redirect_uri="https://www.besufikadyilma.tech/authorize")
    return oauth.google.authorize_redirect(redirect_uri="https://www.besufikadyilma.tech/authorize")
    

@app.route("/home", strict_slashes=False)
def home():
    """
    The function checks if the user is logged in and redirects
    them to the Google OAuth authorization page if they are not,
    otherwise it renders the index.html template.
    """
    if 'user' not in session:
        return oauth.google.authorize_redirect(redirect_uri="https://www.besufikadyilma.tech/authorize")
    return render_template('index.html')


@app.route("/authorize", strict_slashes=False)
def authorize():
    """
    The `authorize` function authorizes access using a Google
    OAuth token and redirects the user to the home page.
    """
    token = oauth.google.authorize_access_token()
    session['user'] = token
    return redirect(url_for("home"))

@app.route("/landing", strict_slashes=False)
def get_landing():
    """
    The function `get_landing` returns the rendered template
    for the landing page.
    """
    return render_template("landing.html")


@app.route("/session", strict_slashes=False)
def get_session():
    """
    The function `get_session` returns a response containing
    the user's userinfo from the session.
    """
    return(make_response(session['user']['userinfo']), 200)


@app.route("/logout", strict_slashes=False)
def logout():
    """
    The function `logout` clears the session and redirects the
    user to the landing page, while also retrieving the user's
    id token if it exists in the session.
    """
    if 'user' in session:
        id_token = session['user']['id_token']
    session.clear()
    return redirect(url_for('get_landing'))


@app.route("/about", strict_slashes=False)
def about():
    """
    The function checks if the user is logged in and redirects
    to a Google authorization page if not, otherwise it renders
    the "about.html" template.
    """
    if 'user' not in session:
        return oauth.google.authorize_redirect(redirect_uri="https://www.besufikadyilma.tech/authorize")
    return render_template("about.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=5002)   
