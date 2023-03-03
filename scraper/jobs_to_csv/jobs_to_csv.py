# Python
import logging
import sys

# External
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper.config._types import JobNumber, DebugMode
from scraper.config.get import get_encoding
from scraper._types import MyWebDriver, Job_values
from .elements_query.await_element import await_element
from .actions.click_javascript import click_via_javascript
from .actions.click_next_page import click_next_page
from .actions.click_x_pop_up import click_x_pop_up
from .actions.pause import pause
from .CSV_Writer import CSV_Writer_RAW
from .job_value_getter.job_value_getter import get_values_for_job
from .job_parser.job_parser import parse_data
from .debugger.printer import print_key_value_pairs, print_current_page, print_current_date_time


# todo one source of truth, avoid circular import
WebElements = list[WebElement]


def save_jobs_to_csv(jobs_number: JobNumber, debug_mode: DebugMode, driver: MyWebDriver):
    '''Getting list of job postings values populated with glassdoor.com'''

    if debug_mode:
        print_current_date_time()

    csv_writer = CSV_Writer_RAW()

    while csv_writer.counter <= jobs_number:

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
            print_current_page(csv_writer.counter, len(jobs_buttons))

        click_x_pop_up(driver)

        saved_button_index = (csv_writer.counter - 1) % len(jobs_buttons)

        for job_button in jobs_buttons[saved_button_index:]:

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

            if not job_posting_exists(job):

                _save_errored_page(driver)

                driver.refresh()
                break

            parse_data(job)

            if debug_mode:
                print_key_value_pairs(job)

            csv_writer.write_observation(job)

        else:

            click_next_page(driver, csv_writer.counter, jobs_number)

            # todo There has to be more elegant and efficient way to do it
            # Awaits element to upload all buttons. Traditional awaits elements didn't work out.
            # https://stackoverflow.com/questions/27003423/staleelementreferenceexception-on-python-selenium
            pause()


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
        with open("error.html", "w", encoding=get_encoding()) as f:
            f.write(html)
    except UnicodeEncodeError as e:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s')

        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.error(f'This is an error message:{e}')


def job_posting_exists(job: Job_values) -> bool:
    '''
    Checks whether the given job posting has a non-empty 'Company_name' field.

    Args:
    - job: a dictionary containing job posting values.

    Returns:
    - A boolean indicating whether the job posting has a company name.
    '''
    return job['Company_name'] != ""
