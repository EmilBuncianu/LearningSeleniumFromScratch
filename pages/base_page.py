import logging
import os
import json
import time
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver, base_url=None):
        self.driver = driver
        # Timp standard de așteptare explicită (10 secunde)
        self.wait = WebDriverWait(self.driver, 10)

        if base_url:
            self.base_url = base_url
        else:
            try:
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

    def find_element(self, locator, retries=3):
        """
        Găsește un element pe pagină cu un mecanism de reîncercare integrat (Anti-Flakiness).
        Gestionează automat StaleElementReferenceException dacă DOM-ul se reîmprospătează dinamic.
        """
        for attempt in range(retries):
            try:
                return self.wait.until(EC.visibility_of_element_located(locator))
            except StaleElementReferenceException:
                if attempt == retries - 1:
                    raise
                logger.warning(
                    f"🔄 [STALE ELEMENT] Reîncercăm identificarea elementului {locator} (Tentativa {attempt + 1}/{retries})")
                time.sleep(0.5)
            except TimeoutException:
                logger.error(f"❌ [TIMEOUT] Elementul {locator} nu a devenit vizibil în 10 secunde.")
                raise

    def click_element(self, locator, retries=3):
        """
        Execută un click robust. Dacă elementul este blocat de o animație sau un banner de loading,
        așteaptă și încearcă din nou. Ca ultim fallback, folosește un click executat prin JavaScript.
        """
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                element.click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException) as e:
                if attempt == retries - 1:
                    logger.warning(
                        f"⚠️ [FALLBACK] Click-ul standard a eșuat după {retries} încercări. Forțăm click-ul prin JavaScript.")
                    try:
                        element = self.wait.until(EC.presence_of_element_located(locator))
                        self.driver.execute_script("arguments[0].click();", element)
                        return
                    except Exception as js_error:
                        logger.error(f"❌ [CRITICAL] Click-ul prin JavaScript a eșuat: {str(js_error)}")
                        raise e
                logger.warning(
                    f"🔄 [CLICK INTERCEPTED] Elementul {locator} este blocat momentan. Reîncercăm în 0.8s... ({attempt + 1}/{retries})")
                time.sleep(0.8)

    def type_text(self, locator, text, clear_first=True, retries=3):
        """Introduce text în siguranță, reîncercând acțiunea dacă elementul devine temporar indisponibil."""
        for attempt in range(retries):
            try:
                element = self.find_element(locator)
                if clear_first:
                    element.clear()
                element.send_keys(text)
                return
            except StaleElementReferenceException:
                if attempt == retries - 1:
                    raise
                logger.warning(f"🔄 [STALE ELEMENT] DOM-ul s-a schimbat la scriere în {locator}. Reîncercăm...")
                time.sleep(0.5)

    def get_element_text(self, locator):
        """Extrage textul dintr-un element în mod dinamic."""
        element = self.find_element(locator)
        text = element.text.strip()
        logger.info(f"Extracted text '{text}' from element: {locator}")
        return text
