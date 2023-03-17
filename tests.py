'''
This is a module for testing the configuration data of a web scraping project.
The module consists of two test classes: TestConfigData and TestJobDescription.
'''

# Python
import os
import csv
import re
import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import ConnectionError
from time import sleep

# External
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath, sanitize_filename
import requests
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

# Internal
from scraper.scraper import scrape_data
from scraper.jobs_to_csv.job_value_getter._element_value_getter import get_values_from_element
from scraper.jobs_to_csv.elements_query.XPATH_text_getter import get_XPATH_values
from scraper.jobs_to_csv.actions.pause import pause
from scraper.jobs_to_csv.elements_query.await_element import await_element
from scraper.jobs_to_csv.webpage_getter._driver_getter import get_driver, InvalidDriverPathError, MyService
from scraper.jobs_to_csv.webpage_getter.webpage_getter import get_webpage
from scraper.jobs_to_csv.job_value_getter._element_value_getter_and_adder import get_and_add_element_value
from scraper.jobs_to_csv.job_value_getter._dict_value_adder import add_values_to_job_from_dict
from scraper.jobs_to_csv.job_value_getter.job_value_getter import XpathSearch, XpathListSearch
from scraper.config.get import get_config, get_url, get_path_csv_raw, get_path_csv_clean, get_NA_value, get_encoding
from scraper.config._types import Config, JobNumber, JobSimilar, Url
from scraper._types import MyWebDriver, Job_elements


