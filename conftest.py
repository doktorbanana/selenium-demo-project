from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pytest
import datetime
import pytest_html
import os
import shutil



SCREENSHOT_PATH_RELATIVE = "screenshots"
SCREENSHOT_PATH = "test_reports/" + SCREENSHOT_PATH_RELATIVE

def pytest_addoption(parser):
    parser.addoption(
        "--intentionally-fail", action="store_true", default=False, help="Run tests that are intentionally failing for demonstration purposes."
    )

def pytest_sessionsionstart(session):
    # Create an empty directory for screenshots
    if os.path.exists(SCREENSHOT_PATH):
        shutil.rmtree(SCREENSHOT_PATH)
    os.mkdir(SCREENSHOT_PATH)

@pytest.fixture(scope="function")
def setup_browser():
    # Add headless mode for CI compatibility
    options = webdriver.ChromeOptions()
    
    prefs = {
        "profile.password_manager_leak_detection_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.delete_all_cookies()   
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
            screenshot_name = f"{item.name}_{timestamp}.png"
 
            original_size = driver.get_window_size()
            required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(required_width, required_height)
            driver.find_element(By.TAG_NAME, 'body').screenshot(
                SCREENSHOT_PATH + "/" + screenshot_name)
            driver.set_window_size(original_size['width'], original_size['height'])

            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.image(SCREENSHOT_PATH_RELATIVE + screenshot_name))
            report.extras = extras

    return report
