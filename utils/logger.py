from lib import consts
from datetime import datetime
from contextlib import contextmanager
import json
import logging
import os
import pytest
import shutil


class Logger:
    def __init__(self, env):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_id = "RUN-" + self.timestamp
        self.env = env
        self.logger = None
        self.test_cases = {}

        self._setup_logger()

    @contextmanager
    def create_test_case(self, test_id: str):
        test_case = TestCase(self, test_id)
        self.test_cases[test_case.test_id] = test_case
        yield test_case

    def log_test_case(self, test_case):
        data = test_case.get_test_data()

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

        self._remove_test_case(test_case)

    def log_test_cases(self):
        for test_case in self.test_cases:
            self.log_test_case(test_case)

    def _remove_test_case(self, test_case):
        self.test_cases.pop(test_case.test_id)

    def _setup_logger(self):
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


class TestCase:
    """ TestCases that belong to a Logger """
    def __init__(self, logger: Logger, test_id: str):
        self.run_id = logger.run_id
        self.env = logger.env
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.test_id = test_id
        self.description = "undefined"
        self.log_level = "INFO"
        self.severity = "Medium"
        self.owner = "undefined"
        self.steps = []
        self.error = None
        self.status = "undefined"

    def set_description(self, desc: str):
        self.description = desc

    def set_severity(self, severity: str):
        self.severity = severity

    def set_owner(self, owner: str):
        self.owner = owner

    def set_status(self, passed: bool):
        self.status = "PASS" if passed else "FAIL"

    def add_step(self, step: str):
        self.steps.append(step)

    def add_error(self, test_report: pytest.TestReport):
        msg = str(test_report.longrepr.reprcrash.message)
        stack_trace = self._get_stack_trace(test_report)
        self.error = {
            "message": msg,
            "stacktrace": stack_trace
        }
        self.set_status(passed=False)
        self.log_level = "ERROR"
    
    def get_test_data(self):
        """ Returns Test Data as JSON"""
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

        json_test_data = json.dumps(test_data, indent=4)

        return json_test_data

    def _get_stack_trace(self, report: pytest.TestReport):
        lines = report.longrepr.reprtraceback.reprentries[0].lines
        return lines
