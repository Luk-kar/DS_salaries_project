"""
This is a module for testing the configuration data of a web scraping project.
The module consists of two test classes: TestConfigData and TestJobDescription.
"""

# Python
import os
import re
import unittest

# Imported
import requests

# Internal
from config.get_config import get_args
from config.Types import Config, Job_Number, Job_Similar, Url


class TestConfigData(unittest.TestCase):
    """
    It tests the configuration data stored in Config 
    object which is obtained from get_args method of config.get_config
    """

    def setUp(self):
        """init common variables"""
        self.config: Config = get_args()

    def is_empty_string(self, string: str) -> None:
        """assert if is it not an empty string"""

        self.assertIsInstance(string, str)
        self.assertNotEqual(string, "")

    def test_args_is_dict(self):
        """assert if instance of a dict"""

        self.assertIsInstance(self.config, dict)

    def test_job_default(self):
        """assert if is it not an empty string"""

        self.is_empty_string(self.config["jobs_titles"]["default"])

    def test_jobs_similar(self):
        """assert if is any of the jobs, not an empty string"""

        jobs: Job_Similar = self.config["jobs_titles"]["similar"]

        self.assertIsInstance(jobs, list)

        for job in jobs:
            self.is_empty_string(job)

    def test_jobs_number(self):
        """test if is it greater than 0"""

        jobs_number: Job_Number = self.config["jobs_number"]
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

        url: Url = self.config["url"]
        job: str = self.config["jobs_titles"]["default"]

        web = url["001_base"] + job + \
            url["002_keyword"] + job + \
            url["003_location"]

        status_code = requests.get(web, timeout=10).status_code
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


class TestJobDescription(unittest.TestCase):
    """It tests single-job page scraping"""

    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
