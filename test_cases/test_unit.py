import unittest
import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "../twa_app")
sys.path.append(topdir)
import app as twa_app

class TwaUnitTests(unittest.TestCase):

    def setUp(self):
        twa_app.app.testing = True
        self.app = twa_app.app.test_client()

    def test_home(self):
        result = self.app.get('/')
        print(result)
        print("********")
        # Make your assertions