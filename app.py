from flask import Flask, render_template, session, redirect, request, url_for, g
from user import User
from database import Database
import requests
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token

app = Flask(__name__)
app.secret_key = '1234'

Database.initialise(database="learning", host="localhost", user="postgres", password="filsu90")

@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_data(session['screen_name'])

@app.route("/")
def homepage():
    return render_template('home.html')

@app.route("/login/twitter")
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    request_token = get_request_token()
    session['request_token'] = request_token

    return redirect(get_oauth_verifier_url(request_token))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

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
    return redirect(url_for('profile'))

@app.route("/profile")
def profile():
    return render_template('profile.html', user=g.user)

@app.route('/search')
def search():
    query = request.args.get('q')
    tweets = g.user.twitter_request(f'https://api.twitter.com/1.1/search/tweets.json?q={query}')
    tweet_list = [{'tweet' : tweet['text'], 'label' : 'neutral'} for tweet in tweets['statuses']]

    for tweet in tweet_list:
        response = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        json_response = response.json()
        tweet['label'] = json_response['label']

    return render_template('search.html', tw_list=tweet_list)

app.run(port=4995)