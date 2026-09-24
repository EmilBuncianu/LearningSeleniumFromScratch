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


# ==========================================
# SINGLE UNIFIED HOOK FOR SCREENSHOTS & HTML REPORTING
# ==========================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Unified hook to capture screenshots on failure and embed them into the HTML report."""
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    # We only trigger the capture during the setup or execution (call) phases upon failure
    if report.when in ("setup", "call") and report.failed:
        # Dynamically fetch the active driver instance from the current test context
        driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")

        if driver:
            # Step 1: Securely establish the target storage directory
            os.makedirs("raport", exist_ok=True)

            # Step 2: Generate a strictly unique filename preventing collision during parallel runs
            clean_test_name = item.nodeid.replace("::", "_").replace("/", "_").replace(".py", "").replace("tests_", "")
            timestamp = datetime.now().strftime("%H-%M-%S-%f")[:-3]  # Includes milliseconds

            screenshot_filename = f"fail_{clean_test_name}_{timestamp}.png"
            screenshot_path = os.path.join("raport", screenshot_filename)

            try:
                # Step 3: Capture and save the screenshot
                driver.get_screenshot_as_file(screenshot_path)
                print(f"\n[FAILURE ALERT] Captured system screen saved securely to: {screenshot_path}")

                # Step 4: Inject the image component cleanly into the pytest-html report DOM
                # Using a relative path context 'screenshot_filename' ensures image visibility post-upload
                html = f'<div><img src="{screenshot_filename}" alt="screenshot" style="width:304px;height:228px;" ' \
                       f'onclick="window.open({{this.src}})" align="right"/></div>'
                extra.append(pytest_html.extras.html(html))
                report.extra = extra
            except Exception as screenshot_error:
                print(f"\n[ERROR] Failed to save screenshot safely during parallel processing: {str(screenshot_error)}")


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
