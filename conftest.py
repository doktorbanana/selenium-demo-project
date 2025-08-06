from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pytest  


@pytest.fixture(scope="function")
def setup_browser():
    # Add headless mode for CI compatibility
    options = webdriver.ChromeOptions()
    
    prefs = {
        "profile.password_manager_leak_detection_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    #options.add_argument("--headless=new")
    
    driver = webdriver.Chrome(options=options)
    driver.delete_all_cookies()   
    yield driver
    driver.quit()