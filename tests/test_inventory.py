"""
This file contains tests for the inventory page functionality.
It includes tests for clicking product images and links,
adding/removing products from the cart, and verifying cart item counts.
"""

from utils.data_loader import load_csv
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

products = load_csv("./test_data/products.csv")
custom_ids = [f"{row['custom_id']}" for row in products]


@pytest.mark.parametrize("product", products, ids=custom_ids)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
@pytest.mark.inventory
def test_img_click(standard_login, test_case_log, product):
    """Test clicking product images on the inventory page."""
    product_name = product["product_name"]

    test_case_log.set_description(
        "Testing to click on the image"
        f" of '{product_name}'."
        f" Expecting to get on the item page."
        )
    test_case_log.set_severity("Medium")
    test_case_log.set_owner("QA")
    test_case_log.set_group("Inventory")

    test_case_log.start_step(1, "Login and navigate to Inventory Page")
    inventory_page = standard_login
    test_case_log.mark_step_finished(1)

    test_case_log.start_step(2, "Click on product image")
    try:
        inventory_page.click_product_img(product_name)
    except RuntimeError as e:
        raise AssertionError(e)
    test_case_log.mark_step_finished(2)


@pytest.mark.parametrize("product", products, ids=custom_ids)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
@pytest.mark.inventory
def test_link_click(standard_login, test_case_log, product):
    """Test clicking product links on the inventory page."""
    product_name = product["product_name"]

    test_case_log.set_description(
        "Testing to click on the title"
        f" of '{product_name}'."
        f" Expecting to get on the item page."
    )
    test_case_log.set_severity("Medium")
    test_case_log.set_owner("QA")
    test_case_log.set_group("Inventory")

    test_case_log.start_step(1, "Login and navigating to Inventory Page")
    inventory_page = standard_login
    test_case_log.mark_step_finished(1)

    test_case_log.start_step(2, "Click on product title")
    try:
        inventory_page.click_product_link(product_name)
    except RuntimeError as e:
        raise AssertionError(e)
    test_case_log.mark_step_finished(2)


@pytest.mark.inventory
def test_cart_count(standard_login, test_case_log):
    """Test adding and removing products from the cart."""

    test_case_log.set_description(
        "Testing the counter badge of the cart"
    )
    test_case_log.set_severity("Medium")
    test_case_log.set_owner("QA")
    test_case_log.set_group("Inventory")

    test_case_log.start_step(1, "Login and navigate to Inventory Page")
    inventory_page = standard_login
    test_case_log.mark_step_finished(1)

    driver = inventory_page.driver
    expected_cart_count = 0

    for i, product in enumerate(products):
        product_name = product["product_name"]
        expected_cart_count += 1

        test_case_log.start_step(i+2,
                                 f"Adding {product_name} to cart"
                                 " Expecting cart count to be"
                                 f" {expected_cart_count}")
        inventory_page.click_add_to_cart(product_name)

        try:
            WebDriverWait(driver, inventory_page.timeout).until(
                lambda d:
                inventory_page.get_num_of_items_in_cart() ==
                expected_cart_count)
        except TimeoutException:
            raise AssertionError(
                f"Cart item count after adding should be"
                f"{expected_cart_count}, "
                f"but got "
                f"{inventory_page.get_num_of_items_in_cart()}")
        test_case_log.mark_step_finished(i+2)

    for i, product in enumerate(products):
        product_name = product["product_name"]
        expected_cart_count -= 1

        test_case_log.start_step(i + len(products) + 2,
                                 f"Removing {product_name} from cart."
                                 " Expecting cart cound to be"
                                 f" {expected_cart_count}")
        inventory_page.click_remove_from_cart(product_name)
        if expected_cart_count > 0:
            try:
                WebDriverWait(driver, inventory_page.timeout).until(
                    lambda d:
                    inventory_page.get_num_of_items_in_cart() ==
                    expected_cart_count)
            except TimeoutException:
                raise AssertionError(
                    f"Cart item count after removing should be "
                    f"{expected_cart_count}"
                    f" , but got "
                    f"{inventory_page.get_num_of_items_in_cart()}")
        else:
            try:
                inventory_page.wait_for_element_not_visible(
                    inventory_page.cart_item_count_locator)
            except TimeoutException:
                raise AssertionError("Cart count still visible after "
                                     "removing all items. "
                                     "Expected it to be invisible.")
        test_case_log.mark_step_finished(i + len(products) + 2)
