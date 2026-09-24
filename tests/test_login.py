import pytest
from pages.login_page import LoginPage

def test_successful_login(driver):
    """Test case to verify successful authentication with valid credentials."""
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.login("standard_user", "secret_sauce")
    assert "/inventory.html" in driver.current_url

@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("invalid_user", "invalid_password", "Epic sadface: Username and password do not match any user in this service"),
        ("standard_user", "invalid_password", "Epic sadface: Username and password do not match any user in this service"),
        ("", "", "Epic sadface: Username is required"),
        ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out.")
    ]
)
def test_invalid_login(driver, username, password, expected_error):
    """Data-driven test matrix covering various negative authentication scenarios."""
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.login(username, password)
    alert_text = login_page.get_alert_text()
    assert expected_error == alert_text
