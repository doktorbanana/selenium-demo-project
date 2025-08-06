from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
            return WebDriverWait(self.driver, self.timeout).until(EC.url_contains(substring))
        except TimeoutException:
            current_url = self.driver.current_url
            raise AssertionError(
                f"Page load failed. Expected URL to contain: '{substring}', "
                f"Current URL: '{current_url}'"
            )
        
    def wait_for_element(self, locator):  
        return WebDriverWait(self.driver, self.timeout).until(  
            EC.presence_of_element_located(locator)
        )
    
    def wait_for_element_visible(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(  
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_element_clickable(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(  
            EC.element_to_be_clickable(locator)
        )

    def click_element(self, locator):  
        self.wait_for_element_clickable(locator).click()  
      
    def input_text(self, locator, text):  
        self.wait_for_element_visible(locator).send_keys(text)