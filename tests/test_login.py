"""
This file contains tests for the login functionality of the application.
It includes tests for successful login, missing username, missing password,
locked user, and invalid credentials.
"""
from pages.login_page import LoginPage
from utils.data_loader import load_csv
import pytest

users = load_csv("./test_data/users.csv")
custom_ids = [f"{row['custom_id']}" for row in users]


@pytest.mark.parametrize("user", users, ids=custom_ids)
def test_login(setup_browser, user):
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

    match expected:
        case "inventory_page":
            inventory_page = login_page.login_expect_success(
                username,
                password)
            assert inventory_page.url_contains(
                "inventory.html"), ""\
                "Login failed or did not redirect to inventory page"

        case "empty_fields_error":
            login_page.login_expect_missing_username(username, password)
            assert login_page.wait_for_element(
                login_page.alert_missing_user_locator), ""\
                "Missing username error not displayed"

        case "missing_username_error":
            login_page.login_expect_missing_username(username, password)
            assert login_page.wait_for_element(
                login_page.alert_missing_user_locator), ""\
                "Missing username error not displayed"

        case "missing_password_error":
            login_page.login_expect_missing_password(username, password)
            assert login_page.wait_for_element(
                login_page.alert_missing_password_locator), ""\
                "Missing password error not displayed"

        case "locked_out_error":
            login_page.login_expect_locked_user(username, password)
            assert login_page.wait_for_element(
                login_page.alert_locked_user_locator), ""\
                "Locked out user error not displayed"

        case "invalid_creds_error":
            login_page.login_expect_invalid_credentials(username, password)
            assert login_page.wait_for_element(
                login_page.alert_invalid_credentials_locator), ""\
                "Invalid credentials error not displayed"

        case _:
            pytest.fail(f"Unexpected expected value: {expected}")
