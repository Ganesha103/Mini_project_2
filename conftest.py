# conftest.py


"""
Use conftest.py is used to Manage the WebDriver setup and teardown


Centralizes WebDriver setup making it reusable across your tests
"""


import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
   """Setup WebDriver"""
   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
   driver.maximize_window()
   """Test Executes Here"""
   yield driver
   """Cleanup after Test"""
   driver.quit()