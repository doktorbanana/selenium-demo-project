from pages.base_page import BasePage
from pages.item_page import ItemPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        try:
            self.wait_for_url_contains("inventory.html")
        except TimeoutException:
            raise AssertionError("We are not on the Inventory page")
        
        # Locators for the inventory page elements
        self.inventory_item_locator = (By.CSS_SELECTOR, "div[data-test='inventory-item']")
        self.item_name_locator = (By.CSS_SELECTOR, "div[data-test='inventory-item-name']")
        self.item_link_locator = (By.CSS_SELECTOR, "a[data-test$='title-link']")
        self.item_img_locator = (By.CSS_SELECTOR, "img[data-test^='inventory-item'][data-test$='img']")
        
        self.add_to_cart_button_locator = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
        self.remove_from_cart_button_locator = (By.CSS_SELECTOR, "button[data-test^='remove-']")
        
        self.cart_item_count_locator = (By.CSS_SELECTOR, "span[data-test='shopping_cart_badge']")


    def get_products(self):
        return self.driver.find_elements(*self.inventory_item_locator)

    def get_product_by_name(self, product_name):
        products = self.get_products()
        for product in products:
            name = product.find_element(*self.item_name_locator).text
            if name == product_name:
                return product
            else:
                raise AssertionError(f"Product '{product_name}' not found in inventory")
    
    def click_add_to_cart(self, product_name):
        product = self.get_product_by_name(product_name)
        if product:
            add_button = product.find_element(*self.add_to_cart_button_locator)
            add_button.click()
        else:
            raise AssertionError(f"Product '{product_name}' not found in inventory")
        
    def click_remove_from_cart(self, product_name):
        product = self.get_product_by_name(product_name)
        if product:
            remove_button = product.find_element(*self.remove_from_cart_button_locator)
            remove_button.click()
        else:
            raise AssertionError(f"Product '{product_name}' not found in inventory")
    
    def click_product_link(self, product_name):
        product = self.get_product_by_name(product_name)
        if product:
            product_link = product.find_element(*self.item_link_locator)
            product_link.click()
        else:
            raise AssertionError(f"Product '{product_name}' not found in inventory")
        
    def click_product_img(self, product_name):
        product = self.get_product_by_name(product_name)
        self.wait_for_element_visible(self.item_img_locator)
        if product:
            product_img = product.find_element(*self.item_img_locator)
            product_img.click()
            return ItemPage(self.driver)
        else:
            raise AssertionError(f"Product '{product_name}' not found in inventory. Products available: {[p.text for p in self.get_products()]}")

    def get_num_of_items_in_cart(self):
        cart_item = self.driver.find_element(self.cart_item_count_locator)
        if cart_item:
            return int(cart_item.text)
        else:
            return 0
    
    