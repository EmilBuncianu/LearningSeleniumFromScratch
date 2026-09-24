from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

def test_product_sorting_by_price(driver):
    """Test case to verify that products are sorted correctly by price from Low to High."""
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
