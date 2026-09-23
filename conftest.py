import os
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
import pytest_html
import requests

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService


# Pasul 1: Îi spunem lui PyTest să accepte parametrul --browser în linia de comandă
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Alege browserul pentru rulare: chrome, firefox sau edge"
    )


@pytest.fixture(scope="function")
def driver(request):
    # Citim browserul ales din linia de comandă
    browser_name = request.config.getoption("browser").lower()

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Modul headless modern
        options.add_argument("--incognito")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver_instance = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless=new")   # Modul headless stabil
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")

        options.add_argument("--no-sandbox")                # Ignoră restricțiile de sandbox din container
        options.add_argument("--disable-dev-shm-usage")      # Previne prăbușirea din lipsă de memorie cache (/dev/shm)
        options.add_argument("--disable-gpu")                # Dezactivează randarea grafică (esențial pe Linux Server)

        driver_instance = webdriver.Firefox(options=options)

    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--headless")  # Modul headless universal standard pentru Edge pe Linux
        options.add_argument("--no-sandbox")  # Obligatoriu pentru privilegii în GitHub Actions
        options.add_argument("--disable-dev-shm-usage")  # Previne crash-urile de memorie cache
        options.add_argument("--disable-gpu")  # Dezactivează accelerarea hardware (important în containere fără placă video)

        driver_instance = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Browser-ul '{browser_name}' nu este suportat! Alege dintre: chrome, firefox, edge.")

    driver_instance.maximize_window()

    yield driver_instance

    driver_instance.quit()


# PyTest Hook pentru screenshot-uri la eșec
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


# Adaugă acest cod la finalul fișierului conftest.py, sub celălalt hook existent

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

            # Codul nou care inserează imaginea în raportul HTML:
            html = f'<div><img src="{screenshot_path}" alt="screenshot" style="width:304px;height:228px;" ' \
                   f'onclick="window.open(this.src)" align="right"/></div>'
            extra.append(pytest_html.extras.html(html))
            report.extra = extra


@pytest.fixture(scope="function")
def auth_headers():
    """
    Fixture global care efectuează logarea în backend, extrage Token-ul primit
    și returnează dicționarul de Headers gata configurat pentru securitate.
    """
    # CORECTAT: Adăugat /api la finalul URL-ului
    base_url = "https://reqres.in/api"

    login_payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslickica"
    }

    response = requests.post(f"{base_url}/login", json=login_payload)
    assert response.status_code == 200, "Autentificarea inițială a eșuat!"

    token = response.json().get("token")
    print(f"\n[API SECURITY] Token extras global din conftest: {token}")

    headers = {
        # Modificat pentru compatibilitatea cu simulatorul ReqRes
        "Authorization": token,
        "Content-Type": "application/json"
    }
    return headers
