from flask import Flask, render_template, session, redirect, request, url_for, g, flash, abort
import error_handlers
from database import Database
import urllib.parse as urlparse
from user import User
import sys
import os
from flask_sqlalchemy import SQLAlchemy
from twitter_auth import get_request_token,get_oauth_verifier_url, get_access_token
from twitter_utils import get_tweets_by_user,\
                            get_tweets_by_app,\
                            parse_tweets,\
                            analyze_tweets,\
                            encode_query,\
                            get_random_word

app = Flask(__name__)
app.register_blueprint(error_handlers.blueprint)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = os.environ.get('SECRET_KEY', 'dev')

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

Database.initialise(database=dbname, host=host, port=port, user=user, password=password)

@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_data(session['screen_name'])

@app.route('/logout')
def logout():
    logout = True if 'screen_name' in session else False
    session.clear()
    if logout:
        flash("You have been successfully logged out!", "success")
    else:
        flash("Goodbye stranger!", "success")
    return redirect(url_for('homepage'))

@app.route("/login/twitter")
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('search'))
    request_token = get_request_token()
    session['request_token'] = request_token
    return redirect(get_oauth_verifier_url(request_token))

@app.route("/auth/twitter")
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    if not oauth_verifier:
        abort(401)
    access_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.load_data(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'],
                    access_token['oauth_token_secret'], None)
        user.save_to_db()

    session['screen_name'] = user.screen_name
    flash("You have been successfully logged in!", "success")
    return redirect(url_for('search'))

@app.route("/")
def homepage():
    return render_template('login.html')

@app.route("/search")
def search():
    if 'quest' not in session and 'screen_name' not in session:
        session['quest'] = 'anonymous'
        flash("Hello stranger! Go ahead and run your first Twitter search or use random search.", "success")

    if 'screen_name' in session:
        return render_template('search.html', user=g.user)
    return render_template('search.html', user=None)

@app.route('/results')
def results():
    r = request.args.get('r')
    query = request.args.get('q')
    if r == "random":
        query = get_random_word()
    elif not query:
        flash("Empty search. See the table above of how to use search operators or use random search.", "danger")
        return redirect(url_for('search'))
    elif len(query) > 100:
        flash("Wow! Your query is way too long (max 100 characters). Try another one.", "danger")
        return redirect(url_for('search'))

    encoded_query = encode_query(query)
    if 'screen_name' in session:
        user=g.user
        tweets = get_tweets_by_user(user, encoded_query)
    else:
        user=None
        tweets = get_tweets_by_app(encoded_query)

    tweet_list = parse_tweets(tweets)
    analyze_tweets(tweet_list)
    return render_template('result.html', tw_list=tweet_list, user=user, query=query)

if __name__ == '__main__':
    app.run()