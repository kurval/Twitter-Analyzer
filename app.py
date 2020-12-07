from flask import Flask, render_template, session, redirect, request
from user import User
from database import Database
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token

app = Flask(__name__)
app.secret_key = '1234'

Database.initialise(database="learning", host="localhost", user="postgres", password="filsu90")

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/login/twitter")
def twitter_login():
    request_token = get_request_token()
    session['request_token'] = request_token

    return redirect(get_oauth_verifier_url(request_token))

@app.route("/auth/twitter")
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    acces_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.load_data(acces_token['screen_name'])
    if not user:
        user = User(acces_token['screen_name'], acces_token['oauth_token'],
                    acces_token['oauth_token_secret'], None)
    user.save_to_db()

    session['screen_name'] = user.screen_name
    return user.screen_name

app.run(port=4995)