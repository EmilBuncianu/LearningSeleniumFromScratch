import os
from pytest_bdd import scenarios, given, when, then
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.data_loader import load_test_data

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
feature_path = os.path.join(project_root, "features", "purchase.feature")

scenarios(feature_path)
test_data = load_test_data()

@given('I am a logged-in user on the inventory page')
def logged_in_user(driver):
    """Pre-requisite step: navigates to login and authenticates the session."""
    login_page = LoginPage(driver)
    valid_credentials = test_data["valid_user"]
    login_page.navigate_to_login()
    login_page.login(valid_credentials["username"], valid_credentials["password"])

@when('I add the backpack to the cart and proceed to checkout')
def add_product_and_checkout(driver):
    inventory_page = InventoryPage(driver)
    inventory_page.add_backpack_to_cart()
    inventory_page.go_to_cart()
    inventory_page.proceed_to_checkout()

@when('I fill in the checkout information')
def fill_shipping_details(driver):
    inventory_page = InventoryPage(driver)
    checkout_info = test_data["checkout_data"]
    inventory_page.fill_checkout_information(
        checkout_info["first_name"],
        checkout_info["last_name"],
        checkout_info["postal_code"]
    )
    inventory_page.finish_order()

@then('the order should be finalized with a success message')
def verify_order_completion(driver):
    inventory_page = InventoryPage(driver)
    success_message = inventory_page.get_success_message()
    assert "Thank you for your order!" in success_message
