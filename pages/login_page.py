"""
This file contains the LoginPage class,
which provides methods to interact with the login page of the application.
It includes methods for logging in with different scenarios,
such as successful login, missing username, missing password,
locked user, and invalid credentials.
"""

from selenium.webdriver.common.by import By
from pages.inventory_page import InventoryPage
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page object for the login page,
    providing methods to perform login actions.
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_url_contains("saucedemo.com")
        self.wait_for_page_ready()

        # Locators for the login page elements
        self.username_locator = (
            By.CSS_SELECTOR,
            "input[data-test='username']")
        self.password_locator = (
            By.CSS_SELECTOR,
            "input[data-test='password']")
        self.login_button_locator = (
            By.CSS_SELECTOR,
            "input[data-test='login-button']")
        self.alert_missing_user_locator = (
            By.XPATH, "//h3[contains(@data-test, 'error') and "
            "contains(., 'Username is required')]")
        self.alert_missing_password_locator = (
            By.XPATH, "//h3[contains(@data-test, 'error') and "
            "contains(., 'Password is required')]")
        self.alert_invalid_credentials_locator = (
            By.XPATH, "//h3[contains(@data-test, 'error') and "
            "contains(., 'not match')]")
        self.alert_locked_user_locator = (
            By.XPATH, "//h3[contains(@data-test, 'error') and "
            "contains(., 'locked out')]")

    # Login methods
    def _login(self, username, password):
        """
        Performs the login action with the provided username and password.
        """
        self.input_text(self.username_locator, username)
        self.input_text(self.password_locator, password)
        self.click_element(self.login_button_locator)

    def _login_expect_error(self, username, password, error_locator):
        """Logs in and expects an error message to be displayed."""
        self._login(username, password)
        try:
            self.wait_for_element_visible(error_locator)
            return self
        except AssertionError:
            raise AssertionError(
                f"Error message not found within {self.timeout} seconds. "
                f"Used locator: {error_locator}")

    def login_expect_success(self, username, password):
        """Logs in and expects to be redirected to the inventory page."""
        self._login(username, password)
        self.wait_for_url_contains("inventory.html")
        return InventoryPage(self.driver)

    def login_expect_invalid_credentials(self, username, password):
        """Logs in with invalid credentials and expects an error message."""
        return self._login_expect_error(username,
                                        password,
                                        self.alert_invalid_credentials_locator)

    def login_expect_missing_username(self, username, password):
        """Logs in with a missing username and expects an error message."""
        return self._login_expect_error(username,
                                        password,
                                        self.alert_missing_user_locator)

    def login_expect_missing_password(self, username, password):
        """Logs in with a missing password and expects an error message."""
        return self._login_expect_error(username,
                                        password,
                                        self.alert_missing_password_locator)

    def login_expect_locked_user(self, username, password):
        """Logs in with a locked user and expects an error message."""
        return self._login_expect_error(username,
                                        password,
                                        self.alert_locked_user_locator)
