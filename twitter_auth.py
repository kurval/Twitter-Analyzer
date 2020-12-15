import oauth2
import constants
from flask import redirect, flash
import urllib.parse as urlparse

consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

def get_request_token():
    '''
    Uses the client to perform a request for the request token
    and gets the request token by parsing the query string returned.
    '''
    client = oauth2.Client(consumer)
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        flash("An error occured when trying to login. \
                Please try again or continue without login", "danger")
        return redirect(url_for('homepage'))
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def get_oauth_verifier_url(request_token):
    return f"{constants.AUTHORIZATION_URL}?oauth_token={request_token['oauth_token']}"

def get_access_token(request_token, oauth_verifier):
    '''
    Creates a Token object which constains the request token, and the verifier.
    Creates a client with consumer (twa app) and the newly created (and verified) token.
    Ask Twitter for an access token, and Twitter knows it should give us it
    because we've verified request token.
    '''
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth2.Client(consumer, token)
    response, content = client.request(constants.ACCES_TOKEN_URL, 'POST')
    if response.status != 200:
        flash("An error occured when trying to login. \
                Please try again or continue without login", "danger")
        return redirect(url_for('homepage'))
    return dict(urlparse.parse_qsl(content.decode('utf-8')))