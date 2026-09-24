import os
from datetime import datetime
import pytest
from selenium import webdriver
import pytest_html
import requests

# Step 1: Register the custom --browser command-line option for PyTest execution
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Choose target browser for execution: chrome, firefox or edge"
    )


@pytest.fixture(scope="function")
def driver(request):
    # Retrieve the specified browser name parameter from the execution command line
    browser_name = request.config.getoption("browser").lower()

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Modern Chromium headless execution switch
        options.add_argument("--incognito")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver_instance = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")  # Forces standard headless mode, ideal for CI environments
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        driver_instance = webdriver.Firefox(options=options)

    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--headless")  # Standard universal headless switch for Edge on Linux architectures
        options.add_argument("--no-sandbox")  # Mandatory flag for container execution permissions in GitHub Actions
        options.add_argument("--disable-dev-shm-usage")  # Prevents browser crashes resulting from shared cache memory exhaustion
        options.add_argument("--disable-gpu")  # Disables hardware rendering (essential on headless Linux servers)

        driver_instance = webdriver.Edge(options=options)
    else:
        raise ValueError(f"The browser choice '{browser_name}' is not supported! Please choose between: chrome, firefox, edge.")

    driver_instance.maximize_window()

    yield driver_instance

    driver_instance.quit()


# PyTest Hook for capturing failure screenshots locally
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            test_name = item.name
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            print(f"\n[FAILURE ALERT] Captured system screen saved to: {screenshot_path}")


# PyTest Hook variant for injecting the failure screenshots inside the interactive HTML report dashboards
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            test_name = item.name
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
            driver.save_screenshot(screenshot_path)

            # FIXED: Double curly braces {{this.src}} to protect the JavaScript code block from Python interpreter errors
            html = f'<div><img src="{screenshot_path}" alt="screenshot" style="width:304px;height:228px;" ' \
                   f'onclick="window.open({{this.src}})" align="right"/></div>'
            extra.append(pytest_html.extras.html(html))
            report.extra = extra


@pytest.fixture(scope="function")
def auth_headers():
    """
    Global lifecycle fixture executing a backend authentication request, extracting
    the returned dynamic security Token, and yielding a pre-configured Authorization header.
    """
    # FIXED: Added the required /api routing suffix to the endpoint context path
    base_url = "https://reqres.in/api"

    login_payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslickica"
    }

    response = requests.post(f"{base_url}/login", json=login_payload)
    assert response.status_code == 200, "Initial backend API authentication routine failed!"

    token = response.json().get("token")
    print(f"\n[API SECURITY] Successfully extracted Authorization token globally from conftest: {token}")

    headers = {
        # Configured for strict compliance with the mock ReqRes authentication gateway
        "Authorization": token,
        "Content-Type": "application/json"
    }
    return headers
