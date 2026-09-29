import os
from datetime import datetime
import pytest
import pytest_html
from selenium import webdriver


def pytest_addoption(parser):
    """Înregistrează opțiunea --browser în linia de comandă PyTest."""
    parser.addoption(
        "--browser", action="store", default="chrome",
        help="Choose target browser for execution: chrome, firefox or edge",
    )


@pytest.fixture(scope="function")
def driver(request):
    """Fixture izolat care instanțiază și curăță WebDriver-ul pentru fiecare test."""
    browser_name = request.config.getoption("browser").lower()

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Esențial pentru rulare stabilă în CI/CD
        options.add_argument("--incognito")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver_instance = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        driver_instance = webdriver.Firefox(options=options)

    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        driver_instance = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Browser-ul '{browser_name}' nu este suportat! Alege dintre: chrome, firefox, edge.")

    driver_instance.maximize_window()

    yield driver_instance

    driver_instance.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook Enterprise care salvează screenshot-uri la erori și le injectează în pytest-html."""
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when in ("setup", "call") and report.failed:
        driver_instance = item.funcargs.get("driver")

        if driver_instance:
            os.makedirs("raport", exist_ok=True)

            clean_test_name = (
                item.nodeid.replace("::", "_")
                .replace("/", "_")
                .replace(".py", "")
                .replace("tests_", "")
            )
            timestamp = datetime.now().strftime("%H-%M-%S-%f")[:-3]
            screenshot_filename = f"fail_{clean_test_name}_{timestamp}.png"
            screenshot_path = os.path.join("raport", screenshot_filename)

            try:
                driver_instance.get_screenshot_as_file(screenshot_path)

                # Generăm tag-ul HTML pentru atașare în raportul HTML local
                html = (
                    f'<div><img src="{screenshot_filename}" alt="screenshot" style="width:304px;height:228px;" '
                    f'onclick="window.open({{this.src}})" align="right"/></div>'
                )
                extra.append(pytest_html.extras.html(html))
                report.extra = extra
            except Exception as e:
                print(f"\n[ERROR] Nu s-a putut genera screenshot-ul: {str(e)}")
