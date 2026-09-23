from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

def test_product_sorting_by_price(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # 1. Autentificare
    login_page.navigate_to_login()
    login_page.login("standard_user", "secret_sauce")

    # 2. Sortăm produsele după preț: Low to High ('lohi' este valoarea din HTML)
    inventory_page.sort_products_by_value("lohi")

    # 3. Extragem lista de prețuri de pe site
    actual_prices = inventory_page.get_all_product_prices()
    print(f"\n[DEBUG] Prețurile de pe site după sortare: {actual_prices}")

    # 4. Creăm o listă sortată matematic în Python pentru comparație
    expected_prices = sorted(actual_prices)

    # 5. Verificăm dacă ordinea de pe site coincide cu cea sortată corect
    assert actual_prices == expected_prices, f"Sortarea a eșuat! Așteptat: {expected_prices}, Dar a rezultat: {actual_prices}"