def decorator(func):
    def _decorator(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return _decorator


# class TestConfigData(unittest.TestCase):
#     '''
#     It tests the configuration data stored in Config
#     object which is obtained from get_args method of scraper.config.get_config
#     '''

#     def setUp(self):
#         '''init all config values'''
#         self.config: Config = get_config()
#         self.url = get_url(self.config['url'],
#                            self.config['jobs_titles']['default'])

#     def _is_empty_string(self, string: str):
#         '''assert if is it not an empty string'''

#         self.assertIsInstance(string, str)
#         self.assertNotEqual(string, "")

#     def _is_valid_file_path(self, file_path: str) -> bool:
#         '''
#         Checks if the file path is valid and does not contain any illegal characters.
#         '''

#         # https://stackoverflow.com/a/67119769/12490791
#         is_valid = file_path == sanitize_filepath(
#             file_path, platform="auto")

#         return is_valid

#     def _is_valid_file_name(self, file_name: str) -> bool:
#         '''
#         Checks if the file path is valid and does not contain any illegal characters.
#         '''
#         is_valid = file_name == sanitize_filename(
#             file_name, platform="universal")

#         return is_valid

#     def test_config_is_dict(self):
#         '''assert if instance of a dict'''

#         self.assertIsInstance(self.config, dict)

#     def test_job_default(self):
#         '''assert if is it not an empty string'''

#         job_title = self.config['jobs_titles']['default']

#         self._is_empty_string(job_title)
#         self.assertTrue(
#             self._is_valid_file_name(job_title)
#         )

#     def test_jobs_similar(self):
#         '''assert if is any of the jobs, not an empty string'''

#         jobs: JobSimilar = self.config['jobs_titles']['similar']

#         self.assertIsInstance(jobs, list)

#         for job in jobs:
#             self._is_empty_string(job)
#             self.assertTrue(
#                 self._is_valid_file_name(job)
#             )

#     def test_jobs_number(self):
#         '''test if is it greater than 0'''

#         jobs_number: JobNumber = self.config['jobs_number']
#         self.assertIsInstance(jobs_number, int)
#         self.assertGreater(jobs_number, 0)

#     def test_url(self):
#         '''test if are there url's types'''

#         url: Url = self.config['url']
#         self.assertIsInstance(url, dict)

#         for part in url:
#             self.assertIsInstance(part, str)

#     def test_is_url_exists(self):
#         '''check if url exists'''

#         def _get_answer(response):
#             '''Clear up the meaning of the response HTTP'''

#             status_code = response.status_code
#             return f" - {status_code} : {response.reason}"

#         response = requests.get(self.url, timeout=10)

#         NOT_EXISTS_code = 404
#         status_code = response.status_code

#         # For some reasons you get 403: Forbidden. But the whole app works anyway.
#         self.assertNotEqual(status_code, NOT_EXISTS_code,
#                             f"Not Found\nError{_get_answer(response)}"
#                             )

#     def test_driver_path(self):
#         '''check if the driver exists on the local machine'''

#         path_file: str = self.config['driver_path']
#         self._is_empty_string(path_file)
#         self.assertTrue(os.path.exists(path_file))
#         self.assertTrue(os.path.isfile(path_file))

#         is_Mac_Win_Linux_app = \
#             path_file.endswith(".exe") or \
#             re.search(".*[^a]$", path_file)  # no extension: Linux, Mac

#         self.assertTrue(is_Mac_Win_Linux_app)

#     def test_debug_mode(self):
#         '''check an arg for verbose mode'''

#         self.assertIsInstance(self.config['debug_mode'], bool)

#     def test_NA_value(self):
#         '''check if NA is got'''

#         self.config['NA_value']
#         self.assertIsNotNone(get_NA_value())

#     def test_encoding_value(self):
#         """check if not an empty string"""

#         self._is_empty_string(get_encoding())

#     def test_output_path_raw(self):
#         '''check correctness of path'''

#         csv_raw_path = get_path_csv_raw()

#         self.assertTrue(self._is_valid_file_path(csv_raw_path))

#     def test_output_path_clean(self):
#         '''check correctness of path'''

#         csv_clean_path = get_path_csv_clean()

#         self.assertTrue(self._is_valid_file_path(csv_clean_path))


# class TestWebDriver(unittest.TestCase):
#     '''It tests single-job page scraping'''

#     def setUp(self):
#         self.config: Config = get_config()
#         self.url = get_url(
#             self.config['url'],
#             self.config['jobs_titles']['default']
#         )
#         self.xpath_element = {
#             'search': '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsRating")]//div\
#                 //div[@class="ratingNum mr-sm"]',
#             'list': '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsHighlights")]/div'
#         }
#         self.html = MagicMock()

#     def _is_HTML(self, page_source):
#         return bool(BeautifulSoup(page_source, "html.parser").find())

#     def test_get_driver_with_debug_mode_true_and_valid_path(self):
#         driver = get_driver(debug_mode=True, path=self.config['driver_path'])
#         self.assertIsInstance(driver, MyWebDriver)

#     def test_get_driver_with_debug_mode_false_and_auto_install(self):
#         driver = get_driver(debug_mode=False, path="auto-install")
#         self.assertIsInstance(driver, MyWebDriver)

#     @patch('os.path.exists', return_value=False)
#     def test_get_driver_not_exists(self, mock_exists):

#         filepath = "C:\\valid_path\\non-existing-driver.exe"

#         with self.assertRaises(InvalidDriverPathError) as cm:
#             MyService(filepath)

#     @patch('os.path.exists', return_value=True)
#     def test_get_driver_with_invalid_file(self, mock_exists):

#         filepath = "C:\\valid_path\\chlomedrifer.exede"

#         with self.assertRaises(InvalidDriverPathError) as cm:
#             MyService(filepath)

#     @patch('os.path.exists', return_value=True)
#     @patch(
#         'scraper.jobs_to_csv.webpage_getter._driver_getter.MyService.__init__',
#         side_effect=WebDriverException('Invalid version')
#     )
#     def test_driver_version_mismatch(self, mock_exists, mock_init):
#         with self.assertRaises(SystemExit):
#             get_driver(path='/path/to/chromedriver')

#     def test_get_webpage_success(self):
#         driver: MyWebDriver = get_webpage(
#             "http://glassdoor.com", False)
#         page_source: str = driver.page_source

#         sleep(0.2)  # to load page

#         self.assertTrue(self._is_HTML(page_source))
#         self.assertIsInstance(driver, MyWebDriver)

#     def test_get_webpage_failure(self):

#         with self.assertRaises((ConnectionError, WebDriverException, SystemExit)):
#             get_webpage(debug_mode=False, url="http://glosduuuur.fi")

#     def _get_XpathSearch(self):

#         return XpathSearch(self.xpath_element['search'])

#     def _get_XpathListSearch(self):

#         return XpathListSearch(self.xpath_element['list'])

#     def test_XpathSearch(self):

#         xpath_search = self._get_XpathSearch()

#         self.assertEqual(xpath_search.element, self.xpath_element['search'])
#         self.assertEqual(xpath_search.value, get_NA_value())

#     def test_XpathListSearch(self):

#         xpath_search = self._get_XpathListSearch()

#         self.assertEqual(xpath_search.element, self.xpath_element['list'])
#         self.assertEqual(xpath_search.value, get_NA_value())

#     @patch('time.sleep', return_value=None)
#     @patch('random.uniform', return_value=0.1)
#     def test_pause(self, mock_uniform, mock_sleep):

#         pause()

#         mock_sleep.assert_called_once_with(0.1)

#     def test_await_element(self):
#         # Set up the test inputs
#         driver = MagicMock(spec=MyWebDriver)
#         timeout = 5
#         by = By.XPATH
#         element = "//div[@class='my-class']"

#         # Set up the mock return value for the find_element method
#         mock_element = MagicMock(spec=WebElement)
#         driver.find_element.return_value = mock_element

#         # Call the function being tested
#         result = await_element(driver, timeout, by, element)

#         # Make sure the find_element method was called with the correct arguments
#         driver.find_element.assert_called_once_with(by, element)

#         # Make sure the result is the same as the mock element returned by find_element
#         self.assertEqual(result, mock_element)

#     def test_add_values(self):

#         job_title = "Software Engineer - L9001"
#         company_name = "Initech Bros."
#         location = "Austin, Texas"
#         description = "We are looking for a young, passionate software engineer \
#             with 30+ years of experience in AppleScript and AI. We provide fresh fruits and \
#                 unlimited PTO as benefits."

#         job = {"Job_title": job_title, "Location": location}
#         values_to_add = {
#             "Description": XpathSearch(
#                 './/div[@class="jobDescriptionContent desc"]'
#             ),
#             "Company_name": XpathSearch(
#                 './/div[@data-test="employerName"]'
#             ),
#         }

#         # simulating a lot of logic...
#         values_to_add["Description"].value = description
#         values_to_add["Company_name"].value = company_name

#         add_values_to_job_from_dict(job, values_to_add)

#         expected_job = {
#             "Job_title": job_title,
#             "Location": location,
#             "Description": description,
#             "Company_name": company_name
#         }

#         self.assertDictEqual(job, expected_job)

#     def test_get_XPATH_values_with_single_element(self):

#         web_element = MagicMock(spec=WebElement)
#         web_element.find_element.return_value.text = 'Hello, Mom!'
#         search = XpathSearch('//div/p')
#         result = get_XPATH_values(web_element, search)

#         self.assertEqual(result, 'Hello, Mom!')

#     def test_get_XPATH_values_with_multiple_elements(self):

#         web_element = MagicMock(spec=WebElement)

#         mock_element_1 = MagicMock(spec=WebElement)
#         mock_element_1.text = "Hello"
#         mock_element_2 = MagicMock(spec=WebElement)
#         mock_element_2.text = "Mom!"

#         web_element.find_elements.return_value = [
#             mock_element_1,
#             mock_element_2
#         ]

#         search = XpathListSearch('//div/p')

#         result = get_XPATH_values(web_element, search)
#         self.assertEqual(result, ['Hello', 'Mom!'])

#     def test_raises_exception_with_invalid_html(self):
#         invalid_html = None
#         search = XpathSearch("//div")
#         with self.assertRaises(AttributeError):
#             get_XPATH_values(invalid_html, search)

#     def test_raises_exception_with_invalid_search(self):

#         mock_web_element = MagicMock()
#         mock_web_element.find_element.side_effect = NoSuchElementException(
#             "Element not found")

#         search = XpathSearch("//nonexistent_element")

#         with self.assertRaises(NoSuchElementException):
#             get_XPATH_values(mock_web_element, search)

#     def test_raises_exception_with_invalid_list_search(self):

#         mock_web_element = MagicMock()
#         mock_web_element.find_elements.side_effect = NoSuchElementException(
#             "Element not found")

#         search = XpathListSearch("//nonexistent_element")

#         with self.assertRaises(NoSuchElementException):
#             get_XPATH_values(mock_web_element, search)

#     def test_get_values_from_element_with_valid_values(self):

#         mock_element = MagicMock(spec=WebElement)

#         job_values: Job_elements = {
#             'Job_title': XpathSearch('.//div[@data-test="jobTitle"]'),
#             'Company_name': XpathSearch('.//div[@data-test="employerName"]'),
#             'Description': XpathSearch('.//div[@class="jobDescriptionContent desc"]'),
#             'Pros': XpathListSearch('.//*[text() = "Pros"]//parent::div//*[contains(name(), "p")]'),
#         }

#         values = {
#             'Job_title': "Assistant to the Regional Manager",
#             'Company_name': "Dunder Mifflin Paper Co.",
#             'Description': "The Yin to my Yang, the Bert to my Ernie, " +
#             "the Jim to my Dwight - are you ready to join the team at Dunder Mifflin Paper Co.?,",
#             'Pros': [
#                 "Dunder Mifflin Paper Co. is not just a company, " +
#                 "it's a way of life - from the quality of the paper " +
#                 "we produce to the community we build within the office," +
#                 "there's nowhere else I'd rather be.",

#                 "While working at Dunder Mifflin Paper Co." +
#                 "can be a bit of a drag at times, " +
#                 "it's the people, like Dwight, that make it all worth it" +
#                 "- that, and the endless supply of pranks I can pull on them."
#             ]
#         }

#         def my_side_effect_element(*args):

#             mock_element_return = MagicMock(spec=WebElement)

#             selector = args[1]

#             if selector == job_values['Job_title'].element:
#                 mock_element_return.text = values['Job_title']

#             elif selector == job_values['Company_name'].element:
#                 mock_element_return.text = values['Company_name']

#             elif selector == job_values['Description'].element:
#                 mock_element_return.text = values['Description']

#             else:
#                 raise KeyError

#             return mock_element_return

#         def my_side_effect_list(*args):

#             mock_return_elements = MagicMock(spec=list[WebElement])

#             selector = args[1]

#             if selector == job_values['Pros'].element:

#                 mock_element_01 = MagicMock(spec=WebElement)
#                 mock_element_02 = MagicMock(spec=WebElement)

#                 mock_element_01.text = values['Pros'][0]
#                 mock_element_02.text = values['Pros'][1]

#                 mock_return_elements = [
#                     mock_element_01,
#                     mock_element_02
#                 ]
#             else:
#                 raise KeyError

#             return mock_return_elements

#         mock_element.find_element.side_effect = my_side_effect_element
#         mock_element.find_elements.side_effect = my_side_effect_list

#         result = get_values_from_element(mock_element, job_values)

#         self.assertEqual(result['Job_title'].value, values['Job_title'])
#         self.assertEqual(result['Company_name'].value, values['Company_name'])
#         self.assertEqual(result['Description'].value, values['Description'])
#         self.assertEqual(result['Pros'].value, values['Pros'])

#         self.assertEqual(
#             mock_element.find_element.call_count +
#             mock_element.find_elements.call_count,
#             len(job_values)
#         )

#     def test_get_values_from_element_not_found(self):

#         mock_element = MagicMock(spec=WebElement)

#         job_elements = {
#             'Salary': XpathSearch("//nonexistent_element"),
#             'Cons': XpathListSearch("//nonexistent_element")
#         }

#         mock_element.find_element.side_effect = NoSuchElementException(
#             "Element not found")

#         mock_element.find_elements.side_effect = NoSuchElementException(
#             "Element not found")

#         job_values = get_values_from_element(
#             mock_element,
#             job_elements
#         )

#         self.assertEqual(
#             self.config['NA_value'],
#             job_values['Salary'].value
#         )
#         self.assertEqual(
#             self.config['NA_value'],
#             job_values['Cons'].value
#         )

#     def test_get_and_add_element_value(self):

#         job_dict_to_update = {
#             'Job_title': '',
#             'Location': '',
#             'Salary': '',
#             'Description': '',
#         }

#         job_values_to_add = {
#             'Job_title': "Theoretical Physicist",
#             'Company_name': "California Institute of Technology",
#             'Description': "Bazinga!",
#             'Cons': [
#                 "The cafeteria serves subpar food, which is a terrible insult" +
#                 "to my delicate palate and refined tastes.",
#                 "You'll have to suffer the indignity of occasionally being wrong, " +
#                 "which is something I never have to deal with."
#             ],
#         }

#         values_source_element = MagicMock(spec=WebElement)

#         job_elements = {
#             'Job_title': XpathSearch('.//div[@data-test="jobTitle"]'),
#             'Company_name': XpathSearch('.//div[@data-test="employerName"]'),
#             'Description': XpathSearch('.//div[@class="jobDescriptionContent desc"]'),
#             'Cons': XpathListSearch('.//*[text() = "Cons"]//parent::div//*[contains(name(), "p")]'),
#         }

#         def my_side_effect_element(*args):

#             mock_element_return = MagicMock(spec=WebElement)

#             selector = args[1]

#             if selector == job_elements['Job_title'].element:
#                 mock_element_return.text = job_values_to_add['Job_title']

#             elif selector == job_elements['Company_name'].element:
#                 mock_element_return.text = job_values_to_add['Company_name']

#             elif selector == job_elements['Description'].element:
#                 mock_element_return.text = job_values_to_add['Description']

#             else:
#                 raise KeyError

#             return mock_element_return

#         def my_side_effect_list(*args):

#             mock_return_elements = MagicMock(spec=list[WebElement])

#             selector = args[1]

#             if selector == job_elements['Cons'].element:

#                 mock_element_01 = MagicMock(spec=WebElement)
#                 mock_element_02 = MagicMock(spec=WebElement)

#                 mock_element_01.text = job_values_to_add['Cons'][0]
#                 mock_element_02.text = job_values_to_add['Cons'][1]

#                 mock_return_elements = [
#                     mock_element_01,
#                     mock_element_02
#                 ]
#             else:
#                 raise KeyError

#             return mock_return_elements

#         values_source_element.find_element.side_effect = my_side_effect_element
#         values_source_element.find_elements.side_effect = my_side_effect_list

#         get_and_add_element_value(
#             job_dict_to_update, values_source_element, job_elements)

#         self.assertEqual(
#             job_dict_to_update['Job_title'], job_values_to_add['Job_title'])
#         self.assertEqual(
#             job_dict_to_update['Company_name'], job_values_to_add['Company_name'])
#         self.assertEqual(
#             job_dict_to_update['Description'], job_values_to_add['Description'])
#         self.assertEqual(
#             job_dict_to_update['Cons'], job_values_to_add['Cons'])


regex = {
    # https://regex101.com/r/9m7gaB/1
    'Non-empty-string': r"^(?!\s*$).+",
    # https://regex101.com/r/XRho9L/1
    '0.0-5.0': r"^(?:[0-4](?:\.[0-9])?|5(?:\.0)?|)$",
    # https://regex101.com/r/TpN5H3/1
    '24h-30d+': r"^(?:24h|[1-2]?[0-9]d?|30d\+?)$",
    # https://regex101.com/r/9bIQDf/1
    'bool': r"^(True|False)$",
    # https://regex101.com/r/8TbXbC/1
    'employees': r"^(?!.*employees).*$",
    # https://regex101.com/r/g076Ht/1
    'exists': r"^.*$",
    # https://regex101.com/r/j32tP1/1
    '1-9999': r"^(?:[1-9]\d{0,3}|)$",
    # https://regex101.com/r/jVaJDa/1
    'Revenue_USD': r"^(?!.*\(USD\)).*$",
    # https://regex101.com/r/phTDbC/1
    '0.00-5.00': r"^(?:0(\.[0-9]{1,2})?|([1-4](\.[0-9]{1,2})?)|5(\.0{1,2})?|)$",
    # https://regex101.com/r/bGQCzp/1
    'reviews': r"^(\[((\'|\").*(\'|\")(, )?)+\]|)$"
}


class TestIntegration(unittest.TestCase):

    def setUp(self):
        '''init all config values'''
        self.jobs_number = 3
        self.csv = {
            'path': "data\RAW\Data_Engineer_06-03-2023_23-41.csv",
            'delimiter': ",",
            'encoding': get_encoding(),
            'expected_values': {
                'Company_name': regex["Non-empty-string"],
                'Rating': regex['0.0-5.0'],
                'Location': regex['Non-empty-string'],
                'Job_title': regex['Non-empty-string'],
                'Description': regex['Non-empty-string'],
                'Job_age': regex['24h-30d+'],
                'Easy_apply': regex['bool'],
                'Employees': regex['employees'],
                'Type_of_ownership': regex['exists'],
                'Sector': regex['exists'],
                'Founded': regex['1-9999'],
                'Industry': regex['exists'],
                'Revenue_USD': regex['Revenue_USD'],
                'Friend_recommend': regex['0.00-5.00'],
                'CEO_approval': regex['0.00-5.00'],
                'Career_opportunities': regex['0.0-5.0'],
                'Comp_&_benefits': regex['0.0-5.0'],
                'Culture_&_values': regex['0.0-5.0'],
                'Senior_management': regex['0.0-5.0'],
                'Work/Life_balance': regex['0.0-5.0'],
                'Pros': regex['reviews'],
                'Cons': regex['reviews'],
                'Benefits_rating': regex['0.0-5.0'],
            }
        }
        self.target_folder = os.path.dirname(get_path_csv_raw())
        self.target_directory_files_before = self._get_csv_files(
            self.target_folder)

    def _test_csv_file_structure(self):

        csv_file_path = self.csv['path']
        delimiter = self.csv['delimiter']
        expected_values = self.csv['expected_values']

        with open(csv_file_path, newline="", encoding=self.csv['encoding']) as file:

            reader = csv.reader(file, delimiter=delimiter)
            headers = next(reader)

            self._test_each_column(expected_values, reader, headers)

    def _test_each_column(self, expected_values, reader, headers):

        for i, row in enumerate(reader):

            self._test_each_field(expected_values, headers, i, row)

    def _test_each_field(self, expected_values, headers, i, row):

        for j, field in enumerate(row):
            header = headers[j]
            expected_regex = expected_values.get(header, None)

            if expected_regex is not None:
                assert re.match(
                    expected_regex, field), f"Invalid value in row {i+2}, column {j+1}:\
                        \nHeader :{header}:\nField  :{field}:\nExpect :{expected_regex}:"

    def _get_csv_files(self, directory: str) -> list[str]:

        csv_files = []

        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                csv_files.append(filename)

        return csv_files

    def test_in_debug_mode(self):

        with self.assertRaises(SystemExit):
            scrape_data(jobs_number=self.jobs_number, debug_mode=True)

        # self._test_csv_file_structure()

    def test_in_production(self):
        # scrape_data(jobs_number=self.jobs_number, debug_mode=False)
        # check the output
        pass

    def tearDown(self) -> None:

        target_folder = self.target_folder
        before_files = self.target_directory_files_before

        new_files = self._get_created_files()

        for filename in new_files:
            if filename not in before_files:
                new_file_path = os.path.join(target_folder, filename)
                os.remove(new_file_path)
                break

        return super().tearDown()

    def _get_created_files(self):

        target_folder = self.target_folder
        before_files = self.target_directory_files_before
        after_files = self._get_csv_files(target_folder)

        difference = set(after_files) - set(before_files)

        return difference


if __name__ == '__main__':
    unittest.main()
