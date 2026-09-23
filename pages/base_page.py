import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://saucedemo.com"

    def open_url(self, path=""):
        logger.info(f"Navighez către URL-ul: {self.base_url}")
        self.driver.get(f"{self.base_url}{path}")

    def find_element(self, locator, time=15):
        # CHANGED: Waiting for visibility ensures the element is rendered and interactive
        element = WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located(locator)
        )
        # BACKUP: Smoothly scroll the element into view to force focus
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element

    def click_element(self, locator, time=15):
        logger.info(f"Execut Click pe elementul cu locatorul: {locator}")
        element = WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

    def type_text(self, locator, text, time=15):
        element = self.find_element(locator, time)
        element.clear()
        element.send_keys(text)
        log_text = "********" if "password" in str(locator).lower() else text
        logger.info(f"Introduc textul '{log_text}' în elementul: {locator}")

    def get_element_text(self, locator, time=15):

        element = self.find_element(locator, time)
        text = element.text
        logger.info(f"Am extras textul '{text}' din elementul: {locator}")
        return element.text
