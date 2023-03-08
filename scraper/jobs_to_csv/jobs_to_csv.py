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
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper.config._types import JobNumber, DebugMode
from scraper.config.get import get_encoding
from scraper._types import MyWebDriver, Job_values, WebElements
from .elements_query.await_element import await_element
from .actions.click_javascript import click_via_javascript
from .actions.click_next_page import click_next_page
from .actions.click_x_pop_up import click_x_pop_up
from .actions.pause import pause
from .CSV_Writer import CSV_Writer_RAW
from .job_value_getter.job_value_getter import get_values_for_job
from .job_parser.job_parser import parse_data
from .debugger.printer import print_key_value_pairs, print_current_page, print_current_date_time

# mypy bug https://github.com/python/mypy/issues/11426
Pages_Number = Literal["Unknown"] | int  # type: ignore[operator]


def save_jobs_to_csv_raw(jobs_number: JobNumber, debug_mode: DebugMode, driver: MyWebDriver):
    '''
    This function saves job listings to a CSV file in RAW format. 

    Args:
        - jobs_number (JobNumber): The total number of jobs to save.
        - debug_mode (DebugMode): A boolean variable indicating whether to run in debug mode.
        - driver (MyWebDriver): An instance of the MyWebDriver class representing a web browser.

    Returns: None
    '''

    print("\r")
    print_current_date_time("Start")

    csv_writer = CSV_Writer_RAW()

    progress_bar = None
    if not debug_mode:
        progress_bar = enlighten.Counter(desc="Total progress",  unit="jobs",
                                         color="green", total=jobs_number)

    number_of_pages = _get_total_web_pages(driver)

    while csv_writer.counter <= jobs_number:

        parse_job_listings(
            jobs_number,
            debug_mode,
            driver,
            csv_writer,
            progress_bar,
            number_of_pages
        )

    if progress_bar:
        progress_bar.close()

    print_current_date_time("End")
    print("\r")


def parse_job_listings(
        jobs_number,
        debug_mode,
        driver,
        csv_writer,
        progress_bar,
        number_of_pages
):

    jobs_list_buttons: WebElement = await_element(
        driver, 20, By.XPATH, '//ul[@data-test="jlGrid"]')

    try:
        jobs_buttons: WebElements = jobs_list_buttons.find_elements(
            By.TAG_NAME, "li"
        )
    except NoSuchElementException as error:
        sys.exit(
            f"Check if you did not have any misspell in the job title or \
                if you were silently blocked by glassdoor.\
                \nError: {error}")

    if debug_mode:
        print_current_page(csv_writer.counter, len(
            jobs_buttons), number_of_pages)

    click_x_pop_up(driver)

    saved_button_index = _calculate_index(csv_writer, jobs_buttons)

    for job_button in jobs_buttons[saved_button_index:]:  # todo to function

        if csv_writer.counter > jobs_number:
            break

        if debug_mode:
            print(f"Progress: {csv_writer.counter}/{jobs_number}")

        try:
            job_button.click()

        except ElementClickInterceptedException:
            click_via_javascript(driver, job_button)

        except StaleElementReferenceException:
            driver.refresh()
            break

        pause()

        click_x_pop_up(driver)

        try:
            job = get_values_for_job(driver, job_button)

        except TimeoutException:
            driver.refresh()
            break

        if not _job_posting_exists(job):
            if debug_mode:
                _save_errored_page(driver)

            driver.refresh()
            break

        parse_data(job)

        if debug_mode:
            print_key_value_pairs(job)

        csv_writer.write_observation(job)

        if progress_bar:
            progress_bar.update()

    else:
        click_next_page(driver, csv_writer.counter, jobs_number)

        # Awaits element to upload all buttons. Traditional awaits elements didn't work out.
        # https://stackoverflow.com/questions/27003423/staleelementreferenceexception-on-python-selenium
        pause()


def _get_total_web_pages(driver: MyWebDriver) -> Pages_Number:
    '''
    Extracts the total number of pages from the job search results.

    Args:
        - driver (MyWebDriver): The webdriver instance for the current job search.

    Returns:
        - The total number of pages as an integer.
    '''

    target_element = '//div[@data-test="pagination-footer-text"]'

    try:
        total_pages = await_element(
            driver, 10, By.XPATH, target_element).text.strip().split(" ")[-1]
        return int(total_pages)
    except (
        TimeoutException,
        NoSuchElementException,
        StaleElementReferenceException,
        IndexError,
        ValueError
    ):
        return "Unknown"


def _calculate_index(csv_writer: CSV_Writer_RAW, jobs_buttons: WebElements):
    '''
    Calculates the index of the next job button to click, 
    based on the current saved rows count and the number of job buttons available.

    Args:
        - csv_writer (CSV_Writer_RAW): An instance of the CSV_Writer_RAW class, 
        which keeps track of the number of jobs saved so far.
        - jobs_buttons (WebElement): The list of job buttons available on the current page.

    Returns:
        - An integer representing the index of the next job button to click.
    '''

    return (csv_writer.counter - 1) % len(jobs_buttons)


def _save_errored_page(driver: MyWebDriver):
    '''
    his function saves the HTML content of the current page in a file named "error.html" 
    in the current working directory. In case there is an encoding error 
    while writing the file, it logs the error message in a file named "logs.log" 
    in the current working directory.

    Args:

        - driver: an instance of MyWebDriver class representing a web browser.

    Returns: None.
    '''

    try:
        html = driver.execute_script(
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


def _job_posting_exists(job: Job_values) -> bool:
    '''
    Checks whether the given job posting has a non-empty 'Company_name' field.

    Args:
    - job: a dictionary containing job posting values.

    Returns:
    - A boolean indicating whether the job posting has a company name.
    '''
    return job['Company_name'] != ""
