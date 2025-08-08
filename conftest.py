from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pytest
import datetime
import pytest_html
import os

@pytest.fixture(scope="function")
def setup_browser():
    # Add headless mode for CI compatibility
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)    
    yield driver
    driver.quit()

@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    # This hook is used to capture the test report and take a screenshot if the test fails
    
    report = yield

    if report.when== "call" and report.failed:
        driver = item.funcargs.get('setup_browser')
        if driver:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"test_reports/screenshots"
            screenshot_name = f"{item.name}_{timestamp}.png"

            if not os.path.exists(screenshot_path):
                os.mkdir(screenshot_path)

            driver.save_screenshot(screenshot_path + "/" + screenshot_name)

            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.image("../" + screenshot_path + "/" + screenshot_name))
            report.extras = extras


    return report
