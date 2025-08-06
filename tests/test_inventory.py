from pages.login_page import LoginPage
import pytest


@pytest.mark.parametrize("product_name", [
    ("Sauce Labs Backpack"),        # Backpack
])

def test_img_click(setup_browser, product_name):
    driver = setup_browser
    driver.get("https://saucedemo.com")
    
    login_page = LoginPage(driver)
    inventory_page = login_page.login_expect_success("standard_user", "secret_sauce")
    item_page = inventory_page.click_product_img(product_name)

    assert item_page.url_contains("item.html"), "Clicking product image did not redirect to item page"