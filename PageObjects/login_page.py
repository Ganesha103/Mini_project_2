# login_page.py


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common import Config
from PageObjects.base_page import BasePage


class Locators:
    USERNAME_INPUT_BOX = "username"
    PASSWORD_INPUT_BOX = "password"
    SUBMIT_BUTTON = "//button[@type='submit']"

    # Menu Locators
    ADMIN_MENU = "//a[@href='/web/index.php/admin/viewAdminModule']"
    PIM_MENU = "//a[@href='/web/index.php/pim/viewPimModule']"
    LEAVE_MENU = "//a[@href='/web/index.php/leave/viewLeaveModule']"
    TIME_MENU = "//a[@href='/web/index.php/time/viewTimeModule']"
    RECRUITMENT_MENU = "//a[@href='/web/index.php/recruitment/viewRecruitmentModule']"
    MY_INFO_MENU = "//a[@href='/web/index.php/pim/viewMyDetails']"
    PERFORMANCE_MENU = "//a[@href='/web/index.php/performance/viewPerformanceModule']"
    DASHBOARD_MENU = "//a[@href='/web/index.php/dashboard/index']"

    ADD_USER_BUTTON = "//*[@id='app']/div[1]/div[2]/div[2]/div/div[2]/div[1]/button"
    USER_ROLE_DROPDOWN = "//*[@id='app']/div[1]/div[1]/header/div[1]/div[3]/ul/li/span"
    EMPLOYEE_NAME_INPUT = "//input[@placeholder='Type for hints...']"
    USERNAME_INPUT = "//*[@id='app']/div[1]/div[2]/div[2]/div/div/form/div[1]/div/div[4]/div/div[2]/input"
    PASSWORD_INPUT = "//*[@id='app']/div[1]/div[2]/div[2]/div/div/form/div[2]/div/div[1]/div/div[2]/input"
    CONFIRM_PASSWORD_INPUT = "//*[@id='app']/div[1]/div[2]/div[2]/div/div/form/div[2]/div/div[2]/div/div[2]/input"
    SAVE_BUTTON = "//*[@id='app']/div[1]/div[2]/div[2]/div/div/form/div[3]/button[2]"
    LOGOUT_BUTTON = "//*[@id='app']/div[1]/div[1]/header/div[1]/div[3]/ul/li/ul/li[4]/a"
    SEARCH_USER_INPUT = "//*[@id='app']/div[1]/div[2]/div[2]/div/div[1]/div[2]/form/div[1]/div/div[1]/div/div[2]/input"
    SEARCH_BUTTON = "//*[@id='app']/div[1]/div[2]/div[2]/div/div[1]/div[2]/form/div[2]/button[2]"
    USER_RECORD = "//*[@id='app']/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/span"


class LoginPage(BasePage, Locators):
    USERNAME_INPUT = (By.NAME, Locators().USERNAME_INPUT_BOX)
    PASSWORD_INPUT = (By.NAME, Locators().PASSWORD_INPUT_BOX)
    LOGIN_BUTTON = (By.XPATH, Locators().SUBMIT_BUTTON)

    MENU_ITEMS = {
        "Admin": (By.XPATH, Locators.ADMIN_MENU),
        "PIM": (By.XPATH, Locators.PIM_MENU),
        "Leave": (By.XPATH, Locators.LEAVE_MENU),
        "Time": (By.XPATH, Locators.TIME_MENU),
        "Recruitment": (By.XPATH, Locators.RECRUITMENT_MENU),
        "My Info": (By.XPATH, Locators.MY_INFO_MENU),
        "Performance": (By.XPATH, Locators.PERFORMANCE_MENU),
        "Dashboard": (By.XPATH, Locators.DASHBOARD_MENU)
    }

    def enter_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def is_username_visible(self):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )

    def is_password_visible(self):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_INPUT)
        )

    def is_username_present(self):
        try:
            self.find_element(self.USERNAME_INPUT)
            return True
        except:
            return False

    def is_password_present(self):
        try:
            self.find_element(self.PASSWORD_INPUT)
            return True
        except:
            return False

    def verify_home_url(self):
        return self.driver.current_url == Config().BASE_URL

    def is_menu_visible(self, menu_name):
        locator = self.MENU_ITEMS.get(menu_name)
        try:
            self.find_element(locator)
            return True
        except:
            return False

    def is_menu_clickable(self, menu_name):
        locator = self.MENU_ITEMS.get(menu_name)
        try:
            self.is_enabled(locator)
            return True
        except:
            return False

    def logout(self):
        """Log out from the admin account"""
        logout_button_1 = WebDriverWait(self.driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, Locators.USER_ROLE_DROPDOWN)))
        logout_button_1.click()

        logout_button = WebDriverWait(self.driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, Locators.LOGOUT_BUTTON)))
        logout_button.click()

    def try_logout(self):
        """Safely attempt to log out"""
        try:
            self.logout()  # Calls the existing logout function
            print("SUCCESS: User logged out.")
        except Exception as e:
            print(f"WARNING: Logout attempt failed - {e}")



import json

def save_cookies(driver):
    """Save cookies after successful login"""
    cookies = driver.get_cookies()
    with open("cookies.json", "w") as file:
        json.dump(cookies, file)


def load_cookies(driver):
    """Load saved cookies into a new browser session"""
    try:
        with open("cookies.json", "r") as file:
            cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
    except FileNotFoundError:
        print("No saved cookies found. Login required.")


def load_cookies(driver):
    """Load saved cookies into a new browser session"""
    try:
        with open("cookies.json", "r") as file:
            cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
    except FileNotFoundError:
        print("No saved cookies found. Login required.")

def test_cookie_based_login_verification(driver):
    driver.get(Config.BASE_URL)

    # Load cookies
    load_cookies(driver)

    # Verify login via cookies
    assert Config.DASHBOARD_URL == driver.current_url, "Login failed via cookies!"

    print("SUCCESS: Login verified via stored cookies.")



class AdminPage(BasePage, Locators):

    def navigate_to_admin_menu(self):
        """Navigate to the Admin menu"""
        self.click((By.XPATH, Locators.ADMIN_MENU))

    def click_add_user(self):
        """Click on the 'Add User' button"""
        self.click((By.XPATH, Locators.ADD_USER_BUTTON))

    def enter_user_details(self, employee_name, username, password):
        """Enter user details in the form"""
        self.enter_text((By.XPATH, Locators.EMPLOYEE_NAME_INPUT), employee_name)
        self.enter_text((By.XPATH, Locators.USERNAME_INPUT), username)
        self.enter_text((By.XPATH, Locators.PASSWORD_INPUT), password)
        self.enter_text((By.XPATH, Locators.CONFIRM_PASSWORD_INPUT), password)

    def save_user(self):
        """Click the save button to submit the new user"""
        self.click((By.XPATH, Locators.SAVE_BUTTON))

    def logout(self):
        """Log out from the admin account"""
        logout_button_1 = WebDriverWait(self.driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, Locators.USER_ROLE_DROPDOWN)))
        logout_button_1.click()

        logout_button = WebDriverWait(self.driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, Locators.LOGOUT_BUTTON)))
        logout_button.click()

    def search_user(self, username):
        """Search for a user in the Admin menu"""
        self.enter_text((By.XPATH, Locators.SEARCH_USER_INPUT), username)
        self.click((By.XPATH, Locators.SEARCH_BUTTON))

    def is_user_present(self, username):
        """Verify if the user exists in the Admin records"""
        user_locator = (By.XPATH, Locators.USER_RECORD.format(username))
        try:
            user_element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(user_locator))
            return bool(user_element)
        except TimeoutException:
            return False



