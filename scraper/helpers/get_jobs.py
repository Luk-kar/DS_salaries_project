# Python
from datetime import datetime
import sys

# External
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Internal
from scraper.config._types import JobNumber, DebugMode
from scraper._types import MyWebElement, Jobs, MyWebDriver
from scraper.helpers.elements_query.await_element import await_element
from scraper.helpers.actions.click_x_pop_up import click_x_pop_up
from scraper.helpers.get_job_values.get_job_values import get_job_values
from scraper.helpers.actions.pause import pause
from scraper.helpers.print_key_value_pairs import print_key_value_pairs


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

            job = get_job_values(driver, job_button)

            clean_job_data(job)

            if debug_mode:
                print_key_value_pairs(job)

            jobs.append(job)


def clean_job_data(job: dict):
    """
    Cleans the input job dictionary by converting numeric and percentage values to floats and integers.

    Args:
        job (dict): The job dictionary to be cleaned.
    """
    clean_easy_apply(job)
    clean_numeric_values(job)


def clean_numeric_values(job: dict):
    """
    Converts numeric and percentage values in the input job dictionary to floats and integers.

    Args:
        job (dict): The job dictionary to be cleaned.
    """
    for key, value in job.items():
        if isinstance(value, str):
            if is_number(value):
                if is_positive_int(value):
                    job[key] = int(value)
                else:
                    job[key] = float(value)
            elif is_percent_value(value):
                job[key] = percent_string_to_float(value)

            # $51K - $81K (Glassdoor est.)

            # look at notepad

            # 51 to 200 Employees

            # Revenue:


def clean_easy_apply(job: dict):
    """
    Cleans the 'Easy_apply' field in the input job dictionary.

    Args:
        job (dict): The job dictionary to be cleaned.
    """
    if 'Easy_apply' in job:
        job['Easy_apply'] = bool(job['easy apply'])


def is_number(string: str):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_positive_int(string):
    return string.isdigit()


def is_percent_value(string: str) -> bool:
    """
    Returns True if the input string is a valid percent value, False otherwise.
    """
    try:
        value = _get_percent_value(string)
        return _is_percent(value)
    except ValueError:
        return False


def _get_percent_value(string: str) -> float:
    """
    Returns the percent value represented by the input string.
    """
    string = string.strip()
    if string.endswith('%'):
        string = string[:-1]
    return float(string)


def _is_percent(value: float) -> bool:
    """
    Returns True if the input value is a valid percent value, False otherwise.
    """
    return 0 <= value <= 100


def percent_string_to_float(string: str) -> float:
    """
    Converts the input string to a float between 0.0 and 1.0 if it represents a valid percent value.
    """
    try:
        value = _get_percent_value(string)
        if _is_percent(value):
            return value / 100
        else:
            raise ValueError("Invalid percent value")
    except ValueError as e:
        raise ValueError(f"Invalid input string: {string}") from e
