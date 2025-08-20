"""
This file contains the configuration and fixtures for the test suite.
It includes browser setup, screenshot handling, and custom command-line
options.
"""

from pages.login_page import LoginPage
from utils.driver_factory import DriverFactory
from utils.logger import Logger, TestState
from utils.json_log_to_html import json_log_to_html
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
    """
    Provide a Logger for the Test Run
    """
    browser_name = request.config.getoption("--browser", default="chrome")
    remote = request.config.getoption("--docker", default=False)
    logger = Logger((browser_name, "Docker" if remote else "Local"))
    yield logger


@pytest.fixture(scope="function")
def test_case_log(request, logger):
    """
    Provide a Log for this test case
    """
    with logger.create_test_case(request.node.name) as case_log:

        yield case_log

        if hasattr(request.node, "rep_call"):
            report = request.node.rep_call
            if report.failed:
                case_log.add_error(report)
            else:
                if case_log.status == "undefined":
                    case_log.set_status(TestState.PASSED)

            logger.log_test_case(case_log)
            json_log = [case_log.get_json_test_data(indent=None, ascii=True)]
            _add_custom_log_to_report(report, json_log)
            logger.remove_test_case(case_log)
        else:
            raise Warning("Couldn't Log TestData."
                          "Test Report was not found as an attribute")


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
    """
    Save test report as test attribute to make it accessible in fixtures.
    And capture screenshots on test failure.
    """
    report = yield
    setattr(item, f"rep_{call.when}", report)
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


def _add_custom_log_to_report(report, json_log_data):
    html_report = json_log_to_html(json_log_data)
    extras = getattr(report, "extras", [])
    extras.append(pytest_html.extras.html(html_report))
    report.extras = extras
    return report
