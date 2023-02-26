# Python
from datetime import datetime
import sys

# External
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Internal
from scraper.config._types import JobNumber, DebugMode
from scraper._types import MyWebElement, Jobs, MyWebDriver
from .elements_query.await_element import await_element
from .actions.click_x_pop_up import click_x_pop_up
from .job_value_getter.job_value_getter import get_values_for_job
from .actions.pause import pause
from .job_parser.job_parser import parse_data
from .debugger.print_key_value_pairs import print_key_value_pairs


def get_jobs(jobs_number: JobNumber, debug_mode: DebugMode, driver: MyWebDriver):
    '''Getting list of job postings values populated with glassdoor.com'''

    jobs: Jobs = []

    if debug_mode:
        now = datetime.now().isoformat(sep=" ", timespec="seconds")
        print(f"\n{now}\n")

    while len(jobs) < jobs_number:
        jobs_list_buttons: MyWebElement = await_element(
            driver, 20, By.XPATH, '//ul[@data-test="jlGrid"]')

        try:
            jobs_buttons: list[MyWebElement] = jobs_list_buttons.find_elements(
                By.TAG_NAME, "li"
            )
        except NoSuchElementException as error:
            sys.exit(
                f"Check if you did not any misspell in the job title or \
                if you were silently blocked by glassdoor.\
                \nError: {error}")

        click_x_pop_up(driver)

        for job_button in jobs_buttons:
            print(f"Progress: {len(jobs) + 1}/{jobs_number}")

            if len(jobs) >= jobs_number:
                break

            job_button.click()

            pause()

            click_x_pop_up(driver)

            job = get_values_for_job(driver, job_button)

            parse_data(job)

            if debug_mode:
                print_key_value_pairs(job)

            jobs.append(job)
