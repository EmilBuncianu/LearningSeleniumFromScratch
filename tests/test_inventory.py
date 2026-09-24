from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import load_test_data

# Load the externalized JSON test data dynamically
test_data = load_test_data()

def test_end_to_end_purchase(driver):
    """Test case to verify a complete user purchase flow using external test data."""
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # 1. Fetch valid credentials and checkout details from JSON mapping
    valid_credentials = test_data["valid_user"]
    checkout_info = test_data["checkout_data"]

    # 2. Authentication flow
    login_page.navigate_to_login()
    login_page.login(valid_credentials["username"], valid_credentials["password"])

    # 3. Add product to cart and navigate to checkout area
    inventory_page.add_backpack_to_cart()
    inventory_page.go_to_cart()

    # 4. Checkout information steps populated from external JSON dataset
    inventory_page.proceed_to_checkout()
    inventory_page.fill_checkout_information(
        checkout_info["first_name"],
        checkout_info["last_name"],
        checkout_info["postal_code"]
    )

    # 5. Finalize order process
    inventory_page.finish_order()

    # 6. Verify successful checkout message
    success_message = inventory_page.get_success_message()
    assert "Thank you for your order!" in success_message
