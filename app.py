from flask import Flask, render_template, session, redirect, request, url_for, g, flash, abort
import error_handlers
from database import Database
from user import User
import ssl
from twitter_auth import get_request_token,get_oauth_verifier_url, get_access_token
from twitter_utils import get_tweets_by_user,\
                            get_tweets_by_app,\
                            parse_tweets,\
                            analyze_tweets,\
                            encode_query

app = Flask(__name__)
app.register_blueprint(error_handlers.blueprint)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = '1234'

Database.initialise(database="learning", host="localhost", user="postgres", password="filsu90")

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
    access_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.load_data(access_token['screen_name'])
    if not user:
        user = User(acces_token['screen_name'], acces_token['oauth_token'],
                    acces_token['oauth_token_secret'], None)
        user.save_to_db()

    session['screen_name'] = user.screen_name
    flash("You have been successfully logged in!", "success")
    return redirect(url_for('search'))

@app.route("/")
def homepage():
    return render_template('login.html')

@app.route("/search")
def search():
    if 'quest' and 'screen_name' not in session:
        session['quest'] = 'anonymous'
        flash("Hello stranger!", "success")

    if 'screen_name' in session:
        return render_template('search.html', user=g.user)
    return render_template('search.html', user=None)

@app.route('/results')
def results():
    query = encode_query(request.args.get('q'))
    if 'screen_name' in session:
        user=g.user
        tweets = get_tweets_by_user(user, query)
    else:
        user=None
        tweets = get_tweets_by_app(query)

    tweet_list = parse_tweets(tweets)
    analyze_tweets(tweet_list)
    return render_template('result.html', tw_list=tweet_list, user=user)

if __name__ == '__main__':
    context = ssl.SSLContext()
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(port=4995, debug=True, ssl_context=context)