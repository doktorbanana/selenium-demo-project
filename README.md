# Automated Test Framework for SauceDemo.com

[![GitHub Actions](https://github.com/doktorbanana/selenium-demo-project/actions/workflows/run_tests.yml/badge.svg)](https://github.com/doktorbanana/selenium-demo-project/actions)

Professional test automation demonstrating industry best practices for web application testing. Designed to showcase testing expertise for Software Tester positions with focus on maintainability, reliability, and CI/CD integration.

## Key Features

### 🧩 Page Object Model Architecture
- Strict separation of test logic and UI locators
- Inheritable base page with common interactions
- Domain-specific pages for login, inventory, and product details

### 📊 Data-Driven Testing
- CSV parameterization for user credentials and products
- Dynamic test case generation from external files
- Custom data loader utility for easy test data management

### 🛡️ Robust Error Handling
- Automatic failure screenshots with full-page capture
- Smart waits for element visibility and interactions
- Flaky test retry mechanism with configurable delays

### 📦 CI/CD Ready
- GitHub Actions workflow for continuous testing
- Self-contained HTML reports with screenshot attachments on failure

## Technologies Used

- Python 3.10+
- Selenium WebDriver 4.34.2
- pytest 8.4.1
- pytest-html (HTML reporting)
- GitHub Actions (CI/CD)

## Setup Instructions

Clone repository:
```
git clone https://github.com/doktorbanana/selenium-demo-project.git
cd <path/to/project>
```

Create virtual environment:
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

Install dependencies:
```
pip install -r requirements.txt
````

## Running Tests

Tests are automatically run with html-report and rerun of failed flaky tests via:
```
pytest
````

Execute intentionally failing demo test:
```
pytest --intentionally-fail
```

## Future Enhancements

This project is work in progress. The following improvements are planned:

- Add cross-browser testing (Firefox, Edge)
- Add mobile device emulation
- Add logging for better test debugging
- Integrate with a test management tool (e.g., TestRail, Xray)
- Add more test scenarios (e.g., sorting, filtering, checkout process)

