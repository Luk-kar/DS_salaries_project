# Python
from datetime import datetime
import sys

# External
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper.config._types import JobNumber, DebugMode
from scraper._types import MyWebDriver
from .elements_query.await_element import await_element
from .actions.click_x_pop_up import click_x_pop_up
from .job_value_getter.job_value_getter import get_values_for_job
from .actions.pause import pause
from .job_parser.job_parser import parse_data
from .debugger.print_key_value_pairs import print_key_value_pairs

WebElements = list[WebElement]


def get_jobs_to_csv(jobs_number: JobNumber, debug_mode: DebugMode, driver: MyWebDriver):
    '''Getting list of job postings values populated with glassdoor.com'''

    if debug_mode:
        now = datetime.now().isoformat(sep=" ", timespec="seconds")
        print(f"\n{now}\n")

    jobs_counter = 1

    while jobs_counter <= jobs_number:

        jobs_list_buttons: WebElement = await_element(
            driver, 20, By.XPATH, '//ul[@data-test="jlGrid"]')

        try:
            jobs_buttons: WebElements = jobs_list_buttons.find_elements(
                By.TAG_NAME, "li"
            )
        except NoSuchElementException as error:
            sys.exit(
                f"Check if you did not any misspell in the job title or \
                if you were silently blocked by glassdoor.\
                \nError: {error}")

        click_x_pop_up(driver)

        for job_button in jobs_buttons:

            print(f"Progress: {jobs_counter}/{jobs_number}")

            if jobs_counter >= jobs_number + 1:
                break

            try:
                job_button.click()

            except ElementClickInterceptedException:

                execute_via_javascript(driver, job_button)

            pause()

            click_x_pop_up(driver)

            job = get_values_for_job(driver, job_button)

            parse_data(job)

            if debug_mode:
                print_key_value_pairs(job)

            # write job to csv
            # todo

        click_next_page(driver, jobs_counter, jobs_number)


def click_next_page(driver: MyWebDriver, jobs_counter: int, jobs_number: int):
    """
    Clicks on the 'Next' button to navigate to the next page of job listings on Glassdoor.

    Args:
    - driver (MyWebDriver): The webdriver instance used to interact with the Glassdoor website.
    - jobs_counter (int): The number of jobs that have been scraped so far.
    - jobs_number (int): The total number of jobs to scrape.

    Raises:
    - ElementClickInterceptedException: If the 'Next' button is present 
    but is not clickable due to an overlay element blocking it.

    - NoSuchElementException: If the 'Next' button is not found on the page, 
    which indicates that there are no more job listings to scrape.

    Note:
    - If the 'Next' button is not clickable due to a driver's error blocking it, 
    the function will attempt to click the button using JavaScript 
    instead of the standard WebDriver click method.
    """

    try:
        next_page = driver.find_element(
            By.XPATH, "//button[@data-test='pagination-next']")

        if next_page.is_enabled():
            next_page.click()
        else:
            exit_scraping_when_no_more_jobs(jobs_counter, jobs_number)

    except ElementClickInterceptedException:
        execute_via_javascript(driver, next_page)

    except NoSuchElementException:
        exit_scraping_when_no_more_jobs(jobs_counter, jobs_number)


def exit_scraping_when_no_more_jobs(jobs_counter: int, jobs_number: int):
    """
    Exits the program when there is no more jobs to scrape from the website.

    Args:
    - jobs_counter (int): The number of jobs that have been scraped so far.
    - jobs_number (int): The total number of jobs to scrape.
    """

    sys.exit(
        f"Scraping terminated before reaching target number of jobs.\n\
            Needed {jobs_counter}, got {jobs_number}."
    )


def execute_via_javascript(driver: MyWebDriver, job_button: WebElement):
    '''
    Executes a click on a WebElement using JavaScript instead of using the 
    standard WebDriver click method.

    :param driver: A webdriver instance to use for executing the script.
    :type driver: MyWebDriver

    :param job_button: The WebElement to click on.
    :type job_button: WebElement
    '''

    # https://stackoverflow.com/a/48667924/12490791
    driver.execute_script("arguments[0].click();", job_button)
