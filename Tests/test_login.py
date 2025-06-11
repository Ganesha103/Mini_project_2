
# test_login.py


"""
Create test using Pytest and Page Object Model


Focuses purely on Test Logic leveraging the Structured Page Objects


Commands :


pytest -v test_login.py
"""
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time
from selenium.webdriver.support.wait import WebDriverWait
from PageObjects.login_page import LoginPage, AdminPage, load_cookies
from common import Config
from conftest import driver
from test_data import test_users


# Test case 1
@pytest.mark.parametrize("username, password, expected_result", test_users)
def test_data_driven_login_verification(driver, username, password, expected_result):
    driver.get(Config.BASE_URL)

    login_page = LoginPage(driver)
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    login_successful = (Config.BASE_URL == driver.current_url)
    WebDriverWait(driver, 20).until(EC.url_to_be(Config.BASE_URL))
    assert login_successful == expected_result, f"Login result mismatched for {username}"

    print(f"SUCCESS: Login verification result for '{username}' matches expected outcome.")

    # Logout only if login was successful
    if login_successful:
        login_page.try_logout()

def test_cookie_based_login_verification(driver):
    driver.get(Config.BASE_URL)

    # Load stored cookies
    load_cookies(driver)

    # Verify login via cookies
    assert Config.BASE_URL == driver.current_url, "Login failed via cookies!"

    print("SUCCESS: Login verified via stored cookies.")

# Test case 2
def test_verify_home_url(driver):
   driver.get(Config().BASE_URL)

   # Check if the home URL is accessible
   assert driver.current_url == Config().BASE_URL, f"Home URL is NOT working: {driver.current_url}"

   print("SUCCESS: Home URL is working as expected.")

# test case 3
def test_valid_login(driver):
   driver.get(Config().BASE_URL)
   login_page = LoginPage(driver)

   login_page.enter_username(Config().USERNAME)
   login_page.enter_password(Config().PASSWORD)
   login_page.click_login()
   time.sleep(40)

   # Assert some Post-Login Behavior
   assert Config().DASHBOARD_URL == driver.current_url
   print(f"SUCCESS : Login Success with {Config().USERNAME} and {Config().PASSWORD}")

# Test case 4
def test_verify_login_fields_visibility(driver):
   driver.get(Config.BASE_URL)

   login_page = LoginPage(driver)

   assert login_page.is_username_visible(), "Username input box is NOT visible!"
   assert login_page.is_password_visible(), "Password input box is NOT visible!"

   print("SUCCESS: Username & Password input boxes are visible.")

# Test case 5
def test_verify_menus_after_login(driver):
   driver.get(Config.BASE_URL)

   login_page = LoginPage(driver)

   login_page.enter_username(Config.USERNAME)
   login_page.enter_password(Config.PASSWORD)
   login_page.click_login()

   # Verify menus
   menus = ["Admin", "PIM", "Leave", "Time", "Recruitment", "My Info", "Performance", "Dashboard"]

   for menu in menus:
      assert login_page.is_menu_visible(menu), f"{menu} menu is NOT visible!"
      assert login_page.is_menu_clickable(menu), f"{menu} menu is NOT clickable!"

   print("SUCCESS: All menus are visible and clickable after login.")


# Test case 6
def test_create_new_user_and_verify_login(driver):
    driver.get(Config.BASE_URL)

    # Login as Admin
    login_page = LoginPage(driver)
    login_page.enter_username(Config.ADMIN_USERNAME)
    login_page.enter_password(Config.ADMIN_PASSWORD)
    login_page.click_login()

    # Navigate to Admin Menu and Create a New User
    admin_page = AdminPage(driver)
    new_employee_name = "Test Employee_143"
    new_username = "TestUser123"
    new_password = "TestPass@123"

    admin_page.navigate_to_admin_menu()
    admin_page.click_add_user()
    admin_page.enter_user_details(new_employee_name, new_username, new_password)
    admin_page.save_user()

    # Log out from Admin account
    admin_page.logout()

    # Login with the newly created user
    login_page.enter_username(new_username)
    login_page.enter_password(new_password)
    login_page.click_login()

    # Verify successful login
    assert Config.BASE_URL == driver.current_url, f"New user login failed: {driver.current_url}"

    print(f"SUCCESS: New user '{new_username}' successfully logged into the CRM.")


# Test case 7
def test_verify_new_user_in_records(driver):
    driver.get(Config.BASE_URL)

    # Login as Admin
    login_page = LoginPage(driver)
    login_page.enter_username(Config.ADMIN_USERNAME)
    login_page.enter_password(Config.ADMIN_PASSWORD)
    login_page.click_login()

    # Navigate to Admin Menu
    admin_page = AdminPage(driver)
    admin_page.navigate_to_admin_menu()

    # Search for the newly created user
    new_username = "TestUser123"
    admin_page.search_user(new_username)

    # Verify if the user exists in records
    assert admin_page.is_user_present(new_username), f"User '{new_username}' not found in records!"

    print(f"SUCCESS: User '{new_username}' is present in the Admin records.")