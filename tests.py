"""
This is a module for testing the configuration data of a web scraping project.
The module consists of two test classes: TestConfigData and TestJobDescription.
"""

# Python
import os
import re
import unittest

# External
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.webdriver import WebDriver

# Internal
from scraper.helpers.get_driver import get_driver
from scraper.helpers.get_webpage import get_webpage
from scraper.config.get import get_config, get_url
from scraper.config._types import Config, JobNumber, JobSimilar, Url
from scraper._types import WebElem


class TestConfigData(unittest.TestCase):
    """
    It tests the configuration data stored in Config 
    object which is obtained from get_args method of scraper.config.get_config
    """

    def setUp(self):
        """init all config values"""
        self.config: Config = get_config()
        self.url = get_url(self.config['url'],
                           self.config["jobs_titles"]["default"])

    def is_empty_string(self, string: str) -> None:
        """assert if is it not an empty string"""

        self.assertIsInstance(string, str)
        self.assertNotEqual(string, "")

    def test_config_is_dict(self):
        """assert if instance of a dict"""

        self.assertIsInstance(self.config, dict)

    def test_job_default(self):
        """assert if is it not an empty string"""

        self.is_empty_string(self.config["jobs_titles"]["default"])

    def test_jobs_similar(self):
        """assert if is any of the jobs, not an empty string"""

        jobs: JobSimilar = self.config["jobs_titles"]["similar"]

        self.assertIsInstance(jobs, list)

        for job in jobs:
            self.is_empty_string(job)

    def test_jobs_number(self):
        """test if is it greater than 0"""

        jobs_number: JobNumber = self.config["jobs_number"]
        self.assertIsInstance(jobs_number, int)
        self.assertGreater(jobs_number, 0)

    def test_url(self):
        """test if are there url's types"""

        url: Url = self.config["url"]
        self.assertIsInstance(url, dict)

        for part in url:
            self.assertIsInstance(part, str)

    def test_web_exists(self):
        """check if url exists"""

        status_code = requests.get(self.url, timeout=10).status_code
        self.assertEqual(status_code, 200)  # Response OK, server connected

    def test_driver_path(self):
        """check if the driver exists on the local machine"""

        path_file: str = self.config["driver_path"]
        self.is_empty_string(path_file)
        self.assertTrue(os.path.exists(path_file))
        self.assertTrue(os.path.isfile(path_file))

        is_Mac_Win_Linux_app = \
            path_file.endswith(".exe") or \
            re.search(".*[^a]$", path_file)  # no extension: Linux, Mac

        self.assertTrue(is_Mac_Win_Linux_app)

    def test_debug_mode(self):
        """check an arg for verbose mode"""

        self.assertIsInstance(self.config["debug_mode"], bool)

    def test_NA_value(self):
        """check if NA is a single valid value everywhere"""

        self.assertEqual(self.config["NA_value"], -1)


class TestJobDescription(unittest.TestCase):
    """It tests single-job page scraping"""

    def setUp(self):
        self.config: Config = get_config()
        self.url = get_url(self.config['url'],
                           self.config["jobs_titles"]["default"])

    def is_HTML(self, page_source):
        return bool(BeautifulSoup(page_source, "html.parser").find())

    def test_is_browser(self):
        driver: WebDriver = get_driver(self.url)

        self.assertIsInstance(
            driver, WebDriver)

    def test_is_webpage_loaded(self):
        driver: WebDriver = get_webpage(
            self.url, False)
        page_source: str = driver.page_source

        self.assertTrue(self.is_HTML(page_source))


if __name__ == '__main__':
    unittest.main()
