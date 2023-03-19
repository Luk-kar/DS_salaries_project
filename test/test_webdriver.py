'''
This module provides a custom WebDriver for automated testing purposes. 
The TestWebDriver class can be used to interact with web pages and 
perform various testing operations. 
It extends the functionality of the Selenium WebDriver to include 
additional features and options specific to our testing needs.
'''

# Python
import unittest
from time import sleep
from unittest.mock import MagicMock, patch
import requests

# External
from bs4 import BeautifulSoup
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper._types import Job_elements, MyWebDriver
from scraper.config._types import Config
from scraper.config.get import get_config, get_NA_value
from scraper.jobs_to_csv.actions.pause import pause
from scraper.jobs_to_csv.elements_query.await_element import await_element
from scraper.jobs_to_csv.elements_query.XPATH_text_getter import \
    get_XPATH_values
from scraper.jobs_to_csv.job_value_getter._dict_value_adder import \
    add_values_to_job_from_dict
from scraper.jobs_to_csv.job_value_getter._element_value_getter import \
    get_values_from_element
from scraper.jobs_to_csv.job_value_getter._element_value_getter_and_adder import \
    get_and_add_element_value
from scraper.jobs_to_csv.job_value_getter.job_value_getter import (
    XpathListSearch,
    XpathSearch
)
from scraper.jobs_to_csv.webpage_getter._driver_getter import (
    InvalidDriverPathError,
    MyService,
    get_driver
)
from scraper.jobs_to_csv.webpage_getter.webpage_getter import get_webpage


class TestWebDriver(unittest.TestCase):
    '''It tests webDriver class'''

    @classmethod
    def setUpClass(cls):
        cls.config: Config = get_config()

    def test_get_driver_with_debug_mode_true_and_valid_path(self):

        driver = get_driver(debug_mode=True, path=self.config['driver_path'])
        self.assertIsInstance(driver, MyWebDriver)

    def test_get_driver_with_debug_mode_false_and_auto_install(self):

        driver = get_driver(debug_mode=False, path="auto-install")
        self.assertIsInstance(driver, MyWebDriver)

    @patch('os.path.exists', return_value=False)
    def test_get_driver_not_exists(self, mock_exists):

        filepath = "C:\\valid_path\\non-existing-driver.exe"

        with self.assertRaises(InvalidDriverPathError):
            MyService(filepath)

    @patch('os.path.exists', return_value=True)
    def test_get_driver_with_invalid_file(self, mock_exists):

        filepath = "C:\\valid_path\\chlomedrifer.exede"

        with self.assertRaises(InvalidDriverPathError):
            MyService(filepath)

    @patch('os.path.exists', return_value=True)
    @patch(
        'scraper.jobs_to_csv.webpage_getter._driver_getter.MyService.__init__',
        side_effect=WebDriverException('Invalid version')
    )
    def test_driver_version_mismatch(self, mock_exists, mock_init):

        with self.assertRaises(SystemExit):
            get_driver(path='/path/to/chromedriver')


class TestWebAccess(unittest.TestCase):
    '''It tests web access behavior'''

    def test_get_webpage_success(self):
        driver: MyWebDriver = get_webpage(
            "http://glassdoor.com", False)
        page_source: str = driver.page_source

        sleep(0.4)  # to load page

        self.assertTrue(self._is_html(page_source))
        self.assertIsInstance(driver, MyWebDriver)

    def test_get_webpage_failure(self):

        with self.assertRaises((
            requests.exceptions.ConnectionError,
            WebDriverException,
            SystemExit
        )):
            get_webpage(debug_mode=False, url="http://glosduuuur.fi")

    def _is_html(self, page_source):

        return bool(BeautifulSoup(page_source, "html.parser").find())


