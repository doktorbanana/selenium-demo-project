from lib import consts
from datetime import datetime
from contextlib import contextmanager
import json
import logging
import os
import traceback
import shutil


class Logger:
    def __init__(self, env):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_id = "RUN-" + self.timestamp
        self.env = env
        self.logger = None

        self._setup_logger()

    @contextmanager
    def get_test_case(self, test_id):
        """Context manager for test case logging"""
        test_data = {
            "test_id": test_id,
            "description": "undefined",
            "metadata":
                {"log_level": "INFO",
                 "run_id": self.run_id,
                 "severity": "undefined",
                 "owner": "undefined",
                 "env": self.env
                 },
            "steps": []
        }

        yield test_data

    def _log_test_case(self, test_case):

        json_data = json.dumps(test_case, indent=4)
        match test_case["metadata"]["log_level"]:
            case "DEBUG":
                self.logger.debug(json_data)
            case "INFO":
                self.logger.info(json_data)
            case "WARNING":
                self.logger.warning(json_data)
            case "ERROR":
                self.logger.error(json_data)
            case "CRITICAL":
                self.logger.critical(json_data)
            case _:
                ValueError(f"Unexpected Log Level: {test_case["log_level"]}")

    def _get_stack_trace(self, error):
        return traceback.format_exc()

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

    def close_test_case(self, test_case):
        self._log_test_case(test_case)
