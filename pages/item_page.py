from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class ItemPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_url_contains("inventory-item.html")