class TestXpath(unittest.TestCase):
    '''It tests various HTML elements queries'''

    @classmethod
    def setUpClass(cls):
        cls.config: Config = get_config()
        cls.xpath_element = {
            'search':
            '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsRating")]//div//div[@class="ratingNum mr-sm"]',
            'list':
            '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsHighlights")]/div'
        }

    def test_XpathSearch(self):

        xpath_search = self._get_XpathSearch()

        self.assertEqual(xpath_search.element, self.xpath_element['search'])
        self.assertEqual(xpath_search.value, get_NA_value())

    def test_XpathListSearch(self):

        xpath_search = self._get_XpathListSearch()

        self.assertEqual(xpath_search.element, self.xpath_element['list'])
        self.assertEqual(xpath_search.value, get_NA_value())

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

    def test_get_XPATH_values_raises_exception_with_invalid_html(self):

        invalid_html = None
        search = XpathSearch("//div")
        with self.assertRaises(AttributeError):
            get_XPATH_values(invalid_html, search)

    def test_get_XPATH_values_raises_exception_with_invalid_search(self):

        mock_web_element = MagicMock()
        mock_web_element.find_element.side_effect = NoSuchElementException(
            "Element not found")

        search = XpathSearch("//nonexistent_element")

        with self.assertRaises(NoSuchElementException):
            get_XPATH_values(mock_web_element, search)

    def test_get_XPATH_values_raises_exception_with_invalid_list_search(self):

        mock_web_element = MagicMock()
        mock_web_element.find_elements.side_effect = NoSuchElementException(
            "Element not found")

        search = XpathListSearch("//nonexistent_element")

        with self.assertRaises(NoSuchElementException):
            get_XPATH_values(mock_web_element, search)

    def _get_XpathSearch(self):

        return XpathSearch(self.xpath_element['search'])

    def _get_XpathListSearch(self):

        return XpathListSearch(self.xpath_element['list'])


class TestElementQueries(unittest.TestCase):
    '''It tests various HTML elements queries'''

    def test_await_element(self):

        driver = MagicMock(spec=MyWebDriver)
        timeout = 5
        by = By.XPATH
        element = "//div[@class='my-class']"

        mock_element = MagicMock(spec=WebElement)
        driver.find_element.return_value = mock_element

        result = await_element(driver, timeout, by, element)

        driver.find_element.assert_called_once_with(by, element)

        self.assertEqual(result, mock_element)


class TestActions(unittest.TestCase):
    '''It tests web driver actions during the scraping'''

    @patch('time.sleep', return_value=None)
    @patch('random.uniform', return_value=0.1)
    def test_pause(self, mock_uniform, mock_sleep):

        pause()

        mock_sleep.assert_called_once_with(0.1)


