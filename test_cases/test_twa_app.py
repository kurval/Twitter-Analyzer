import unittest
from test_cases.common import CommonMethods
from test_cases.resources.locators import PageLocators
from selenium.webdriver.common.by import By
import time

class TwaTests(unittest.TestCase):

    cm = CommonMethods()
    pl = PageLocators()
    def setUp(self):
        self.driver = self.cm.get_driver()

    def test_login(self):
        login_btn = self.cm.get_click_element((By.ID, 'lg-ano'), self.driver)
        login_btn.click()
        time.sleep(3)
        alert = self.cm.get_element((By.ID, 'tw-alert'), self.driver)
        self.assertEqual("Hello stranger! Go ahead and run your first Twitter search or use Random search.", alert.text)
        search = self.cm.get_element((By.ID, 'tw-search'), self.driver)
        self.assertEqual("Twitter search", search.text)
    
    def tearDown(self):
        self.driver.close()