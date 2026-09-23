from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_end_to_end_purchase(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    # 1. Logare
    login_page.navigate_to_login()
    login_page.login("standard_user", "secret_sauce")

    # 2. Adăugare produs în coș și navigare către coș
    inventory_page.add_backpack_to_cart()
    inventory_page.go_to_cart()

    # 3. Checkout
    inventory_page.proceed_to_checkout()
    inventory_page.fill_checkout_information("Alex", "Popescu", "12345")

    # 4. Finalizare comandă
    inventory_page.finish_order()

    # 5. Verificare succes
    success_message = inventory_page.get_success_message()
    assert "Thank you for your order!" in success_message

    # Adaugă acest test la finalul fișierului tests/test_login.py

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


# Adaugă acest test la finalul fișierului tests/test_login.py
