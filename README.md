# 🚀 Learning Selenium From Scratch

![Automation Status](https://github.com)
[![Allure Report](https://shields.io)](https://github.io)

A fully modularized, enterprise-grade hybrid test automation framework built in **Python** using **PyTest**. The project integrates robust backend service validations (**API Testing**) and graphical web interface automation (**Selenium UI Testing**), highly optimized for parallel execution within modern CI/CD pipelines.

---

## 🏗️ Project Architecture

```text
LearningSeleniumFromScratch/
├── .github/workflows/
│   └── workflow.yml        # Unified GitHub Actions pipeline (Multi-browser Matrix)
├── data/
│   └── test_env.json       # Global environment configurations (Target base URLs)
├── features/
│   ├── login.feature       # Gherkin BDD login execution scenarios
│   └── purchase.feature    # Gherkin BDD end-to-end checkout flow scenarios
├── pages/
│   ├── base_page.py        # Custom Selenium wrapper with dynamic explicit waits
│   ├── login_page.py       # Page Object Model locators & methods for Login
│   └── inventory_page.py   # Page Object Model locators & methods for Inventory/Checkout
├── tests/
│   ├── test_api/           # Dedicated REST API testing suite (ReqRes)
│   │   ├── api_client.py   # HTTP Client Wrapper over the requests library
│   │   ├── conftest.py     # API-specific fixtures (Session setup & auth token caching)
│   │   └── test_api.py     # Functional REST API assertions & CRUD validations
│   └── test_ui/            # Dedicated UI testing suite using Selenium
│       ├── conftest.py     # WebDriver initializations (Headless Chrome/FF/Edge) & failure hooks
│       ├── test_login.py   # Data-Driven UI authentication tests
│       └── test_sorting.py # Algorithmic DOM price sorting engine verifications
└── pytest.ini              # Main global test suite configuration file
```

## 🛠️ Local Installation & Configuration

### 1. Clone the Repository and Setup a Virtual Environment
```bash
git clone https://github.com
cd LearningSeleniumFromScratch

# Create and activate an isolated Python virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Project Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running Tests Locally from Terminal

### Execute the Backend REST API Test Suite
```bash
pytest tests/test_api/ -v
```

### Execute the Graphical Selenium UI Test Suite
```bash
# Run using the default browser configuration (Chrome Headless)
pytest tests/test_ui/ -v

# Force execution on specific targeted browsers via the command line
pytest tests/test_ui/ --browser=firefox -v
pytest tests/test_ui/ --browser=edge -v
```

### Generate Standalone Local PyTest HTML Reports
```bash
pytest tests/test_ui/ --html=raport/report.html --self-contained-html -v
```

---

## ☁️ CI/CD Pipeline Infrastructure (GitHub Actions)

Upon every code `push` or `pull_request` event targeting the `main` branch, an automated deployment pipeline executes seamlessly:
1. **Matrix Strategy Isolation**: Orchestrates the graphical test suite concurrently across three distinct virtualized environment nodes running **Google Chrome**, **Mozilla Firefox**, and **Microsoft Edge**.
2. **Allure History Injection**: Automatically tracks and pulls structural execution records from the historical `gh-pages` branch to compute stability metrics and execution trend curves.
3. **Automated Static Deployment**: Compiles the analytical browser outputs and deploys an interactive cross-browser entry dashboard directly to **GitHub Pages** post-execution.
