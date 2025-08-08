from pages.login_page import LoginPage
import pytest


def test_intentionally_fail(setup_browser, request):
    if not request.config.getoption("--intentionally-fail"):
        pytest.skip(reason="This test only runs with "
                    "--intentionally-fail option. "
                    "It is intentionally failing for demonstration purposes.")

    driver = setup_browser
    driver.get("https://saucedemo.com")
    login_page = LoginPage(driver)
    inventory_page = login_page.login_expect_success(
        "standard_user",
        "secret_sauce")

    error_msg = "This test is intentionally failing " \
                "for demonstration purposes. " \
                f"We expect to be on the {inventory_page.title} when it fails."

    assert False, error_msg
