from pages.login_page import LoginPage
from utils.data_loader import load_csv
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

products = load_csv("./test_data/products.csv")
custom_ids = [f"{row['custom_id']}" for row in products]

@pytest.mark.parametrize("product", products, ids=custom_ids)
@pytest.mark.flaky(reruns=5, reruns_delay=2)
def test_img_click(standard_login, product):
    product_name = product["product_name"]
    inventory_page = standard_login
    item_page = inventory_page.click_product_img(product_name)
    assert item_page.url_contains("item.html"), "Clicking product image did not redirect to item page"


@pytest.mark.parametrize("product", products, ids=custom_ids)
@pytest.mark.flaky(reruns=5, reruns_delay=2)
def test_link_click(standard_login, product):
    product_name = product["product_name"]
    inventory_page = standard_login
    item_page = inventory_page.click_product_link(product_name)

    assert item_page.url_contains("item.html"), "Clicking product link did not redirect to item page"


def test_cart_count(setup_browser):
    driver = setup_browser
    driver.get("https://saucedemo.com")
    
    login_page = LoginPage(driver)
    inventory_page = login_page.login_expect_success("standard_user", "secret_sauce")
    
    expected_cart_count = 0
    
    for product in products:
        product_name = product["product_name"]
        inventory_page.click_add_to_cart(product_name)
        expected_cart_count += 1
        try:
            WebDriverWait(driver, 10).until(
                lambda d: inventory_page.get_num_of_items_in_cart() == expected_cart_count
            )  
        except TimeoutException:
            raise AssertionError(f"Cart item count after adding should be {expected_cart_count}, but got {inventory_page.get_num_of_items_in_cart()}")
        
    for product in products:
        product_name = product["product_name"]
        inventory_page.click_remove_from_cart(product_name)
        expected_cart_count -= 1
        if expected_cart_count > 0:
            try:
                WebDriverWait(driver, 10).until(
                    lambda d: inventory_page.get_num_of_items_in_cart() == expected_cart_count
                )  
            except TimeoutException:
                raise AssertionError(f"Cart item count after removing should be {expected_cart_count}, but got {inventory_page.get_num_of_items_in_cart()}")
        else:
            try:
                inventory_page.wait_for_element_not_visible(inventory_page.cart_item_count_locator)
            except AssertionError:
                raise AssertionError("Cart count still visible after removing all items. Expected it to be invisible.")