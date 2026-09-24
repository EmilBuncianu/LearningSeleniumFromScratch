from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class InventoryPage(BasePage):
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    # Universal selectors using simple IDs
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")

    FINISH_BUTTON = (By.ID, "finish")
    SUCCESS_HEADER = (By.CLASS_NAME, "complete-header")

    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")

    def __init__(self, driver):
        super().__init__(driver)

    def add_backpack_to_cart(self):
        self.click_element(self.ADD_TO_CART_BUTTON)

    def go_to_cart(self):
        self.click_element(self.CART_ICON)

    def proceed_to_checkout(self):
        # Give the page a brief moment to load the scripts behind the button
        # NOTE: Since you implemented safe wrappers, you can safely experiment with removing these hardcoded delays later!
        import time
        time.sleep(1)
        self.click_element(self.CHECKOUT_BUTTON)
        # Ensure the page transition has completed successfully
        time.sleep(1)

    def fill_checkout_information(self, first_name, last_name, postal_code):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        self.click_element(self.CONTINUE_BUTTON)

    def finish_order(self):
        import time
        time.sleep(0.5)
        self.click_element(self.FINISH_BUTTON)

    def get_success_message(self):
        return self.get_element_text(self.SUCCESS_HEADER)

    def sort_products_by_value(self, value_text):
        dropdown_element = self.find_element(self.SORT_DROPDOWN)
        select = Select(dropdown_element)
        select.select_by_value(value_text)

    def get_all_product_prices(self):
        # Wait dynamically for all price tags to be visible on the DOM
        price_elements = self.wait.until(EC.visibility_of_all_elements_located(self.PRODUCT_PRICES))
        prices = []
        for element in price_elements:
            text_price = element.text.strip()
            if text_price: # Ne asigurăm că elementul are text complet randat
                clean_price = float(text_price.replace("$", ""))
                prices.append(clean_price)
        return prices

