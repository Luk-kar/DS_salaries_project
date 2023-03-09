'''
This is a module for testing the configuration data of a web scraping project.
The module consists of two test classes: TestConfigData and TestJobDescription.
'''

# Python
import os
import re
import unittest
from unittest.mock import patch, MagicMock, Mock

# External
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath, sanitize_filename
import requests
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

# Internal
from scraper.jobs_to_csv.elements_query.XPATH_text_getter import get_XPATH_values
from scraper.jobs_to_csv.actions.pause import pause
from scraper.jobs_to_csv.elements_query.await_element import await_element
from scraper.jobs_to_csv.webpage_getter._driver_getter import get_driver
from scraper.jobs_to_csv.webpage_getter.webpage_getter import get_webpage
from scraper.config.get import get_config, get_url, get_path_csv_raw, get_path_csv_clean, get_NA_value, get_encoding
from scraper.jobs_to_csv.job_value_getter._dict_value_adder import add_values_to_job_from_dict
from scraper.config._types import Config, JobNumber, JobSimilar, Url
from scraper._types import MyWebDriver
from scraper.jobs_to_csv.job_value_getter.job_value_getter import XpathSearch, XpathListSearch


def decorator(func):
    def _decorator(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return _decorator


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

    def _is_empty_string(self, string: str):
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

        self._is_empty_string(job_title)
        self.assertTrue(
            self._is_valid_file_name(job_title)
        )

    def test_jobs_similar(self):
        '''assert if is any of the jobs, not an empty string'''

        jobs: JobSimilar = self.config['jobs_titles']['similar']

        self.assertIsInstance(jobs, list)

        for job in jobs:
            self._is_empty_string(job)
            self.assertTrue(
                self._is_valid_file_name(job)
            )

    def test_jobs_number(self):
        '''test if is it greater than 0'''

        jobs_number: JobNumber = self.config['jobs_number']
        self.assertIsInstance(jobs_number, int)
        self.assertGreater(jobs_number, 0)

    def test_url(self):
        '''test if are there url's types'''

        url: Url = self.config['url']
        self.assertIsInstance(url, dict)

        for part in url:
            self.assertIsInstance(part, str)

    def test_web_exists(self):
        '''check if url exists'''

        response = requests.get(self.url, timeout=10)
        OK_status_code = 200
        status_code = response.status_code

        self.assertEqual(status_code, OK_status_code,
                         f"OK\nError - {status_code} : {response.reason}")

    def test_driver_path(self):
        '''check if the driver exists on the local machine'''

        path_file: str = self.config['driver_path']
        self._is_empty_string(path_file)
        self.assertTrue(os.path.exists(path_file))
        self.assertTrue(os.path.isfile(path_file))

        is_Mac_Win_Linux_app = \
            path_file.endswith(".exe") or \
            re.search(".*[^a]$", path_file)  # no extension: Linux, Mac

        self.assertTrue(is_Mac_Win_Linux_app)

    def test_debug_mode(self):
        '''check an arg for verbose mode'''

        self.assertIsInstance(self.config['debug_mode'], bool)

    def test_NA_value(self):
        '''check if NA is got'''

        self.config['NA_value']
        self.assertIsNotNone(get_NA_value())
        # Checks also KeyError:

    def test_encoding_value(self):
        """check if not an empty string"""

        self._is_empty_string(get_encoding())

    def test_output_path_raw(self):
        '''check correctness of path'''

        csv_raw_path = get_path_csv_raw()

        self.assertTrue(self._is_valid_file_path(csv_raw_path))

    def test_output_path_clean(self):
        '''check correctness of path'''

        csv_clean_path = get_path_csv_clean()

        self.assertTrue(self._is_valid_file_path(csv_clean_path))


class TestWebDriver(unittest.TestCase):
    '''It tests single-job page scraping'''

    def setUp(self):
        self.config: Config = get_config()
        self.url = get_url(
            self.config['url'],
            self.config['jobs_titles']['default']
        )
        self.xpath_element = {
            'search': '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsRating")]//div\
                //div[@class="ratingNum mr-sm"]',
            'list': '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsHighlights")]/div'
        }

    def _is_HTML(self, page_source):
        return bool(BeautifulSoup(page_source, "html.parser").find())

    def test_is_browser(self):
        driver: MyWebDriver = get_driver(self.url)

        self.assertIsInstance(
            driver, MyWebDriver)

    def test_is_webpage_loaded(self):
        driver: MyWebDriver = get_webpage(
            self.url, False)
        page_source: str = driver.page_source

        self.assertTrue(self._is_HTML(page_source))

    def _get_XpathSearch(self):

        return XpathSearch(self.xpath_element['search'])

    def _get_XpathListSearch(self):

        return XpathListSearch(self.xpath_element['list'])

    def test_XpathSearch(self):

        xpath_search = self._get_XpathSearch()

        self.assertEqual(xpath_search.element, self.xpath_element['search'])
        self.assertEqual(xpath_search.value, get_NA_value())

    def test_XpathListSearch(self):

        xpath_search = self._get_XpathListSearch()

        self.assertEqual(xpath_search.element, self.xpath_element['list'])
        self.assertEqual(xpath_search.value, get_NA_value())

    @patch('time.sleep', return_value=None)
    @patch('random.uniform', return_value=0.1)
    def test_pause(self, mock_uniform, mock_sleep):

        pause()

        mock_sleep.assert_called_once_with(0.1)

    def test_await_element(self):
        # Set up the test inputs
        driver = MagicMock(spec=MyWebDriver)
        timeout = 5
        by = By.XPATH
        element = "//div[@class='my-class']"

        # Set up the mock return value for the find_element method
        mock_element = MagicMock(spec=WebElement)
        driver.find_element.return_value = mock_element

        # Call the function being tested
        result = await_element(driver, timeout, by, element)

        # Make sure the find_element method was called with the correct arguments
        driver.find_element.assert_called_once_with(by, element)

        # Make sure the result is the same as the mock element returned by find_element
        self.assertEqual(result, mock_element)

    def test_add_values(self):

        job_title = "L9001 Software Engineer"
        company_name = "Initech Bros."
        location = "Austin, Texas"
        description = "We are looking for a young, passionate software engineer \
            with 30+ years of experience in AppleScript and AI. We provide fresh fruits and \
                unlimited PTO as benefits."

        job = {"Job_title": job_title, "Location": location}
        values_to_add = {
            "Description": XpathSearch(
                './/div[@class="jobDescriptionContent desc"]'
            ),
            "Company_name": XpathSearch(
                './/div[@data-test="employerName"]'
            ),
        }

        # simulating a lot of logic...
        values_to_add["Description"].value = description
        values_to_add["Company_name"].value = company_name

        add_values_to_job_from_dict(job, values_to_add)

        expected_job = {
            "Job_title": job_title,
            "Location": location,
            "Description": description,
            "Company_name": company_name
        }

        self.assertDictEqual(job, expected_job)

    def test_get_XPATH_values_with_single_element(self):

        web_element = MagicMock(spec=WebElement)
        web_element.find_element.return_value.text = 'Hello, Mom!'
        search = XpathSearch('//div/p')
        result = get_XPATH_values(web_element, search)

        self.assertEqual(result, 'Hello, Mom!')

    def test_get_XPATH_values_with_multiple_elements(self):

        web_element = MagicMock(spec=WebElement)

        mock_element_1 = MagicMock(spec=WebElement)
        mock_element_1.text = "Hello"
        mock_element_2 = MagicMock(spec=WebElement)
        mock_element_2.text = "Mom!"

        web_element.find_elements.return_value = [
            mock_element_1,
            mock_element_2
        ]

        search = XpathListSearch('//div/p')

        result = get_XPATH_values(web_element, search)
        self.assertEqual(result, ['Hello', 'Mom!'])

    def test_get_XPATH_values_with_missing_element(self):

        mock_element = MagicMock(spec=WebElement)
        mock_element.find_element.return_value = None  # todo raise exception
        search = XpathSearch('//div/p')
        result = get_XPATH_values(mock_element, search)

        self.assertEqual(result, 'NA_value')

    def test_get_XPATH_values_with_missing_elements(self):
        mock_element = Mock()
        mock_element.find_elements.return_value = []  # todo raise exception
        search = XpathListSearch('//div/p')
        result = get_XPATH_values(mock_element, search)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
