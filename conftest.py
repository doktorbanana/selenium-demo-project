from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pytest
import datetime
import pytest_html
import os
import shutil

def pytest_addoption(parser):
    parser.addoption(
        "--intentionally-fail", action="store_true", default=False, help="Run tests that are intentionally failing for demonstration purposes."
    )

@pytest.fixture(scope="function")
def setup_browser():
    # Add headless mode for CI compatibility
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
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

            if os.path.exists(screenshot_path):
                shutil.rmtree(screenshot_path)
            
            os.mkdir(screenshot_path)
 
            original_size = driver.get_window_size()
            required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(required_width, required_height)
            driver.find_element(By.TAG_NAME, 'body').screenshot(screenshot_path
                                                               + "/" + screenshot_name)
            driver.set_window_size(original_size['width'], original_size['height'])

            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.image("screenshots/" + screenshot_name))
            report.extras = extras


    return report
