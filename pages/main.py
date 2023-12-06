#!/usr/bin/python3
from flask import Flask, make_response, url_for, redirect, render_template, session, abort
from authlib.integrations.flask_client import OAuth
from os import getenv
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = "secret_key"
oauth = OAuth(app)
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
    redirect_uri='http://web-02.besufikadyilma.tech'
)
my_token = oauth.google.authorize_access_token()

@app.route("/login", strict_slashes=False)
def login():
    try:
        if 'user' in session:
            return redirect(url_for('home'))
    except KeyError:
        abort(401)
    return oauth.google.authorize_redirect(redirect_uri="http://web-02.besufikadyilma.tech/authorize")

@app.route("/home", strict_slashes=False)
def home():
    if 'user' not in session:
        return oauth.google.authorize_redirect(redirect_uri="http://web-02.besufikadyilma.tech/authorize")
    return render_template('index.html')


@app.route("/authorize", strict_slashes=False)
def authorize():
    token = oauth.google.authorize_access_token()
    session['user'] = token
    # print(session)
    return redirect(url_for("home"))

@app.route("/landing", strict_slashes=False)
def get_landing():
    return render_template("landing.html")


@app.route("/session", strict_slashes=False)
def get_session():
    # print(session)
    global my_token
    session['user'] = my_token
    print(session)
    return(make_response(session['user']['userinfo']), 200)


@app.route("/logout", strict_slashes=False)
def logout():
    if 'user' in session:
        id_token = session['user']['id_token']
    session.clear()
    return redirect(url_for('get_landing'))


@app.route("/about", strict_slashes=False)
def about():
    if 'user' not in session:
        return oauth.google.authorize_redirect(redirect_uri="http://web-02.besufikadyilma.tech/authorize")
    return render_template("about.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=5002)   
