"""
This module provides a factory class to create WebDriver
instances for different browsers.
It supports both local and remote WebDriver instances."
"""

from selenium import webdriver


class DriverFactory:
    """
    Factory class to create WebDriver instances for different browsers.
    It supports both local and remote WebDriver instances.
    """

    @staticmethod
    def create_driver(browser_name, remote):
        """
        Create a WebDriver instance for the specified browser.
        If remote is True, it creates a remote WebDriver instance.
        """
        options = DriverFactory._create_browser_options(browser_name)

        if remote:
            return DriverFactory._create_remote_driver(options)
        else:
            return DriverFactory._create_local_driver(options, browser_name)

    @staticmethod
    def _create_browser_options(browser_name):
        """
        Create browser options based on the specified browser.
        """
        if browser_name.lower() == "chrome":
            return DriverFactory._create_chrome_options()
        elif browser_name.lower() == "firefox":
            return DriverFactory._create_firefox_options()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

    @staticmethod
    def _create_chrome_options():
        """
        Create Chrome options for the browser.
        """
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.password_manager_leak_detection": False}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable-features=PasswordLeakToggleMove")
        options.add_argument("--headless=new")
        return options

    @staticmethod
    def _create_firefox_options():
        """
        Create Firefox options for the browser.
        """
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        return options

    @staticmethod
    def _create_local_driver(options, browser_name):
        """
        Create a local WebDriver instance for the specified browser.
        """
        if browser_name.lower() == "chrome":
            return webdriver.Chrome(options=options)
        elif browser_name.lower() == "firefox":
            return webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

    @staticmethod
    def _create_remote_driver(options):
        """
        Create a remote WebDriver instance for the specified browser.
        """
        grid_url = "http://localhost:4444/wd/hub"
        return webdriver.Remote(command_executor=grid_url, options=options)
