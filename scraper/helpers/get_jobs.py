# Python
from datetime import datetime
import sys
import re

# External
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Internal
from scraper.config.get import get_config
from scraper.config._types import JobNumber, DebugMode, NA_value
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

    na_value = get_config()['NA_value']  # todo
    for key, value in job.items():

        if is_NA_value(value):
            job[key] = na_value
            print(f"{key}: {job[key]}")

    parse_easy_apply(job)
    parse_numerical_values(job)
    parse_salary(job)
    parse_employees(job)
    parse_revenue(job)


def is_NA_value(value):
    """
    Checks whether the given value is an NA value.

    Args:
        value (any): The value to check.

    Returns:
        bool: True if the value is NA, False otherwise.
    """
    NA_VALUES = [[], "N/A", "Unknown / Non-Applicable"]

    if is_emptish_string(value) or value in NA_VALUES:
        return True
    else:
        return False


def is_emptish_string(value):
    return isinstance(value, str) and len(value.strip()) == 0


def parse_revenue(job):
    na_value = get_config()['NA_value']
    if job['Revenue_USD'] != na_value:
        job['Revenue_USD'] = job['Revenue_USD'].replace("(USD)", "").strip()


def parse_employees(job):
    na_value = get_config()['NA_value']
    if job['Employees'] != na_value:
        job['Employees'] = job['Employees'].replace("Employees", "").strip()


def parse_numerical_values(job: dict):
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


def parse_easy_apply(job: dict):
    """
    Cleans the 'Easy_apply' field in the input job dictionary.

    Args:
        job (dict): The job dictionary to be cleaned.
    """
    if 'Easy_apply' in job:
        job['Easy_apply'] = bool(job['Easy_apply'])


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


def parse_salary(job: dict) -> dict:
    """Parses the salary data in the given dictionary and adds new keys for salary low, salary high, salary estimate,
    and currency. Deletes the 'Salary' key from the dictionary.

    Args:
        salary_dict (dict): A dictionary containing the salary data in the format "$51K - $81K (Glassdoor est.)".

    Returns:
        None: This function does not return a value; 
        it updates the `job` dictionary in place.
    """

    salary = job['Salary']

    na_value = get_config()['NA_value']
    salary_values = {
        'Salary_low': na_value,
        'Salary_high': na_value,
        'Currency': na_value,
        'Salary_provided': na_value
    }

    if salary:

        # Employer Provided Salary:$200K - $300K
        salary_range = get_pay_scale_ranges(salary)
        low, high = salary_range.split(' - ')

        salary_values['Salary_low'] = _parse_to_int(low)
        salary_values['Salary_high'] = _parse_to_int(high)
        salary_values['Currency'] = _get_currency(salary_range)
        salary_values['Salary_provided'] = get_estimate(salary)

    # insert into dictionary
    index = get_key_index(job, 'Salary')
    insert_keys_values(job, salary_values, index)

    del job['Salary']


def dict_to_tuples(dictionary: dict) -> list:
    """
    Converts a dictionary into a list of tuples where each tuple contains a key-value pair from the dictionary.

    Args:
        d (dict): A dictionary to convert.

    Returns:
        list: A list of tuples where each tuple contains a key-value pair from the dictionary.
    """
    return list(dictionary.items())


def get_key_index(dict_receiver: dict, key) -> int:

    return list(dict_receiver.keys()).index(key)


def insert_keys_values(dict_receiver: dict, dict_add: dict, pos: int) -> dict:

    tuples_add = dict_to_tuples(dict_add)

    items = list(dict_receiver.items())

    for key_value in tuples_add:
        items.insert(pos, key_value)
        pos += 1

    dict_receiver.clear()  # to be sure that order of keys will be right
    dict_receiver.update(dict(items))


def get_pay_scale_ranges(salary: str) -> str:
    """
    Extracts pay-scale ranges from the given input string using regular expressions.

    Args:
        salary (str): Input string containing pay-scale ranges.

    Returns:
        str: Pay-scale range extracted from the input string. If multiple ranges are present, returns the first one.
    """

    # https://regex101.com/r/AY8ag3/1 read "$200K - $300K"
    pattern_pay_scale = r'\$\d+[Kk]? - \$\d+[Kk]?'
    pay_scale = re.search(pattern_pay_scale, salary)[0]

    return pay_scale


def get_estimate(salary: str) -> bool | NA_value:

    if "Employer Provided Salary" in salary:
        return True
    elif "Glassdoor est" in salary:
        return False
    else:
        return get_config()['NA_value']


def _get_currency(salary_range: str) -> str:
    """Returns the currency from the salary range string.

    Args:
        salary_range (str): The salary range string.

    Returns:
        str: The currency string.
    """

    # https://regex101.com/r/FEKvy6/387
    currency = re.search(r"^.+?(?=\d)", salary_range)[0]
    currency_no_spaces = currency.strip()

    return currency_no_spaces


def _change_to_integer(salary: str) -> int:
    """Converts the given string to an integer.

    Args:
        salary (str): The salary string.

    Returns:
        int: The integer value of the salary string.
    """

    numeric_filter = filter(str.isdigit, salary)
    numeric_string = "".join(numeric_filter)
    integer = int(numeric_string)

    return integer


def _parse_to_int(salary: str) -> int:
    """Parses the salary string to an integer.

    Args:
        salary (str): The salary string.

    Returns:
        int: The integer value of the salary string.
    """

    if salary.endswith('K'):
        value = _change_to_integer(salary)
        value_K_ed = value * 1000
        return value_K_ed
    else:
        value = _change_to_integer(salary)
        return value
