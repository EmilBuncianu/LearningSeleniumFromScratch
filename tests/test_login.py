import pytest
from pages.login_page import LoginPage
# Importăm direct funcția izolată
from utils.data_loader import load_test_data

# Încărcăm datele în siguranță înainte de faza de test discovery
test_data = load_test_data()


def test_successful_login(driver):
    """Test case to verify successful authentication with valid credentials."""
    login_page = LoginPage(driver)
    valid_credentials = test_data["valid_user"]

    login_page.navigate_to_login()
    login_page.login(valid_credentials["username"], valid_credentials["password"])
    assert "/inventory.html" in driver.current_url


def get_invalid_login_scenarios():
    return [
        (scenario["username"], scenario["password"], scenario["expected_error"])
        for scenario in test_data["invalid_login_matrix"]
    ]


@pytest.mark.parametrize(
    "username, password, expected_error",
    get_invalid_login_scenarios()
)
def test_invalid_login(driver, username, password, expected_error):
    """Data-driven test matrix covering negative authentication scenarios."""
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.login(username, password)
    alert_text = login_page.get_alert_text()
    assert expected_error == alert_text
