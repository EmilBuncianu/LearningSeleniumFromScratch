from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage
from utils.data_loader import load_test_data

# Link this file to the Gherkin feature file
scenarios('../features/login.feature')

# Load your thread-safe JSON test data
test_data = load_test_data()

@given('I navigate to the login page')
def navigate_to_login(driver):
    """Triggers the login page initialization."""
    login_page = LoginPage(driver)
    login_page.navigate_to_login()

@when('I enter a valid username and password')
def enter_credentials(driver):
    """Fetches credentials from JSON and submits the login form."""
    login_page = LoginPage(driver)
    valid_credentials = test_data["valid_user"]
    login_page.login(valid_credentials["username"], valid_credentials["password"])

@then('I should be redirected to the inventory page')
def verify_redirection(driver):
    """Asserts that the browser URL correctly routes to the inventory page."""
    assert "/inventory.html" in driver.current_url



from pytest_bdd import when, then, parsers

# We reuse the existing @given('I navigate to the login page') defined at the top of your file

# 🚀 REPARAT CU REGEX: (.*) acceptă nativ caractere alfanumerice, speciale sau text complet gol
@when(parsers.re(r'I enter an invalid username (?P<username>.*) and password (?P<password>.*)'))
def enter_invalid_credentials(driver, username, password):
    """Submits the login form handling empty strings or regular text variations seamlessly via regex mapping."""
    login_page = LoginPage(driver)
    login_page.login(username, password)


# 🚀 REPARAT CU REGEX: Potrivește textul de eroare indiferent de lungime
@then(parsers.re(r'I should see the login error message (?P<expected_error>.*)'))
def verify_error_message(driver, expected_error):
    """Extracts the DOM alert text and asserts it matches the expected validation rules via regex parsing."""
    login_page = LoginPage(driver)
    alert_text = login_page.get_alert_text()
    assert expected_error == alert_text


