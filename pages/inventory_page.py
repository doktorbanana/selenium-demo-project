from pages.base_page import BasePage
from pages.item_page import ItemPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait_for_url_contains("inventory.html")
        
        # Locators for the inventory page elements
        self.inventory_item_locator = (By.CSS_SELECTOR, "div[data-test='inventory-item']")
        self.item_name_locator = (By.CSS_SELECTOR, "div[data-test='inventory-item-name']")
        self.item_link_locator = (By.CSS_SELECTOR, "a[data-test$='title-link']")
        self.item_img_locator = (By.CSS_SELECTOR, "img[data-test^='inventory-item'][data-test$='img']")
        
        self.add_to_cart_button_locator = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
        self.remove_from_cart_button_locator = (By.CSS_SELECTOR, "button[data-test^='remove-']")
        
        self.cart_item_count_locator = (By.CSS_SELECTOR, "span[data-test='shopping-cart-badge']")


    def get_products(self):
        products = self.driver.find_elements(*self.inventory_item_locator)
        return products

    def get_product_by_name(self, product_name):
        products = self.get_products()
        for product in products:
            name = product.find_element(*self.item_name_locator).text
            if name == product_name:
                return product
        raise AssertionError(f"Product '{product_name}' not found in inventory. Products available: {[p.text for p in products]}")
    
    def click_add_to_cart(self, product_name):
        product = self.get_product_by_name(product_name)
        add_button = product.find_element(*self.add_to_cart_button_locator)
        add_button.click()
        
    def click_remove_from_cart(self, product_name):
        product = self.get_product_by_name(product_name)
        self.wait_for_element_visible(self.remove_from_cart_button_locator)
        remove_button = product.find_element(*self.remove_from_cart_button_locator)
        remove_button.click()
        
    def click_product_link(self, product_name):
        product = self.get_product_by_name(product_name)
        self.wait_for_element_visible(self.item_link_locator)
        product_link = product.find_element(*self.item_link_locator)
        product_link.click()
        return ItemPage(self.driver)
                
    def click_product_img(self, product_name):
        product = self.get_product_by_name(product_name)
        self.wait_for_element_visible(self.item_img_locator)
        product_img = product.find_element(*self.item_img_locator)
        product_img.click()
        return ItemPage(self.driver)
    
    def get_num_of_items_in_cart(self):
        try:
            self.wait_for_element_visible(self.cart_item_count_locator)
            cart_item = self.driver.find_element(*self.cart_item_count_locator)
            return int(cart_item.text)
        except AssertionError:
            return 0
    
    