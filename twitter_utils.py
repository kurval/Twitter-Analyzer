import constants
import requests
import json
import urllib.parse as urlparse
from flask import abort
import random

def encode_query(query):
    if query[0] == '@':
        query = query.replace('@', 'from:', 1)
    return urlparse.quote_plus(query)

def get_tweets_by_user(user, query):
    return user.twitter_request(f"{constants.SEARCH_URL}?q={query}")

def get_tweets_by_app(query):
    headers = {
        "Authorization": "Bearer " + constants.BEARER}
    content = requests.get(f"{constants.SEARCH_URL}?q={query}", headers=headers)
    if content.status_code != 200:
        abort(400)
    return json.loads(content.text)

def parse_tweets(tweets):
    return [{'tweet' : tweet['text'],
                    'name' : tweet['user']['name'],
                    'screen_name' : tweet['user']['screen_name'],
                    'time' : tweet['created_at'].split('+')[0] + 'UTC',
                    'id' : tweet['id_str'],
                    'url' : 'https://twitter.com/' +  tweet['user']['screen_name'] + '/status/' + tweet['id_str'],
                    'label' : 'neutral'} 
                    for tweet in tweets['statuses']]

def analyze_tweets(tweet_list):
    for tweet in tweet_list:
        response = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        if response.status_code != 200:
            abort(400)
        json_response = response.json()
        tweet['label'] = json_response['label']

def get_random_word():
    response = requests.get("https://www.mit.edu/~ecprice/wordlist.10000")
    if response.status_code != 200:
            abort(400)
    WORDS = response.content.splitlines()
    word = random.choice(WORDS)
    return word.decode('utf-8')