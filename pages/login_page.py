from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.inventory_page import InventoryPage
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_url_contains("saucedemo.com")
        

        # Locators for the login page elements
        self.username_locator = (By.CSS_SELECTOR, "input[data-test='username']")
        self.password_locator = (By.CSS_SELECTOR, "input[data-test='password']")
        self.login_button_locator = (By.CSS_SELECTOR, "input[data-test='login-button']")
        
        self.alert_missing_user_locator = (By.XPATH, "//h3[contains(@data-test, 'error') and "
            "contains(., 'Username is required')]")
        self.alert_missing_password_locator = (By.XPATH, "//h3[contains(@data-test, 'error') and "
            "contains(., 'Password is required')]")
        self.alert_invalid_credentials_locator = (By.XPATH, "//h3[contains(@data-test, 'error') and "
            "contains(., 'not match')]")
        self.alert_locked_user_locator = (By.XPATH, "//h3[contains(@data-test, 'error') and "
            "contains(., 'locked out')]")
        
        
    # Login methods
    def _login(self, username, password):
        self.input_text(self.username_locator, username)
        self.input_text(self.password_locator, password)
        self.click_element(self.login_button_locator)

    def _login_expect_error(self, username, password, error_locator):
        self._login(username, password)
        try:
            self.wait_for_element_visible(error_locator)
            return self 
        except AssertionError:
            raise AssertionError(f"Error message not found within {self.timeout} seconds. Used locator: {error_locator}")

    def login_expect_success(self, username, password):
        self._login(username, password)
        self.wait_for_url_contains("inventory.html")
        return InventoryPage(self.driver)
            
    def login_expect_invalid_credentials(self, username, password):
        return self._login_expect_error(username, password, self.alert_invalid_credentials_locator)
        
    def login_expect_missing_username(self, username, password):
        return self._login_expect_error(username, password, self.alert_missing_user_locator)
    
    
    def login_expect_locked_user(self, username, password):
        return self._login_expect_error(username, password, self.alert_locked_user_locator)