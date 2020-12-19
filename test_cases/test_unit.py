import twa_app.app as twa_app
import unittest

class TwaUnitTests(unittest.TestCase):

    def setUp(self):
        twa_app.app.testing = True
        self.app = twa_app.app.test_client()

    def test_home(self):
        result = self.app.get('/')
        print(result)
        print("********")
        # Make your assertions