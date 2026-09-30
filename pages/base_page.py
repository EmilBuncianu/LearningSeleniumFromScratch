import logging
import os
import json
import time
from PIL import Image, ImageChops
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
        for attempt in range(retries):
            try:
                return self.wait.until(EC.visibility_of_element_located(locator))
            except StaleElementReferenceException:
                if attempt == retries - 1:
                    raise
                logger.warning(f"🔄 [STALE] Retrying element {locator} ({attempt + 1}/{retries})")
                time.sleep(0.5)
            except TimeoutException:
                logger.error(f"❌ [TIMEOUT] Element {locator} not visible.")
                raise

    def click_element(self, locator, retries=3):
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                # FIXED: Corectat sintaxa din arguments in arguments[0] pentru scrollIntoView
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                element.click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException) as e:
                if attempt == retries - 1:
                    try:
                        element = self.wait.until(EC.presence_of_element_located(locator))
                        # FIXED: Corectat si fallback-ul de JS click cu arguments[0]
                        self.driver.execute_script("arguments[0].click();", element)
                        return
                    except Exception:
                        raise e
                time.sleep(0.8)

    def type_text(self, locator, text, clear_first=True, retries=3):
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
                time.sleep(0.5)

    def get_element_text(self, locator):
        element = self.find_element(locator)
        text = element.text.strip()
        logger.info(f"Extracted text '{text}' from element: {locator}")
        return text

    def assert_visual_baseline(self, baseline_name, threshold_percent=1.0):
        baselines_dir = os.path.join("tests", "visual_baselines")
        diffs_dir = os.path.join("raport", "visual_diffs")
        os.makedirs(baselines_dir, exist_ok=True)
        os.makedirs(diffs_dir, exist_ok=True)

        baseline_path = os.path.join(baselines_dir, f"{baseline_name}.png")
        current_screenshot_path = os.path.join(diffs_dir, f"current_{baseline_name}.png")
        diff_path = os.path.join(diffs_dir, f"diff_{baseline_name}.png")

        self.driver.save_screenshot(current_screenshot_path)

        if not os.path.exists(baseline_path):
            self.driver.save_screenshot(baseline_path)
            logger.info(f"📸 [VISUAL] Baseline '{baseline_name}' created as reference.")
            return True

        img_baseline = Image.open(baseline_path).convert("RGB")
        img_current = Image.open(current_screenshot_path).convert("RGB")

        if img_baseline.size != img_current.size:
            img_current = img_current.resize(img_baseline.size)

        diff = ImageChops.difference(img_baseline, img_current)
        bbox = diff.getbbox()

        if bbox is None:
            logger.info(f"✅ [VISUAL PASS] Perfect match for '{baseline_name}'.")
            if os.path.exists(current_screenshot_path):
                os.remove(current_screenshot_path)
            return True
        else:
            diff.save(diff_path)

            # FIXED: Utilizăm funcții moderne pentru a evita DeprecationWarning în Pillow
            pixels_changed = sum(1 for p in diff.getdata() if sum(p) > 0)

            # FIXED: Calculăm corect suprafața totală înmulțind lățimea (index 0) cu înălțimea (index 1)
            width, height = img_baseline.size
            total_pixels = width * height

            mismatch_percentage = (pixels_changed / total_pixels) * 100

            logger.warning(f"📊 [VISUAL SCORE] Mismatch for '{baseline_name}': {mismatch_percentage:.2f}%")

            if mismatch_percentage > threshold_percent:
                msg = f"❌ [VISUAL FAILED] Layout mismatch for '{baseline_name}'! Diff: {mismatch_percentage:.2f}%"
                logger.error(msg)
                raise AssertionError(msg)

            logger.info(f"✅ [VISUAL PASS] Diff ({mismatch_percentage:.2f}%) is within tolerance.")
            return True

