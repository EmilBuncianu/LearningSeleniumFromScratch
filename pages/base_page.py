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
        logger.info(f"Navigating to URL: {self.base_url}")
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
            # Ensure the element is clickable
            element = self.wait.until(EC.element_to_be_clickable(locator))
            # Optional: Automatically scroll to the element if it is a long page
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
        except Exception as e:
            print(f"❌ Error clicking on {locator}: {str(e)}")
            # Your tool can also take an automatic screenshot here if you want
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

    def get_element_text(self, locator, time=15):

        element = self.find_element(locator)
        text = element.text
        logger.info(f"Extracted text '{text}' from element: {locator}")
        return element.text
