from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_end_to_end_purchase(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # 1. Authentication flow
    login_page.navigate_to_login()
    login_page.login("standard_user", "secret_sauce")

    # 2. Add product to cart and navigate to checkout area
    inventory_page.add_backpack_to_cart()
    inventory_page.go_to_cart()

    # 3. Checkout information steps
    inventory_page.proceed_to_checkout()
    inventory_page.fill_checkout_information("Alex", "Popescu", "12345")

    # 4. Finalize order process
    inventory_page.finish_order()

    # 5. Verify successful checkout message
    success_message = inventory_page.get_success_message()
    assert "Thank you for your order!" in success_message


def test_product_sorting_by_price(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # 1. Authentication flow
    login_page.navigate_to_login()
    login_page.login("standard_user", "secret_sauce")

    # 2. Sort products by price: Low to High ('lohi' maps to the HTML value attribute)
    inventory_page.sort_products_by_value("lohi")

    # 3. Extract the list of product prices from the DOM
    actual_prices = inventory_page.get_all_product_prices()
    print(f"\n[DEBUG] App prices extracted after sorting sequence: {actual_prices}")

    # 4. Generate a mathematically sorted array in Python for absolute baseline comparison
    expected_prices = sorted(actual_prices)

    # 5. Assert whether the UI rendering matches the expected numerical sort order
    assert actual_prices == expected_prices, f"Product sorting failed! Expected order: {expected_prices}, but received: {actual_prices}"
