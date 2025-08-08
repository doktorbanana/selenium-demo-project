"""
This file contains the configuration and fixtures for the test suite.
It includes browser setup, screenshot handling, and custom command-line
options.
"""

from selenium import webdriver
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
    """Add custom command-line options for pytest."""
    parser.addoption(
        "--intentionally-fail",
        action="store_true",
        default=False,
        help="Run tests that are intentionally failing "
        "for demonstration purposes."
    )


def pytest_sessionstart(session):
    """Create a directory for screenshots at the start of the session."""
    if os.path.exists(SCREENSHOTS_PATH):
        shutil.rmtree(SCREENSHOTS_PATH)
    os.makedirs(SCREENSHOTS_PATH)


############
# FIXTURES #
############


@pytest.fixture(scope="function")
def setup_browser():
    """Set up the browser for testing."""
    options = webdriver.ChromeOptions()
    prefs = {
        "profile.password_manager_leak_detection_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def standard_login(setup_browser):
    """
    Log in with standard user credentials
    and return the inventory page.
    """
    driver = setup_browser
    driver.get("https://saucedemo.com")
    login_page = LoginPage(driver)
    return login_page.login_expect_success("standard_user", "secret_sauce")


#########
# HOOKS #
#########


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshots on test failure."""
    report = yield

    if report.when == "call" and report.failed:
        driver = item.funcargs.get('setup_browser')
        if driver:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(SCREENSHOTS_PATH, screenshot_name)

            original_size = driver.get_window_size()
            required_width = driver.execute_script(
                'return document.body.parentNode.scrollWidth')
            required_height = driver.execute_script(
                'return document.body.parentNode.scrollHeight')
            driver.set_window_size(required_width, required_height)
            driver.find_element(By.TAG_NAME, 'body').screenshot(
                screenshot_path)
            driver.set_window_size(original_size['width'],
                                   original_size['height'])

            screenshot_path_relative = os.path.join(
                SCREENSHOTS_PATH_RELATIVE,
                screenshot_name)
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.image(screenshot_path_relative))
            report.extras = extras

    return report
