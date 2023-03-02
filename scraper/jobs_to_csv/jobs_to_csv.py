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
from .actions.click_javascript import click_via_javascript
from .actions.click_next_page import click_next_page
from .actions.click_x_pop_up import click_x_pop_up
from .actions.pause import pause
from .CSV_Writer import CSV_Writer_RAW
from .job_value_getter.job_value_getter import get_values_for_job
from .job_parser.job_parser import parse_data
from .debugger.printer import print_key_value_pairs, print_current_page


# todo one source of truth, avoid circular import
WebElements = list[WebElement]


def save_jobs_to_csv(jobs_number: JobNumber, debug_mode: DebugMode, driver: MyWebDriver):
    '''Getting list of job postings values populated with glassdoor.com'''

    if debug_mode:
        now = datetime.now().isoformat(sep=" ", timespec="seconds")
        print(f"\nDate: {now}")

    csv_writer = CSV_Writer_RAW()

    while csv_writer.counter <= jobs_number:

        if debug_mode:
            print_current_page(driver)

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

        click_x_pop_up(driver)

        for job_button in jobs_buttons:

            print(f"Progress: {csv_writer.counter}/{jobs_number}")

            if csv_writer.counter >= jobs_number + 1:
                break

            try:
                job_button.click()

            except ElementClickInterceptedException:

                click_via_javascript(driver, job_button)

            pause()

            click_x_pop_up(driver)

            job = get_values_for_job(driver, job_button)

            parse_data(job)

            if debug_mode:
                print_key_value_pairs(job)

            csv_writer.write_observation(job)

        click_next_page(driver, csv_writer.counter, jobs_number)

        # todo There has to be more elegant and efficient way to do it
        # Await element to upload all buttons
        # https://stackoverflow.com/questions/27003423/staleelementreferenceexception-on-python-selenium
        pause()
