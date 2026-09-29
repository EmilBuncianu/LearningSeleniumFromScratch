import os
from pytest_bdd import given, parsers, scenarios, then, when
from pages.login_page import LoginPage
from utils.data_loader import load_test_data

# FIXED: Calculăm calea absolută mergând 2 directoare în sus până în rădăcina proiectului
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
feature_path = os.path.join(project_root, "features", "login.feature")

# Legăm fișierul de feature folosind calea absolută sigură
scenarios(feature_path)

# Load your thread-safe JSON test data
test_data = load_test_data()


@given("I navigate to the login page")
def navigate_to_login(driver):
    """Triggers the login page initialization."""
    login_page = LoginPage(driver)
    login_page.navigate_to_login()


@when("I enter a valid username and password")
def enter_credentials(driver):
    """Fetches credentials from JSON and submits the login form."""
    login_page = LoginPage(driver)
    valid_credentials = test_data["valid_user"]
    login_page.login(valid_credentials["username"], valid_credentials["password"])


@then("I should be redirected to the inventory page")
def verify_redirection(driver):
    """Asserts that the browser URL correctly routes to the inventory page."""
    assert "/inventory.html" in driver.current_url


@when(parsers.re(r"I enter an invalid username (?P<username>.*) and password (?P<password>.*)"))
def enter_invalid_credentials(driver, username, password):
    """Submits the login form handling empty strings or regular text variations seamlessly."""
    login_page = LoginPage(driver)

    # Curățăm ghilimelele dacă datele vin sub formă de string gol în BDD Matrix
    user = "" if username == '""' or username is None else username
    pwd = "" if password == '""' or password is None else password

    login_page.login(user, pwd)


@then(parsers.re(r"I should see the login error message (?P<expected_error>.*)"))
def verify_error_message(driver, expected_error):
    """Extracts the DOM alert text and asserts it matches the expected validation rules."""
    login_page = LoginPage(driver)
    alert_text = login_page.get_alert_text()
    assert expected_error == alert_text
