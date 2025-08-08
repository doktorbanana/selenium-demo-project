from pages.base_page import BasePage


class ItemPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_url_contains("inventory-item.html")
