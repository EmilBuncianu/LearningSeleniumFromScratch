import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://saucedemo.com"
        self.wait = WebDriverWait(self.driver, 10)

    def open_url(self, path=""):
        logger.info(f"Navighez către URL-ul: {self.base_url}")
        self.driver.get(f"{self.base_url}{path}")

    def find_element(self, locator):
        """Așteaptă ca elementul să fie prezent și vizibil pe pagină înainte de a-l returna."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"❌ Eroare: Elementul cu locatorul {locator} nu a devenit vizibil în 10 secunde.")
            raise

    def click_element(self, locator):
        """Așteaptă ca elementul să fie clicabil, face scroll la el și dă click."""
        try:
            # Asigură-te că elementul poate primi click
            element = self.wait.until(EC.element_to_be_clickable(locator))
            # Optional: Scroll automat până la element dacă e o pagină lungă
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
        except Exception as e:
            print(f"❌ Eroare la click pe {locator}: {str(e)}")
            # Aici tool-ul tău poate face și o captură de ecran automată dacă vrei
            raise

    def type_text(self, locator, text, clear_first=True):
        """Așteaptă elementul, curăță câmpul (opțional) și introduce textul în siguranță."""
        try:
            element = self.find_element(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
        except Exception as e:
            print(f"❌ Eroare la scrierea textului în {locator}: {str(e)}")
            raise

    def get_element_text(self, locator, time=15):

        element = self.find_element(locator)
        text = element.text
        logger.info(f"Am extras textul '{text}' din elementul: {locator}")
        return element.text
