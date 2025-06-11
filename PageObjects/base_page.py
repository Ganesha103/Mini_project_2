# base_page.py


"""
The BasePage Class includes common methods like find elements, clicks and interact with UI
"""


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from common import Config


class BasePage:


   def __init__(self, driver):
       self.driver = driver
       self.timeout = Config().TIMEOUT


   def find_element(self, locator):
       try:
           web_element = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))
           return web_element
       except (NoSuchElementException, ElementNotVisibleException, TimeoutException):
           raise Exception(f"Element {locator} not found within {self.timeout} seconds")


   def is_visible(self, locator):
       try:
           web_element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))
           return web_element
       except (NoSuchElementException, ElementNotVisibleException, TimeoutException):
           return False


   def is_enabled(self, locator):
       try:
           web_element = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(locator))
           return web_element
       except (NoSuchElementException, ElementNotVisibleException, TimeoutException):
           return False


   def click(self, locator):
       element = self.find_element(locator) and self.is_visible(locator) and self.is_enabled(locator)
       element.click()


   def enter_text(self, locator, text):
       element = self.find_element(locator)
       element.click()
       element.send_keys(text)
