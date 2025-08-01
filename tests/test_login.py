from pages.login_page import LoginPage
import pytest

@pytest.mark.parametrize("username, password, expected", [
    ("standard_user", "secret_sauce", "inventory_page"),        # Valid
    ("", "", "empty_fields_error"),                             # Empty fields
    ("locked_out_user", "secret_sauce", "locked_out_error"),    # Locked out user
    ("invalid", "invalid", "invalid_creds_error")               # Invalid credentials
])

def test_login(setup_browser, username, password, expected):
    driver = setup_browser
    driver.get("https://saucedemo.com")

    login_page = LoginPage(driver)

    match expected:
        case "inventory_page":
            inventory_page = login_page.login_expect_success(username, password)
            assert inventory_page.url_contains("inventory.html"), "Login failed or did not redirect to inventory page"
        
        case "empty_fields_error":
            login_page.login_expect_missing_username(username, password)
            assert login_page.wait_for_element(login_page.alert_missing_user_locator), "Missing username error not displayed"
        
        case "locked_out_error":
            login_page.login_expect_locked_user(username, password)
            assert login_page.wait_for_element(login_page.alert_locked_user_locator), "Locked out user error not displayed"
        
        case "invalid_creds_error":
            login_page.login_expect_invalid_credentials(username, password)
            assert login_page.wait_for_element(login_page.alert_invalid_credentials_locator), "Invalid credentials error not displayed"
        case _:
            pytest.fail(f"Unexpected expected value: {expected}")