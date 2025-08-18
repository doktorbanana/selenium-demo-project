"""
This file contains the configuration and fixtures for the test suite.
It includes browser setup, screenshot handling, and custom command-line
options.
"""

from pages.login_page import LoginPage
from utils.driver_factory import DriverFactory
from utils.logger import Logger
from selenium.webdriver.common.by import By
import pytest
from datetime import datetime
import pytest_html
import os
import shutil


SCREENSHOTS_PATH_RELATIVE = "screenshots"
SCREENSHOTS_PATH = os.path.join("test_reports", SCREENSHOTS_PATH_RELATIVE)
LOG_PATH_RELATIVE = "logs"
LOG_PATH = os.path.join("test_reports", LOG_PATH_RELATIVE)


def pytest_addoption(parser):
    """Add custom command-line options for pytest."""
    parser.addoption(
        "--intentionally-fail",
        action="store_true",
        default=False,
        help="Run tests that are intentionally failing "
        "for demonstration purposes."
    )

    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome or firefox"
    )

    parser.addoption(
        "--docker",
        action="store_true",
        default=False,
        help="Run tests in Docker environment"
    )


############
# FIXTURES #
############

@pytest.fixture(scope="session")
def logger(request):
    browser_name = request.config.getoption("--browser", default="chrome")
    remote = request.config.getoption("--docker", default=False)
    logger = Logger((browser_name, "Docker" if remote else "Local"))
    yield logger


@pytest.fixture(scope="function")
def test_case_logger(request, logger):
    test_id = request.node.name
    with logger.get_test_case(test_id) as test_case:
        try:
            yield test_case
            test_case["status"] = "PASS"
        except Exception as e:
            test_case["status"] = "FAIL"
            test_case["metadata"]["log_level"] = "ERROR"
            test_case["error"] = {
                "message": str(e),
                "stack_trace": logger._get_stack_trace(e)
            }
        finally:
            logger.close_test_case(test_case)


@pytest.fixture(scope="function")
def setup_browser(request):
    """
    Set up the browser for testing based on command-line options.
    """
    browser_name = request.config.getoption("--browser", default="chrome")
    remote = request.config.getoption("--docker", default=False)

    driver = DriverFactory.create_driver(browser_name, remote)
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
        report = _add_screenshots_to_report(report, item)
    return report


def _add_screenshots_to_report(report, item):
    driver = item.funcargs.get('setup_browser')
    if driver:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
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


def pytest_configure(config):
    _create_screenshot_path()


def _create_screenshot_path():
    """Create a directory for screenshots at the start of the session."""
    if os.path.exists(SCREENSHOTS_PATH):
        shutil.rmtree(SCREENSHOTS_PATH)
    os.makedirs(SCREENSHOTS_PATH)
