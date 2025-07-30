from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pytest  


@pytest.fixture(scope="function")
def setup_browser():
    driver = webdriver.Chrome()    
    yield driver
    driver.quit()