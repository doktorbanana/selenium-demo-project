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
- Custom logs for easy debugging on failure
- JSON-logs for compatibility with test management services

### 📦 CI/CD Ready
- GitHub Actions workflow for continuous testing
- Self-contained HTML reports with screenshot attachments on failure

### 🐳 Docker Support
- Containerized testing supported
- Pre-configured `docker-compose.yml` for local setup
- Remote use of docker in Github Actions: containers for each Browser

### 🌐 Cross-Browser Testing
- Chrome/Firefox
- Remote: parallel execution with browser matrix
- Local: choose with CLI-option (`browser=`)

## Technologies Used

- Python 3.10+
- Selenium WebDriver 4.34.2
- pytest 8.4.1
- pytest-html (HTML reporting)
- GitHub Actions (CI/CD)
- Docker (containerized testing)

## Setup Instructions

### Basic Setup
```
git clone https://github.com/doktorbanana/selenium-demo-project.git
cd <path/to/project>

python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### Docker Setup (Optional)
The tests can be executed in Docker containers for each browser. If Docker is installed on your system, run the following command to setup the images:

```
docker-compose up -d  # Start required containers
```

Note: On the github-hosted remote runners Docker is enabled by default.

## Running Tests

Tests are automatically run in Chrome with html-report and rerun of failed flaky tests via:
```
pytest
````

Optional flags:
```
--intentionally-fail # run test that fails intentionally to checkout error-handling
--browser=firefox # choose between chrome and firefox
--docker # execute tests in docker container (needs installation, see above)
```

## Future Enhancements

This project is work in progress. The following improvements are planned:

- Add mobile device emulation
- Integrate with a test management tool (e.g., TestRail, Xray)
- Add more test scenarios (e.g., sorting, filtering, checkout process)

