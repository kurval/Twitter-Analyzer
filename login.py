#!/usr/bin/python3
from user import User
from database import Database
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token

Database.initialise(database="learning", host="localhost", user="postgres", password="filsu90")

user_email = input("Enter your email: ")
user = User.load_data(user_email)
if not user:
    request_token = get_request_token()

    oauth2_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth2_verifier)

    first_name = input("Enter you first name: ")
    last_name = input("Enter your last name ")

    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=from%3ArealDonaldTrump')

for tweet in tweets['statuses']:
    print(tweet['text'])