# Custom Web Automation Framework (Python + Selenium + PyTest)

This project represents a robust, highly scalable, and production-ready web automation framework built completely from scratch. The architecture strictly follows industry best practices (Enterprise-grade QA) with a strong emphasis on clean maintainability, fast execution, and advanced logging/reporting capabilities.

## 🚀 Core Technologies & Frameworks

*   **Programming Language:** Python 3.14+
*   **Core Automation Engine:** Selenium WebDriver (v4)
*   **Test Runner Engine:** PyTest
*   **Design Pattern:** Page Object Model (POM)
*   **Reporting Dashboard:** pytest-html (Interactive HTML report with embedded failure snapshots and step-by-step logging charts)

## 🏗️ Project Architecture

The codebase is engineered modularly to enforce a strict Separation of Concerns (SoC) layout:

```text
LearningSeleniumFromScratch/
│
├── conftest.py               # Global configurations, lifecycle hooks, and driver engine setups
├── pytest.ini                # PyTest configurations managing real-time system logging buffers
├── raport/
│   └── raport_teste.html     # Automatically generated interactive visual dashboard report
│
├── pages/                    # Page Object Layers (Encapsulating element locators and behaviors)
│   ├── __init__.py
│   ├── base_page.py          # Core interaction wrapper (Explicit Waits, fluid scrolling, clicking, typing)
│   ├── login_page.py         # Authentication layout mapping and functional action methods
│   └── inventory_page.py     # Inventory item components, forms, filters, and checkout step layers
│
└── tests/                    # Executable Test Suite Layers (Functional verification and assertions)
    ├── __init__.py
    ├── test_login.py         # Isolation scripts for verification (Positive & Parametrizied Negative cases)
    └── test_inventory.py     # Business flow validation scripts (End-to-End purchase & Math sorting orders)
```

## 💎 Key Features & Applied Best Practices

1.  **Page Object Model (POM):** Element mapping structures and webpage interactors are abstracted into dedicated controller classes. Test scripts contain zero hardcoded selectors, ensuring effortless code maintenance when application layouts shift.
2.  **Explicit Synchronization Waits:** Completely eliminates automated test flakiness by exclusively leveraging dynamic `WebDriverWait` mechanisms tied to targeted `visibility_of_element_located` states.
3.  **Advanced Driver Sandboxing (ChromeOptions):** The driver launches in **Incognito mode**, with **Headless mode** enabled for hyper-fast execution. It embeds specialized proxy switches to block intrusive browser credential pop-ups and mask runtime automation metadata (Anti-bot simulation).
4.  **Data-Driven Test Parametrization:** Negative authentication edge cases leverage `@pytest.mark.parametrize` matrices. This injects multiple unique credentials and dynamic assertion variables into a single clean test method.
5.  **Fixture Reusability (DRY Principle):** Successful application authentication loops are handled natively via a custom PyTest fixture (`logged_in_driver`). This provides inventory tests with an active, pre-authenticated driver instance, eliminating redundant code blocks.
6.  **Granular Low-Level Logging Engine:** Every action (URL loading, field interaction, click sequences, data scraping) maps out structured timestamp metrics containing module class files and exact runtime execution lines.
7.  **Failure Capture & HTML Embedding:** Built with custom runtime report wrapper hooks that intercept failing cases. It captures an immediate UI state snapshot to the `screenshots/` directory and embeds it directly inside the HTML report rows for fast debugging.

## 🛠️ Installation & Execution

### 1. Set Up Environment Dependencies
Ensure your active python virtual environment (`.venv`) is enabled, and deploy the configuration package library bundles:
```bash
pip install selenium pytest pytest-html
```

### 2. Execute the Full Automated Suite
Trigger the global test execution script directly from your root project directory terminal workspace to run all 7 isolated tests uninhibited in the background (Headless mode):
```bash
python -m pytest -v -s --html=raport/raport_teste.html
```

Once the test run loop completes, open the newly generated `raport/raport_teste.html` file in any standard browser to view the interactive test execution summary tables!
