from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Stable locators for SauceDemo
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    # The error alert message appears inside an h3 container on this platform
    ALERT_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)
        # SauceDemo renders the authentication form directly on the root URL path
        self.path = "/"

    def navigate_to_login(self):
        self.open_url(self.path)

    def login(self, username, password):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    def get_alert_text(self):
        return self.get_element_text(self.ALERT_MESSAGE)
