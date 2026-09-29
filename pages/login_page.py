import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

# Inițializăm logger-ul pentru acest fișier
logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "h3[data-test='error']")

    def navigate_to_login(self):
        logger.info("Deschidem pagina principală de autentificare...")
        self.open_url("/")

    def login(self, username, password):
        logger.info(f"Încercăm autentificarea pentru utilizatorul: '{username}'")

        if not username:
            logger.warning("Câmpul 'username' trimis este gol!")

        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)

        logger.info("Se execută click pe butonul de Login.")
        self.click_element(self.LOGIN_BUTTON)

    def get_alert_text(self):
        logger.info("Preluăm mesajul de eroare afișat pe interfață.")
        error_text = self.get_element_text(self.ERROR_CONTAINER)
        logger.error(f"Eroare detectată pe UI: '{error_text}'")
        return error_text