class TestJobValueGetterFunctions(unittest.TestCase):
    '''
    A testing class for functions related to getting and adding job values.
    '''

    @classmethod
    def setUpClass(cls):

        cls.na_value = get_NA_value()

        cls.config: Config = get_config()
        cls.job_values = {
            'Job_title': "Theoretical Physicist",
            'Company_name': "Caltech",
            'Location': "Pasadena, California",
            'Description': "Bazinga!",
            'Salary': cls.na_value,
            'Cons': [
                "The cafeteria serves subpar food, which is a terrible insult" +
                "to my delicate palate and refined tastes.",
                "You'll have to suffer the indignity of occasionally being wrong, " +
                "which is something I never have to deal with."
            ],
            'Pros': [
                "The Physics Bowl Quiz (in 4 reviews)",
                "You can work with people with an IQ of 187, which puts it in the top 0.0001%% of the world's population (in 1 reviews)"
            ]
        }
        cls.selectors = {
            'Job_title': XpathSearch('.//div[@data-test="jobTitle"]'),
            'Company_name': XpathSearch('.//div[@data-test="employerName"]'),
            'Description': XpathSearch('.//div[@class="jobDescriptionContent desc"]'),
            'Pros': XpathListSearch('.//*[text() = "Pros"]//parent::div//*[contains(name(), "p")]'),
            'Salary': XpathSearch("//nonexistent_element"),
            'Cons': XpathListSearch("//nonexistent_element"),
        }

    def test_get_values_from_element_found(self):

        mock_element_found = MagicMock(spec=WebElement)

        xpath_selectors: Job_elements = {
            'Job_title': XpathSearch('.//div[@data-test="jobTitle"]'),
            'Company_name': XpathSearch('.//div[@data-test="employerName"]'),
            'Description': XpathSearch('.//div[@class="jobDescriptionContent desc"]'),
            'Pros': XpathListSearch('.//*[text() = "Pros"]//parent::div//*[contains(name(), "p")]'),
        }

        def mock_element_side_effect(*args):

            mock_element_return = MagicMock(spec=WebElement)

            selector = args[1]

            if selector == self.selectors['Job_title'].element:
                mock_element_return.text = self.job_values['Job_title']

            elif selector == self.selectors['Company_name'].element:
                mock_element_return.text = self.job_values['Company_name']

            elif selector == self.selectors['Description'].element:
                mock_element_return.text = self.job_values['Description']

            else:
                raise KeyError

            return mock_element_return

        def mock_list_side_effect(*args):

            mock_return_elements = MagicMock(spec=list[WebElement])

            selector = args[1]

            if selector == xpath_selectors['Pros'].element:

                mock_element_01 = MagicMock(spec=WebElement)
                mock_element_02 = MagicMock(spec=WebElement)

                mock_element_01.text = self.job_values['Pros'][0]
                mock_element_02.text = self.job_values['Pros'][1]

                mock_return_elements = [
                    mock_element_01,
                    mock_element_02
                ]
            else:
                raise KeyError

            return mock_return_elements

        mock_element_found.find_element.side_effect = mock_element_side_effect
        mock_element_found.find_elements.side_effect = mock_list_side_effect

        result = get_values_from_element(mock_element_found, xpath_selectors)

        self.assertEqual(result['Job_title'].value,
                         self.job_values['Job_title'])
        self.assertEqual(result['Company_name'].value,
                         self.job_values['Company_name'])
        self.assertEqual(result['Description'].value,
                         self.job_values['Description'])
        self.assertEqual(result['Pros'].value, self.job_values['Pros'])

        self.assertEqual(
            mock_element_found.find_element.call_count +
            mock_element_found.find_elements.call_count,
            len(xpath_selectors)
        )

    def test_get_values_from_element_not_found(self):

        mock_element_not_found = MagicMock(spec=WebElement)

        job_elements = {
            'Salary': XpathSearch("//nonexistent_element"),
            'Cons': XpathListSearch("//nonexistent_element")
        }

        mock_element_not_found.find_element.side_effect = NoSuchElementException(
            "Element not found")

        mock_element_not_found.find_elements.side_effect = NoSuchElementException(
            "Element not found")

        job_values = get_values_from_element(
            mock_element_not_found,
            job_elements
        )

        self.assertEqual(
            self.na_value,
            job_values['Salary'].value
        )
        self.assertEqual(
            self.na_value,
            job_values['Cons'].value
        )

    def test_add_values(self):

        job_values = {
            "Job_title": self.job_values['Job_title'],
            "Location": self.job_values['Location']
        }
        values_to_add = {
            "Description": XpathSearch(
                './/div[@class="jobDescriptionContent desc"]'
            ),
            "Company_name": XpathSearch(
                './/div[@data-test="employerName"]'
            ),
        }

        # simulating a lot of logic...

        values_to_add["Description"].value = self.job_values['Description']
        values_to_add["Company_name"].value = self.job_values['Company_name']

        add_values_to_job_from_dict(job_values, values_to_add)

        expected_job = {
            "Job_title": self.job_values['Job_title'],
            "Location": self.job_values['Location'],
            "Description": self.job_values['Description'],
            "Company_name": self.job_values['Company_name']
        }

        self.assertDictEqual(job_values, expected_job)

    def test_get_and_add_element_value(self):

        job_dict_to_update = {
            'Job_title': '',
            'Location': '',
            'Salary': '',
            'Description': '',
        }

        values_source_element = MagicMock(spec=WebElement)

        job_elements = {
            'Job_title': XpathSearch('.//div[@data-test="jobTitle"]'),
            'Company_name': XpathSearch('.//div[@data-test="employerName"]'),
            'Description': XpathSearch('.//div[@class="jobDescriptionContent desc"]'),
            'Cons': XpathListSearch('.//*[text() = "Cons"]//parent::div//*[contains(name(), "p")]'),
        }

        def my_side_effect_element(*args):

            mock_element_return = MagicMock(spec=WebElement)

            selector = args[1]

            if selector == job_elements['Job_title'].element:
                mock_element_return.text = self.job_values['Job_title']

            elif selector == job_elements['Company_name'].element:
                mock_element_return.text = self.job_values['Company_name']

            elif selector == job_elements['Description'].element:
                mock_element_return.text = self.job_values['Description']

            else:
                raise KeyError

            return mock_element_return

        def my_side_effect_list(*args):

            mock_return_elements = MagicMock(spec=list[WebElement])

            selector = args[1]

            if selector == job_elements['Cons'].element:

                mock_element_01 = MagicMock(spec=WebElement)
                mock_element_02 = MagicMock(spec=WebElement)

                mock_element_01.text = self.job_values['Cons'][0]
                mock_element_02.text = self.job_values['Cons'][1]

                mock_return_elements = [
                    mock_element_01,
                    mock_element_02
                ]
            else:
                raise KeyError

            return mock_return_elements

        values_source_element.find_element.side_effect = my_side_effect_element
        values_source_element.find_elements.side_effect = my_side_effect_list

        get_and_add_element_value(
            job_dict_to_update, values_source_element, job_elements
        )

        self.assertEqual(
            job_dict_to_update['Job_title'], self.job_values['Job_title'])
        self.assertEqual(
            job_dict_to_update['Company_name'], self.job_values['Company_name'])
        self.assertEqual(
            job_dict_to_update['Description'], self.job_values['Description'])
        self.assertEqual(
            job_dict_to_update['Cons'], self.job_values['Cons'])
