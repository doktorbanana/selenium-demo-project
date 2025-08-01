from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pytest  


@pytest.fixture(scope="function")
def setup_browser():
    # Add headless mode for CI compatibility
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    
    driver = webdriver.Chrome(options=options)    
    yield driver
    driver.quit()