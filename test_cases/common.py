import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import warnings

# HELPER METHODS
class CommonMethods():
    # Default browser
    BROWSER = "chrome"
    START_URL = "http://127.0.0.1:4995/"
    
    def get_driver(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        driver = webdriver.Chrome(options=self.get_options())
        driver.set_window_size(1920, 1080)
        driver.get(self.START_URL)
        return driver

    def get_options(self):
        options = Options()
        options.add_experimental_option('w3c', False)
        options.add_argument('-headless')
        return options
    
    def get_exeptions(self):
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        return ignored_exceptions

    def get_element(self, attr, driver):
        wait = WebDriverWait(driver, 20, ignored_exceptions=self.get_exeptions())
        element = wait.until(EC.presence_of_element_located(attr))
        return element

    def get_title(self, attr, text, driver):
        wait = WebDriverWait(driver, 20, ignored_exceptions=self.get_exeptions())
        wait.until(EC.text_to_be_present_in_element(attr, text))
        element = self.get_element(attr, driver)
        return element

    def move_and_click(self, attr, driver):
        element = self.get_element(attr, driver)
        action_chains = ActionChains(driver)
        action_chains.move_to_element(element).click().perform()
    
    def get_click_element(self, attr, driver):
        wait = WebDriverWait(driver, 20, ignored_exceptions=self.get_exeptions())
        element = wait.until(EC.element_to_be_clickable(attr))
        return element

    def get_table(self, attr, driver):
        wait = WebDriverWait(driver, 20, ignored_exceptions=self.get_exeptions())
        chart = wait.until(EC.visibility_of_element_located(attr))
        return chart