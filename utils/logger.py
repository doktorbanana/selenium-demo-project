"""
This file contains classes needed for Logging the tests.
"""
from lib import consts
from datetime import datetime
from contextlib import contextmanager
from enum import StrEnum
import json
import logging
import os
import pytest
import shutil


class Logger:
    """
    Create a Logger that is used for a testrun.
    It logs the data of each test case in JSON format.
    """
    def __init__(self, env):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_id = "RUN-" + self.timestamp
        self.env = env
        self.logger = None
        self.test_cases = {}

        self._setup_logger()

    @contextmanager
    def create_test_case(self, test_id: str):
        """
        Create a new test case and register it with this logger.
        """
        test_case = TestCase(self, test_id)
        self.test_cases[test_case.test_id] = test_case
        yield test_case

    def log_test_case(self, test_case):
        """
        Write test data of a given test case to logfile.
        """
        data = test_case.get_json_test_data()

        match test_case.log_level:
            case "DEBUG":
                self.logger.debug(data)
            case "INFO":
                self.logger.info(data)
            case "WARNING":
                self.logger.warning(data)
            case "ERROR":
                self.logger.error(data)
            case "CRITICAL":
                self.logger.critical(data)
            case _:
                ValueError(f"Unexpected Log Level: {data["log_level"]}")

    def log_test_cases(self):
        """
        Write test data of all registered test cases to logfile.
        """
        for test_case in self.test_cases.values():
            self.log_test_case(test_case)

    def remove_test_case(self, test_case):
        """
        Unregister test case.
        """
        self.test_cases.pop(test_case.test_id)

    def _setup_logger(self):
        """
        Create directories for logfile and clean up old log files.
        Create python logger and add JSON Formatter.
        """
        log_path = os.path.join("test_reports", "logs")
        if os.path.exists(log_path):
            shutil.rmtree(log_path)
        os.makedirs(log_path)

        log_file = os.path.join(log_path, f"{self.run_id}.log")

        logger = logging.getLogger(consts.LOGGER_NAME)
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            "%(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        self.logger = logger


class TestState(StrEnum):
    PASSED = "PASSED"
    BLOCKED = "BLOCKED"
    UNTESTED = "UNTESTED"
    RETEST = "RETEST"
    FAILED = "FAILED"


class TestCase:
    """ TestCases can be registered at a Logger """
    def __init__(self, logger: Logger, test_id: str):
        self.run_id = logger.run_id
        self.env = logger.env
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.test_id = test_id
        self.description = "undefined"
        self.log_level = "INFO"
        self.severity = "Medium"
        self.owner = "undefined"
        self.group = "undefined"
        self.steps = {}
        self.error = None
        self.status = "undefined"

    def set_description(self, desc: str):
        """
        Set the description of this test case.
        """
        self.description = desc

    def set_severity(self, severity: str):
        """
        Set the severity level of this test case.
        Should be "Low", "Medium", or "High."
        """
        self.severity = severity

    def set_owner(self, owner: str):
        """
        Set the owner of this test case.
        """
        self.owner = owner

    def set_status(self, status: TestState):
        """
        Set the status of this test case.
        """
        self.status = status

    def set_group(self, group: str):
        """ Set the suite or group a test belongs to"""
        self.group = group

    def start_step(self, number: int, desc: str):
        """
        Add a step for this test case.
        """
        self.steps[number] = {
            "descrpition": desc,
            "state": "started"}

    def mark_step_finished(self, number: int):
        """
        Mark a step as sucessfully finished.
        """
        self.steps[number]["state"] = "finished"

    def add_error(self, test_report: pytest.TestReport):
        """
        Add an error for this test case.
        Extracts the error-msg and stacktrace from a pytest-TestReport
        and adds it to the data of this test case.
        """
        msg = str(test_report.longrepr.reprcrash.message)
        stack_trace = self._get_stack_trace(test_report)
        self.error = {
            "message": msg,
            "stacktrace": stack_trace
        }
        self.set_status(TestState.FAILED)
        self.log_level = "ERROR"

    def get_json_test_data(self, indent=4, ascii=False):
        """
        Gets Test data in JSON format.
        """
        test_data = self._get_test_data()
        json_test_data = json.dumps(test_data,
                                    indent=indent,
                                    ensure_ascii=ascii)
        return json_test_data

    def _get_test_data(self):
        """
        Returns Test Data as JSON
        """
        test_data = {
            "test_id": self.test_id,
            "description": self.description,
            "metadata":
                {"run_id": self.run_id,
                 "severity": self.severity,
                 "owner": self.owner,
                 "env": self.env
                 },
            "steps": self.steps,
            "status": self.status
        }

        if self.error:
            test_data["error"] = self.error

        return test_data

    def _get_stack_trace(self, report: pytest.TestReport):
        """
        Extracts stacktrace from a pytest.TestReport
        """
        lines = report.longrepr.reprtraceback.reprentries[0].lines
        return lines
