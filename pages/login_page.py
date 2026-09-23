from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locatori stabili pentru SauceDemo
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    # Mesajul de eroare apare într-un container h3 pe acest site
    ALERT_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)
        # SauceDemo are formularul direct pe pagina principală, deci calea e goală
        self.path = "/"

    def navigate_to_login(self):
        self.open_url(self.path)

    def login(self, username, password):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    def get_alert_text(self):
        return self.get_element_text(self.ALERT_MESSAGE)
