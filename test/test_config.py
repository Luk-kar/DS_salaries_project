'''
This module contains unit tests for verifying the configuration data of 
a web scraping project, including the validation of job titles, 
the number of jobs, URLs, driver paths, debug mode, NA value, and 
encoding values. 
The tests use the Config object obtained from get_config() method of 
scraper.config.get module. 
The unit tests check whether the configuration values are of 
the correct type and meet the required criteria.
'''

# Python
import os
import re
import unittest

# External
from pathvalidate import sanitize_filepath, sanitize_filename
import requests

# Internal
from scraper.config.get import (
    get_config,
    get_url,
    get_path_csv_raw,
    get_NA_value,
    get_encoding
)
from scraper.config._types import Config, JobNumber, JobSimilar, Url, Locations


class TestConfigData(unittest.TestCase):
    '''
    It tests the configuration data stored in Config
    object which is obtained from get_args method of scraper.config.get_config
    '''

    def setUp(self):
        '''init all config values'''
        self.config: Config = get_config()
        self.url = get_url(self.config['url'],
                           self.config['jobs_titles']['default'])

    def _assert_is_not_empty_string(self, string: str):
        '''assert if is it not an empty string'''

        self.assertIsInstance(string, str)
        self.assertNotEqual(string, "")

    def _is_valid_file_path(self, file_path: str) -> bool:
        '''
        Checks if the file path is valid and does not contain any illegal characters.
        '''

        # https://stackoverflow.com/a/67119769/12490791
        is_valid = file_path == sanitize_filepath(
            file_path, platform="auto")

        return is_valid

    def _is_valid_file_name(self, file_name: str) -> bool:
        '''
        Checks if the file path is valid and does not contain any illegal characters.
        '''
        is_valid = file_name == sanitize_filename(
            file_name, platform="universal")

        return is_valid

    def test_config_is_dict(self):
        '''assert if instance of a dict'''

        self.assertIsInstance(self.config, dict)

    def test_job_default(self):
        '''assert if is it not an empty string'''

        job_title = self.config['jobs_titles']['default']

        self._assert_is_not_empty_string(job_title)
        self.assertTrue(
            self._is_valid_file_name(job_title)
        )

    def test_jobs_similar(self):
        '''assert if is any of the jobs, not an empty string'''

        jobs: JobSimilar = self.config['jobs_titles']['similar']

        self.assertIsInstance(jobs, list)

        for job in jobs:
            self._assert_is_not_empty_string(job)
            self.assertTrue(
                self._is_valid_file_name(job)
            )

    def test_jobs_locations(self):
        '''assert if is any of the jobs, not an empty string'''

        locations: Locations = self.config['locations']

        default = locations['default']
        self.assertIsInstance(default, str)

        others = locations['others']
        self.assertIsInstance(others, list)

        for location in others:
            self._assert_is_not_empty_string(location)

    def test_jobs_number(self):
        '''test if is it greater than 0'''

        jobs_number: JobNumber = self.config['jobs_number']
        self.assertIsInstance(jobs_number, int)
        self.assertGreater(jobs_number, 0)
        self.assertLessEqual(jobs_number, 900)  # Glassdoor cap

    def test_url(self):
        '''test if are there url's types'''

        url: Url = self.config['url']
        self.assertIsInstance(url, dict)

        for part in url:
            self.assertIsInstance(part, str)

    def test_is_url_exists(self):
        '''check if url exists'''

        response = requests.get(self.url, timeout=10)

        code_not_exists = 404
        status_code = response.status_code

        # For some reasons you get 403: Forbidden. But the whole app works anyway.
        self.assertNotEqual(status_code, code_not_exists,
                            f"Not Found\nError - {status_code} : {response.reason}"
                            )

    def test_driver_path(self):
        '''check if the driver exists on the local machine'''

        path_file: str = self.config['driver_path']
        self._assert_is_not_empty_string(path_file)
        self.assertTrue(os.path.exists(path_file))
        self.assertTrue(os.path.isfile(path_file))

        is_Mac_Win_Linux_app = \
            path_file.endswith(".exe") or \
            re.search(".*[^a]$", path_file)  # no extension: Linux, Mac

        self.assertTrue(is_Mac_Win_Linux_app)

    def test_debug_mode(self):
        '''check an arg for verbose mode'''

        self.assertIsInstance(self.config['debug_mode'], bool)

    def test_na_value(self):
        '''check if NA is got'''

        self.assertIsNotNone(get_NA_value())

    def test_encoding_value(self):
        """check if not an empty string"""

        self._assert_is_not_empty_string(get_encoding())

    def test_output_path_raw(self):
        '''check correctness of path'''

        csv_raw_path = get_path_csv_raw()

        self.assertTrue(self._is_valid_file_path(csv_raw_path))


if __name__ == '__main__':
    unittest.main()
