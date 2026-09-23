import os
from datetime import datetime
import pytest
from selenium import webdriver
import pytest_html
import requests

@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.ChromeOptions()

    # 1. FORȚARE MOD INCOGNITO (Izolează complet sesiunile de testare)
    options.add_argument("--incognito")
    options.add_argument("--headless=new")  # Dezactivează interfața grafică complet
    options.add_argument("--disable-gpu")  # Optimizează consumul de resurse pe Windows
    options.add_argument("--window-size=1920,1080")  # Definește o rezoluție fixă în memorie pentru acuratețea elementelor

    # 2. DEZACTIVARE DETECȚIE SCURGERI DE DATE LA NIVEL DE MOTOR CHROME
    options.add_argument("--disable-features=PasswordLeakDetection,PasswordManager")

    # 3. Dezactivare pop-up salvări parole locale
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    })

    # 4. Anti-bot detection switches
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    # Mask driver execution flags
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    if request.node:
        request.node.funcargs['driver'] = driver

    yield driver

    driver.quit()


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
