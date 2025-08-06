from pages.login_page import LoginPage
from utils.data_loader import load_csv
import pytest

products = load_csv("./test_data/products.csv")

@pytest.mark.parametrize("product", products)
def test_img_click(setup_browser, product):
    driver = setup_browser
    driver.get("https://saucedemo.com")

    product_name = product["product_name"]
    
    login_page = LoginPage(driver)
    inventory_page = login_page.login_expect_success("standard_user", "secret_sauce")
    item_page = inventory_page.click_product_img(product_name)

    assert item_page.url_contains("item.html"), "Clicking product image did not redirect to item page"


@pytest.mark.parametrize("product", products)
def test_link_click(setup_browser, product):
    driver = setup_browser
    driver.get("https://saucedemo.com")

    product_name = product["product_name"]
    print(product_name)
    
    login_page = LoginPage(driver)
    inventory_page = login_page.login_expect_success("standard_user", "secret_sauce")
    item_page = inventory_page.click_product_link(product_name)

    assert item_page.url_contains("item.html"), "Clicking product link did not redirect to item page"