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
from selenium.common.exceptions import (NoSuchElementException,
                                        WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper._types import Job_elements, MyWebDriver
from scraper.config._types import Config
from scraper.config.get import get_config, get_NA_value, get_url
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


class TestDriver(unittest.TestCase):
    '''It tests single-job page scraping'''

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


class TestWebDriver(unittest.TestCase):
    '''It tests single-job page scraping'''

    @classmethod
    def setUpClass(cls):
        cls.config: Config = get_config()
        cls.url = get_url(
            cls.config['url'],
            cls.config['jobs_titles']['default']
        )
        cls.xpath_element = {
            'search': '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsRating")]//div\
                //div[@class="ratingNum mr-sm"]',
            'list': '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsHighlights")]/div'
        }
        cls.html = MagicMock()

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

        driver = MagicMock(spec=MyWebDriver)
        timeout = 5
        by = By.XPATH
        element = "//div[@class='my-class']"

        mock_element = MagicMock(spec=WebElement)
        driver.find_element.return_value = mock_element

        result = await_element(driver, timeout, by, element)

        driver.find_element.assert_called_once_with(by, element)

        self.assertEqual(result, mock_element)

    def test_add_values(self):

        job_title = "Software Engineer - L9001"
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

    def test_raises_exception_with_invalid_html(self):

        invalid_html = None
        search = XpathSearch("//div")
        with self.assertRaises(AttributeError):
            get_XPATH_values(invalid_html, search)

    def test_raises_exception_with_invalid_search(self):

        mock_web_element = MagicMock()
        mock_web_element.find_element.side_effect = NoSuchElementException(
            "Element not found")

        search = XpathSearch("//nonexistent_element")

        with self.assertRaises(NoSuchElementException):
            get_XPATH_values(mock_web_element, search)

    def test_raises_exception_with_invalid_list_search(self):

        mock_web_element = MagicMock()
        mock_web_element.find_elements.side_effect = NoSuchElementException(
            "Element not found")

        search = XpathListSearch("//nonexistent_element")

        with self.assertRaises(NoSuchElementException):
            get_XPATH_values(mock_web_element, search)

    def test_get_values_from_element_with_valid_values(self):

        mock_element = MagicMock(spec=WebElement)

        job_values: Job_elements = {
            'Job_title': XpathSearch('.//div[@data-test="jobTitle"]'),
            'Company_name': XpathSearch('.//div[@data-test="employerName"]'),
            'Description': XpathSearch('.//div[@class="jobDescriptionContent desc"]'),
            'Pros': XpathListSearch('.//*[text() = "Pros"]//parent::div//*[contains(name(), "p")]'),
        }

        values = {
            'Job_title': "Assistant to the Regional Manager",
            'Company_name': "Dunder Mifflin Paper Co.",
            'Description': "The Yin to my Yang, the Bert to my Ernie, " +
            "the Jim to my Dwight - are you ready to join the team at Dunder Mifflin Paper Co.?,",
            'Pros': [
                "Dunder Mifflin Paper Co. is not just a company, " +
                "it's a way of life - from the quality of the paper " +
                "we produce to the community we build within the office," +
                "there's nowhere else I'd rather be.",

                "While working at Dunder Mifflin Paper Co." +
                "can be a bit of a drag at times, " +
                "it's the people, like Dwight, that make it all worth it" +
                "- that, and the endless supply of pranks I can pull on them."
            ]
        }

        def my_side_effect_element(*args):

            mock_element_return = MagicMock(spec=WebElement)

            selector = args[1]

            if selector == job_values['Job_title'].element:
                mock_element_return.text = values['Job_title']

            elif selector == job_values['Company_name'].element:
                mock_element_return.text = values['Company_name']

            elif selector == job_values['Description'].element:
                mock_element_return.text = values['Description']

            else:
                raise KeyError

            return mock_element_return

        def my_side_effect_list(*args):

            mock_return_elements = MagicMock(spec=list[WebElement])

            selector = args[1]

            if selector == job_values['Pros'].element:

                mock_element_01 = MagicMock(spec=WebElement)
                mock_element_02 = MagicMock(spec=WebElement)

                mock_element_01.text = values['Pros'][0]
                mock_element_02.text = values['Pros'][1]

                mock_return_elements = [
                    mock_element_01,
                    mock_element_02
                ]
            else:
                raise KeyError

            return mock_return_elements

        mock_element.find_element.side_effect = my_side_effect_element
        mock_element.find_elements.side_effect = my_side_effect_list

        result = get_values_from_element(mock_element, job_values)

        self.assertEqual(result['Job_title'].value, values['Job_title'])
        self.assertEqual(result['Company_name'].value, values['Company_name'])
        self.assertEqual(result['Description'].value, values['Description'])
        self.assertEqual(result['Pros'].value, values['Pros'])

        self.assertEqual(
            mock_element.find_element.call_count +
            mock_element.find_elements.call_count,
            len(job_values)
        )

    def test_get_values_from_element_not_found(self):

        mock_element = MagicMock(spec=WebElement)

        job_elements = {
            'Salary': XpathSearch("//nonexistent_element"),
            'Cons': XpathListSearch("//nonexistent_element")
        }

        mock_element.find_element.side_effect = NoSuchElementException(
            "Element not found")

        mock_element.find_elements.side_effect = NoSuchElementException(
            "Element not found")

        job_values = get_values_from_element(
            mock_element,
            job_elements
        )

        self.assertEqual(
            self.config['NA_value'],
            job_values['Salary'].value
        )
        self.assertEqual(
            self.config['NA_value'],
            job_values['Cons'].value
        )

    def test_get_and_add_element_value(self):

        job_dict_to_update = {
            'Job_title': '',
            'Location': '',
            'Salary': '',
            'Description': '',
        }

        job_values_to_add = {
            'Job_title': "Theoretical Physicist",
            'Company_name': "California Institute of Technology",
            'Description': "Bazinga!",
            'Cons': [
                "The cafeteria serves subpar food, which is a terrible insult" +
                "to my delicate palate and refined tastes.",
                "You'll have to suffer the indignity of occasionally being wrong, " +
                "which is something I never have to deal with."
            ],
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
                mock_element_return.text = job_values_to_add['Job_title']

            elif selector == job_elements['Company_name'].element:
                mock_element_return.text = job_values_to_add['Company_name']

            elif selector == job_elements['Description'].element:
                mock_element_return.text = job_values_to_add['Description']

            else:
                raise KeyError

            return mock_element_return

        def my_side_effect_list(*args):

            mock_return_elements = MagicMock(spec=list[WebElement])

            selector = args[1]

            if selector == job_elements['Cons'].element:

                mock_element_01 = MagicMock(spec=WebElement)
                mock_element_02 = MagicMock(spec=WebElement)

                mock_element_01.text = job_values_to_add['Cons'][0]
                mock_element_02.text = job_values_to_add['Cons'][1]

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
            job_dict_to_update['Job_title'], job_values_to_add['Job_title'])
        self.assertEqual(
            job_dict_to_update['Company_name'], job_values_to_add['Company_name'])
        self.assertEqual(
            job_dict_to_update['Description'], job_values_to_add['Description'])
        self.assertEqual(
            job_dict_to_update['Cons'], job_values_to_add['Cons'])

    def _is_html(self, page_source):

        return bool(BeautifulSoup(page_source, "html.parser").find())

    def _get_XpathSearch(self):

        return XpathSearch(self.xpath_element['search'])

    def _get_XpathListSearch(self):

        return XpathListSearch(self.xpath_element['list'])
