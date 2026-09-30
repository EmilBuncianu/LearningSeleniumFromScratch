import pytest
from pages.login_page import LoginPage


def test_login_page_visual_layout(driver):
    """Verifică automat dacă designul paginii de login nu s-a decalat (CSS/Imagini)."""
    login_page = LoginPage(driver)

    # Navigăm pe pagină
    login_page.navigate_to_login()

    # FIXED: Ne asigurăm că apelăm metoda moștenită nativ din clasa părinte BasePage
    login_page.assert_visual_baseline("login_page_layout", threshold_percent=9)
