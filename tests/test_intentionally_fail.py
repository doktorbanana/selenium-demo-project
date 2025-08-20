"""
This file contains a test that is intentionally designed to fail.
It is used for demonstration purposes and will only run when the
--intentionally-fail option is set.
"""

import pytest
from utils.logger import TestState


@pytest.mark.intfail
def test_intentionally_fail(standard_login, test_case_log, request):
    """
    This test is intentionally failing for demonstration purposes.
    It is designed to fail when the --intentionally-fail option is not set.
    """
    test_case_log.set_description(
        "This test intentionally fails."
        " It's used to demonstrate how failing tests are handled."
        )
    test_case_log.set_severity("Low")
    test_case_log.set_owner("QA")
    test_case_log.set_group("Intentional Fail")

    if not request.config.getoption("--intentionally-fail"):
        test_case_log.set_status(TestState.UNTESTED)
        pytest.skip(reason="This test only runs with "
                    "--intentionally-fail option. "
                    "It is intentionally failing for demonstration purposes.")

    test_case_log.start_step(1, "Login and navigate to Inventory Page")
    inventory_page = standard_login
    test_case_log.mark_step_finished(1)

    test_case_log.start_step(2, "Do something bad!")
    error_msg = (
        "This test is intentionally failing "
        "for demonstration purposes. "
        f"We expect to be on the {inventory_page.driver.title}"
        " page when it fails."
    )

    assert False, error_msg
