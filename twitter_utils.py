import oauth2
import constants
import urllib.parse as urlparse

consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

def get_request_token():
    # Create a consumer, which uses CONSUMER_KEY and CONSUMER_SECRET to identify our app uniquely
    client = oauth2.Client(consumer)

    # Use the client to perform a request for the request token
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        print("An error occured gettin the request token from Twitter! ")

    # Get the request token by parsing the query string returned
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def get_oauth_verifier_url(request_token):
    return f"{constants.AUTHORIZATION_URL}?oauth_token={request_token['oauth_token']}"

def get_access_token(request_token, oauth_verifier):
    # Create a Token object which constains the request token, and the verifier
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    # Create a client with our consumer (our app) and the newly created (and verified) token
    client = oauth2.Client(consumer, token)

    # Ask Twitter for an access token, and Twitter knows it should give us it because we've verified request token
    response, content = client.request(constants.ACCES_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))
