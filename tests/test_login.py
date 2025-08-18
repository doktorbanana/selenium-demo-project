"""
This file contains tests for the login functionality of the application.
It includes tests for successful login, missing username, missing password,
locked user, and invalid credentials.
"""
from pages.login_page import LoginPage
from utils.data_loader import load_csv
import pytest
from selenium.common.exceptions import TimeoutException

users = load_csv("./test_data/users.csv")
custom_ids = [f"{row['custom_id']}" for row in users]


@pytest.mark.parametrize("user", users, ids=custom_ids)
@pytest.mark.login
def test_login(setup_browser, test_case_log, user):
    """
    Test logging in with various user scenarios.
    This test covers successful login, missing username, missing password,
    locked user, and invalid credentials.
    """
    driver = setup_browser
    driver.get("https://saucedemo.com")

    login_page = LoginPage(driver)

    username = user["username"]
    password = user["password"]
    expected = user["expected"]

    test_case_log.set_description(
        f"Testing Login as '{user["custom_id"]}'."
        f" Expecting '{expected}' after clicking login button."
        )
    test_case_log.set_severity("High")
    test_case_log.set_owner("QA")
    test_case_log.add_step("1. Navigated to saucedemo.org")

    match expected:
        case "inventory_page":
            try:
                login_page.login_expect_success(
                    username,
                    password)
                test_case_log.add_step(
                    "2. Logged in with valid credentials"
                )
            except TimeoutException:
                msg = ("Login failed or did not redirect"
                       " to inventory page."
                       " Current URL:"
                       f" {driver.current_url}")
                raise AssertionError(msg)

        case "empty_fields_error":
            try:
                login_page.login_expect_missing_username(username, password)
                test_case_log.add_step(
                    "2. Logged in with empty fields"
                )
            except TimeoutException:
                msg = "Missing username error not displayed."
                raise AssertionError(msg)

        case "missing_username_error":
            try:
                login_page.login_expect_missing_username(username, password)
                test_case_log.add_step(
                    "2. Logged in with emtpy username field"
                )
            except TimeoutException:
                msg = "Missing username error not displayed."
                raise AssertionError(msg)

        case "missing_password_error":
            try:
                login_page.login_expect_missing_password(username, password)
                test_case_log.add_step(
                    "2. Logged in with empty password field"
                )
            except TimeoutException:
                msg = "Missing password error not displayed."
                raise AssertionError(msg)

        case "locked_out_error":
            try:
                login_page.login_expect_locked_user(username, password)
                test_case_log.add_step(
                    "2. Logged in as locked out user"
                )
            except TimeoutException:
                msg = "Locked out user error not displayed."
                raise AssertionError(msg)

        case "invalid_creds_error":
            try:
                login_page.login_expect_invalid_credentials(username, password)
                test_case_log.add_step(
                    "2. Logged in with invalid credentials"
                )
            except TimeoutException:
                msg = ("Invalid credentials"
                       " error not displayed.")
                raise AssertionError(msg)

        case _:
            pytest.fail(f"Unexpected expected value: {expected}")
