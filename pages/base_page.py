from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10  # Default timeout for waits

    def get_page_title(self):
        return self.driver.title

    def url_contains(self, substring):
        return substring in self.driver.current_url

    def wait_for_url_contains(self, substring):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.url_contains(substring)
                )
        except TimeoutException:
            current_url = self.driver.current_url
            raise AssertionError(
                f"Page load failed. Expected URL to contain: '{substring}', "
                f"Current URL: '{current_url}'"
            )

    def wait_for_element(self, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise AssertionError(
                f"Element with locator {locator} not found "
                f"within {self.timeout} seconds")

    def wait_for_element_visible(self, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise AssertionError(
                f"Element with locator {locator} not visible "
                f"within {self.timeout} seconds")

    def wait_for_element_not_visible(self, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            raise AssertionError(
                f"Element with locator {locator} still visible "
                f"after {self.timeout} seconds")

    def wait_for_element_clickable(self, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            raise AssertionError(
                f"Element with locator {locator} not clickable "
                f"within {self.timeout} seconds")

    def click_element(self, locator):
        self.wait_for_element_clickable(locator).click()

    def input_text(self, locator, text):
        self.wait_for_element_visible(locator).send_keys(text)
