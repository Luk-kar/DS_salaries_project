'''
This module contains functions for web scraping of job listings from Glassdoor. 
It uses Selenium for web automation.
It also contains functions for writing job data to CSV files in its RAW version.
'''
# Python
import logging
import sys
from typing import Literal

# External
import enlighten
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper._types import Job_values, MyWebDriver, WebElements
from scraper.config._types import DebugMode, JobNumber, JobDefault, Location
from scraper.config.get import get_encoding

from .actions.click_javascript import click_via_javascript
from .actions.click_next_page import click_next_page
from .actions.click_x_pop_up import click_x_pop_up
from .actions.pause import pause
from .CSV_Writer import CSV_Writer_RAW
from .debugger.printer import (
    print_current_date_time,
    print_current_page,
    print_key_value_pairs
)
from .elements_query.await_element import await_element
from .job_parser.job_parser import parse_data
from .job_value_getter.job_value_getter import get_values_for_job

# mypy bug https://github.com/python/mypy/issues/11426
Pages_Number = Literal["Unknown"] | int  # type: ignore[operator]

# Update the docstring


class GlassdoorJobScraper:
    '''
    This class provides a web scraping tool for job listings from Glassdoor 
    using Selenium for web automation. 
    The class contains functions for retrieving job data from the search results page, 
    parsing the job information, and writing the data to CSV files. 

    Attributes:
        jobs_number (int): The number of job listings to scrape.
        debug_mode (bool): Flag indicating whether to display debug information.
        driver (MyWebDriver): The webdriver instance for the current job search.
        csv_writer (CSV_Writer_RAW): Object responsible for writing data to CSV files.
        progress_bar (enlighten.Counter): Object responsible for displaying progress bar.
        number_of_pages (Pages_Number): The total number of pages for the job search results.

    Methods:
        save_jobs_to_csv_raw(): Retrieves and writes job data to CSV files.

    The class uses a number of helper functions and external packages including:
    - enlighten: A package for creating progress bars.
    - selenium: A package for web automation.
    - typing: A package for type hints.

    This class is intended for use by data scientists, recruiters, 
    and anyone else who needs to collect job data from Glassdoor in bulk. 
    '''

    def __init__(
            self,
            job_title: JobDefault,
            location: Location,
            jobs_number: JobNumber,
            debug_mode: DebugMode,
            driver: MyWebDriver
    ):
        self.job_title = job_title
        self.location = location
        self.jobs_number = jobs_number
        self.debug_mode = debug_mode
        self.driver = driver
        self.csv_writer = CSV_Writer_RAW(job_title, location)
        self.progress_bar = None
        self.number_of_pages = None

    def save_jobs_to_csv_raw(self):
        '''
        It scrapes job listings from Glassdoor website 
        and writes job data to CSV files in its raw version.
        Each founded job is appended each time to the CSV file separately.

        Returns:
            None

        Raises:
            NoSuchElementException: If the specified jobs buttons are not found.
            ElementClickInterceptedException: If a button is found, 
            but is not clickable at the moment.
            StaleElementReferenceException: If a button is no longer present on the page.
            TimeoutException: If a job posting is not found within a specified timeout.
        '''

        print("\r")
        print_current_date_time("Start")
        print(f"Job title: {self.job_title}")
        print(f"Location: {self.location}")

        self.number_of_pages = self._get_total_web_pages()
        if not self.debug_mode:
            self.progress_bar = enlighten.Counter(
                desc="Total progress",
                unit="jobs",
                color="green",
                total=self.jobs_number
            )

        while self.csv_writer.counter <= self.jobs_number:

            self._write_job_listings()

        if self.progress_bar:
            self.progress_bar.close()

        print_current_date_time("End")
        print("\r")

    def _write_job_listings(self):
        '''
        Parse job listings on Glassdoor and write data int CSV for each job.

        Returns:
            None

        Raises:
            NoSuchElementException: If the specified jobs buttons are not found.
            ElementClickInterceptedException: If a button is found, 
            but is not clickable at the moment.
            StaleElementReferenceException: If a button is no longer present on the page.
            TimeoutException: If a job posting is not found within a specified timeout.
        '''

        jobs_list_buttons = await_element(
            self.driver, 25, By.XPATH, '//ul[@data-test="jlGrid"]')

        jobs_buttons = self.get_jobs_buttons(jobs_list_buttons)

        if self.debug_mode:
            print_current_page(self.csv_writer.counter, len(
                jobs_buttons), self.number_of_pages)

        click_x_pop_up(self.driver)

        saved_button_index = self._calculate_index(jobs_buttons)

        for job_button in jobs_buttons[saved_button_index:]:

            if self.csv_writer.counter > self.jobs_number:
                break

            if self.debug_mode:
                print(
                    f"\rProgress: {self.csv_writer.counter}/{self.jobs_number}")

            try:
                job_button.click()

            except ElementClickInterceptedException:
                click_via_javascript(self.driver, job_button)

            except StaleElementReferenceException:
                self.driver.refresh()
                break

            pause()
            click_x_pop_up(self.driver)

            try:
                job = get_values_for_job(self.driver, job_button)

            except TimeoutException:
                self.driver.refresh()
                break

            if not self._job_posting_exists(job):

                if self.debug_mode:
                    self._save_errored_page()

                self.driver.refresh()
                break

            parse_data(job)

            if self.debug_mode:
                print_key_value_pairs(job)

            self.csv_writer.write_observation(job)

            if self.progress_bar:
                self.progress_bar.update()

        else:
            click_next_page(
                self.driver, self.csv_writer.counter, self.jobs_number)

            # Awaits element to upload all buttons. Traditional awaits elements didn't work out.
            # https://stackoverflow.com/questions/27003423/staleelementreferenceexception-on-python-selenium
            pause()

    def get_jobs_buttons(self, jobs_list_buttons: WebElement):
        '''
        Extracts job listing buttons from the jobs list container.

        Args:
            jobs_list_buttons (WebElement): The WebElement containing the job
                listing buttons to be extracted.

        Returns:
            jobs_buttons (list of WebElements): The list of WebElements
                representing the job listing buttons.

        Raises:
            NoSuchElementException: If no job listing buttons are found in
                the provided container.
            SystemExit: If the scraper was blocked by Glassdoor or if there
                was a misspelling in the job title.
        '''

        try:
            jobs_buttons: WebElements = jobs_list_buttons.find_elements(
                By.TAG_NAME, "li"
            )
        except NoSuchElementException as error:
            sys.exit(
                f"Check if you did not have any misspell in the job title or \
                    if you were silently blocked by glassdoor.\
                    \nError: {error}")

        return jobs_buttons

    def _get_total_web_pages(self) -> Pages_Number:
        '''
        Extracts the total number of pages from the job search results.

        Returns:
            - The total number of pages as an integer.
        '''

        target_element = '//div[@data-test="pagination-footer-text"]'

        try:
            total_pages = await_element(
                self.driver, 10, By.XPATH, target_element).text.strip().split(" ")[-1]
            return int(total_pages)
        except (
            TimeoutException,
            NoSuchElementException,
            StaleElementReferenceException,
            IndexError,
            ValueError
        ):
            return "Unknown"

    def _calculate_index(self, jobs_buttons: WebElements) -> int:
        '''
        Calculates the index of the next job button to click, 
        based on the current saved rows count and the number of job buttons available.

        Returns:
            - An integer representing the index of the next job button to click.
        '''

        return (self.csv_writer.counter - 1) % len(jobs_buttons)

    def _save_errored_page(self):
        '''
        his function saves the HTML content of the current page in a file named "error.html" 
        in the current working directory. In case there is an encoding error 
        while writing the file, it logs the error message in a file named "logs.log" 
        in the current working directory.

        Returns: None.
        '''

        try:
            html = self.driver.execute_script(
                "return document.body.innerHTML;")
            with open("error.html", "w", encoding=get_encoding()) as file:
                file.write(html)

        except UnicodeEncodeError as error:

            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(message)s')

            file_handler = logging.FileHandler('errors.log')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.error('This is an error message:%s', error)

    def _job_posting_exists(self, job: Job_values) -> bool:
        '''
        Checks whether the given job posting has a non-empty 'Company_name' field.

        Args:
        - job: a dictionary containing job posting values.

        Returns:
        - A boolean indicating whether the job posting has a company name.
        '''

        return job['Company_name'] != ""
