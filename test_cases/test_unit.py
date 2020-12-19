import unittest
import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "../twa_app")
sys.path.append(topdir)
import app as twa_app
from twitter_utils import get_random_word, analyze_tweets, get_tweets_by_app, parse_tweets

class TwaUnitTests(unittest.TestCase):

    def setUp(self):
        twa_app.app.testing = True
        self.app = twa_app.app.test_client()

    def test_home(self):
        res = self.app.get('/')
        self.assertTrue(res.status_code == 200)
        self.assertIn("Welcome to Twitter Analyzer!", res.get_data(as_text=True))
        self.assertIn("Explore and Analyze Tweets using", res.get_data(as_text=True))

    def test_search(self):
        res = self.app.get('/search')
        self.assertTrue(res.status_code == 200)
        self.assertIn("Twitter search", res.get_data(as_text=True))
        self.assertIn("*This search serves data for the past seven days.", res.get_data(as_text=True))
        self.assertIn("Search operators", res.get_data(as_text=True))

    def test_footer(self):
        res = self.app.get('/')
        self.assertIn("Copyright 2020 by", res.get_data(as_text=True))
        res = self.app.get('/search')
        self.assertIn("Copyright 2020 by", res.get_data(as_text=True))

    def test_empty_results(self):
        res = self.app.get('/results')
        self.assertTrue(res.status_code == 302)

    def test_get_random_word(self):
        random_word = get_random_word()
        self.assertTrue(len(random_word) > 0)

    def test_analyze_tweets(self):
        tweet_list = [{'tweet':"Analyze this tweet for unit testing"}]
        analyze_tweets(tweet_list)
        self.assertIn(tweet_list[0]['label'], ['neutral', 'pos', 'neg'])

    def test_get_tweets(self):
        tweets = get_tweets_by_app("test")
        tweets = parse_tweets(tweets)
        self.assertTrue(len(tweets[0]['tweet']) > 0)