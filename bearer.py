import constants
import urllib.parse as urlparse
import base64
import requests
import json

OAUTH2_TOKEN = 'https://api.twitter.com/oauth2/token'

def get_bearer_token(consumer_key, consumer_secret):
    # enconde consumer key
    consumer_key = urlparse.quote(consumer_key)
    # encode consumer secret
    consumer_secret = urlparse.quote(consumer_secret)
    # create bearer token
    bearer_token = consumer_key + ':' + consumer_secret
    # base64 encode the token
    base64_encoded_bearer_token = base64.b64encode(bearer_token.encode('utf-8'))
    # set headers
    headers = {
        "Authorization": "Basic " + base64_encoded_bearer_token.decode('utf-8'),
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}

    response = requests.post(OAUTH2_TOKEN, headers=headers, data={'grant_type': 'client_credentials'})
    to_json = response.json()
    # print("token_type = %s\naccess_token  = %s" % (to_json['token_type'], to_json['access_token']))

def twitter_request_bearer(query):
    headers = {
        "Authorization": "Bearer " + constants.BEARER}
    content = requests.get(f"{constants.SEARCH_URL}?q={urlparse.quote_plus(query)}", headers=headers)
    return json.loads(content.text)

