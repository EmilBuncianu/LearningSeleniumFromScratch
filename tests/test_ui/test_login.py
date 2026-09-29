# Exemplu de integrare cu base_url din test_env.json în tests/test_ui/test_login.py
import pytest
from pages.login_page import LoginPage
from utils.data_loader import load_test_data

test_data = load_test_data()

def test_successful_login(driver, base_url): # Adăugat base_url ca argument
    """Test case to verify successful authentication with valid credentials."""
    login_page = LoginPage(driver)
    valid_credentials = test_data["valid_user"]

    # Dacă clasa LoginPage suportă primirea unui URL direct:
    driver.get(base_url)
    login_page.login(valid_credentials["username"], valid_credentials["password"])
    assert "/inventory.html" in driver.current_url
