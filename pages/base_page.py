import logging
import os
import json
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver, base_url=None):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

        # FIXED: Preluăm dinamic URL-ul din JSON dacă nu este specificat direct
        if base_url:
            self.base_url = base_url
        else:
            try:
                # Căutăm fișierul de configurare aflat în rădăcina proiectului
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                json_path = os.path.join(base_dir, "data", "test_env.json")
                with open(json_path, "r") as file:
                    config = json.load(file)
                    self.base_url = config.get("base_url", "https://saucedemo.com")
            except Exception:
                self.base_url = "https://saucedemo.com"

    def open_url(self, path=""):
        logger.info(f"Navigating to URL: {self.base_url}{path}")
        self.driver.get(f"{self.base_url}{path}")

    def find_element(self, locator):
        """Waits for the element to be present and visible on the page before returning it."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"❌ Error: Element with locator {locator} did not become visible within 10 seconds.")
            raise

    def click_element(self, locator):
        """Waits for the element to be clickable, scrolls to it, and clicks it."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
        except Exception as e:
            print(f"❌ Error clicking on {locator}: {str(e)}")
            raise

    def type_text(self, locator, text, clear_first=True):
        """Waits for the element, clears the field (optional), and safely enters the text."""
        try:
            element = self.find_element(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
        except Exception as e:
            print(f"❌ Error writing text into {locator}: {str(e)}")
            raise

    def get_element_text(self, locator):
        """Extracts text from element dynamically."""
        element = self.find_element(locator)
        text = element.text.strip()
        logger.info(f"Extracted text '{text}' from element: {locator}")
        return text  # FIXED: Returnează corect textul extras
