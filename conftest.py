from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pytest
import datetime
import pytest_html
import os
import shutil
from pages.login_page import LoginPage


SCREENSHOTS_PATH_RELATIVE = "screenshots"
SCREENSHOTS_PATH = os.path.join("test_reports", SCREENSHOTS_PATH_RELATIVE)

def pytest_addoption(parser):
    parser.addoption(
        "--intentionally-fail", action="store_true", default=False, help="Run tests that are intentionally failing for demonstration purposes."
    )

def pytest_sessionstart(session):
    # Create an empty directory for screenshots
    if os.path.exists(SCREENSHOTS_PATH):
        shutil.rmtree(SCREENSHOTS_PATH)
    os.makedirs(SCREENSHOTS_PATH)

##### FIXTURES #####
@pytest.fixture(scope="function")
def setup_browser():
    # Add headless mode for CI compatibility
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)    
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def standard_login(setup_browser):
    driver = setup_browser
    driver.get("https://saucedemo.com")
    login_page = LoginPage(driver)
    return login_page.login_expect_success("standard_user", "secret_sauce")
    

##### HOOKS #####
@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    # This hook is used to capture the test report and take a screenshot if the test fails
    
    report = yield

    if report.when== "call" and report.failed:
        driver = item.funcargs.get('setup_browser')
        if driver:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(SCREENSHOTS_PATH, screenshot_name)

            original_size = driver.get_window_size()
            required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(required_width, required_height)
            driver.find_element(By.TAG_NAME, 'body').screenshot(screenshot_path)
            driver.set_window_size(original_size['width'], original_size['height'])

            screenshot_path_relative = os.path.join(SCREENSHOTS_PATH_RELATIVE, screenshot_name)
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.image(screenshot_path_relative))
            report.extras = extras

    return report
