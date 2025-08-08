from pages.login_page import LoginPage
from utils.data_loader import load_csv
import pytest

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