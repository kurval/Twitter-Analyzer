from flask import Flask, render_template, session, redirect, request, url_for, g, flash
from user import User
from database import Database
import requests
import urllib.parse
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token, get_tweets_by_user
from bearer import twitter_request_bearer
import ssl

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = '1234'

Database.initialise(database="learning", host="localhost", user="postgres", password="filsu90")

@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_data(session['screen_name'])

@app.route('/logout')
def logout():
    session.clear()
    flash("Goodbye!", "success")
    return redirect(url_for('homepage'))

@app.route("/login/twitter")
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('search'))
    request_token = get_request_token()
    session['request_token'] = request_token
    flash("Logged in succesfully", "success")
    return redirect(get_oauth_verifier_url(request_token))

@app.route("/auth/twitter")
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    if not oauth_verifier:
        return redirect(url_for('homepage'))
    acces_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.load_data(acces_token['screen_name'])
    if not user:
        user = User(acces_token['screen_name'], acces_token['oauth_token'],
                    acces_token['oauth_token_secret'], None)
    user.save_to_db()

    session['screen_name'] = user.screen_name
    return redirect(url_for('search'))

@app.route("/")
def homepage():
    return render_template('login.html')

@app.route("/search")
def search():
    if 'quest' not in session and 'screen_name' not in session:
        session['quest'] = 'anonymous'
        flash("Hello stranger!", "success")

    if 'screen_name' in session:
        return render_template('search.html', user=g.user)
    return render_template('search.html', user=None)

@app.route('/results')
def results():
    query = request.args.get('q')
    if not query:
        return redirect(url_for('search'))
    if 'screen_name' in session:
        user=g.user
        tweets = get_tweets_by_user(g.user, query)
    else:
        user=None
        tweets = twitter_request_bearer(query)
    tweet_list = [{'tweet' : tweet['text'],
                    'name' : tweet['user']['name'],
                    'screen_name' : tweet['user']['screen_name'],
                    'time' : tweet['created_at'].split('+')[0] + 'UTC',
                    'id' : tweet['id_str'],
                    'url' : 'https://twitter.com/' +  tweet['user']['screen_name'] + '/status/' + tweet['id_str'],
                    'label' : 'neutral'} 
                    for tweet in tweets['statuses']]

    for tweet in tweet_list:
        response = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        json_response = response.json()
        tweet['label'] = json_response['label']

    return render_template('result.html', tw_list=tweet_list, user=user)

if __name__ == '__main__':
    context = ssl.SSLContext()
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(port=4995, debug=True, ssl_context=context)