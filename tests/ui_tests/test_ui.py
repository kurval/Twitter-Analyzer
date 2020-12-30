import unittest
from common import CommonMethods
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import string
import time

class TwaUiTests(unittest.TestCase):

    cm = CommonMethods()
    def setUp(self):
        self.driver = self.cm.get_driver()

    def login_ano(self):
        login_btn = self.cm.get_click_element((By.ID, 'tw-ano'), self.driver)
        login_btn.click()

    def test_logout(self):
        self.login_ano()
        back_btn = self.cm.get_element((By.ID, 'tw-back'), self.driver)
        back_btn.click()
        alert = self.cm.get_element((By.ID, 'tw-alert'), self.driver)
        self.assertEqual("Goodbye stranger!", alert.text)

    def test_search_page(self):
        self.login_ano()
        alert = self.cm.get_element((By.ID, 'tw-alert'), self.driver)
        self.assertEqual("Hello stranger! Go ahead and run your first Twitter search or use random search.", alert.text)

    def test_random_search(self):
        self.login_ano()
        random_btn = self.cm.get_click_element((By.ID, 'tw-random'), self.driver)
        random_btn.click()
        badge = self.cm.get_element((By.ID, 'tw-badge-neg'), self.driver)
        self.assertEqual("Negative", badge.text)
        results = self.cm.get_table((By.ID, 'tw-results'), self.driver)
        self.assertTrue(results.is_displayed())

    def test_search(self):
        self.login_ano()
        search_btn = self.cm.get_click_element((By.ID, 'tw-search'), self.driver)
        search_btn.click()
        input_field = self.cm.get_element((By.ID, 'q'), self.driver)

        search_text = "@NASA"
        input_field.send_keys(search_text)
        input_field.send_keys(Keys.RETURN)
        results = self.cm.get_table((By.ID, 'tw-results'), self.driver).text
        self.assertIn(search_text, results)

    def test_search_over_max(self):
        self.login_ano()
        search_btn = self.cm.get_click_element((By.ID, 'tw-search'), self.driver)
        search_btn.click()
        input_field = self.cm.get_element((By.ID, 'q'), self.driver)

        letters = string.ascii_lowercase
        search_text = ''.join(random.choice(letters) for i in range(101))
        input_field.send_keys(search_text)
        input_field.send_keys(Keys.RETURN)

        alert = self.cm.get_element((By.ID, 'tw-alert'), self.driver)
        self.assertEqual("Wow! Your query is way too long (max 100 characters). Try another one.", alert.text)

    def tearDown(self):
        self.driver.close()