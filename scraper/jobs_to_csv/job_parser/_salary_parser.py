
'''
This module contains functions for parsing salary information in job postings. 
The parse_salary() function takes in a dictionary containing salary information 
and modifies the dictionary to include additional keys for
 salary low, salary high, salary estimate, and currency. 
 The insert_dict_to_dictionary() function inserts the salary key-value pairs 
 into the original job posting dictionary while maintaining the order of other keys.
'''

# Python
from typing import Any
import re


# Internal
from scraper.config.get import get_NA_value
from scraper.config._types import NA_value
from scraper._types import Field_value


def parse_salary(job: dict):
    '''
    Parses the salary data in the given dictionary and 
    adds new keys for salary low, salary high, salary estimate, and currency. 
    Deletes the 'Salary' key from the dictionary.

    Args:
        salary_dict (dict): A dictionary containing the salary data 
        in the format:
        - "$51K - $81K (Glassdoor est.)" 
        - "Employer Provided Salary: $51K - $81K"

    Returns:
        None: This function does not return anything. 
        The job dictionary is modified in place.
    '''

    salary: str | NA_value = job['Salary']

    na_value = get_NA_value()
    salary_values: dict[str, Field_value] = {
        'Salary_low': na_value,
        'Salary_high': na_value,
        'Currency': na_value,
        'Salary_provided': na_value
    }

    if salary != na_value:

        # Employer Provided Salary:$200K - $300K
        salary_range = get_pay_scale_ranges(salary)
        low, high = salary_range.split(' - ')

        salary_values['Salary_low'] = _parse_to_int(low)
        salary_values['Salary_high'] = _parse_to_int(high)
        salary_values['Currency'] = _get_currency(salary_range)
        salary_values['Salary_provided'] = get_is_provided(salary)

    # insert into dictionary
    insert_dict_to_dictionary(job, salary_values)

    del job['Salary']


def insert_dict_to_dictionary(job: dict, salary_values: dict):
    '''
    Inserts the keys and values from the given `salary_values` dictionary 
    into the `job` dictionary at the appropriate
    position relative to the 'Salary' key, preserving the order of the other keys.

    Args:
        job (dict): The dictionary to which the salary values will be added.
        salary_values (dict): The dictionary containing the salary values to be added.

    Returns:
        None: This function does not return anything. 
        The job dictionary is modified in place.
    '''

    index = get_key_index(job, 'Salary')
    insert_keys_values(job, salary_values, index)


def dict_to_tuples(dictionary: dict) -> list[tuple[Any, Any]]:
    '''
    Converts a dictionary into a list of tuples 
    where each tuple contains a key-value pair from the dictionary.

    Args:
        d (dict): A dictionary to convert.

    Returns:
        list: A list of tuples where each tuple contains a key-value pair from the dictionary.
    '''
    return list(dictionary.items())


def get_key_index(dict_receiver: dict, key) -> int:
    '''
    Return the index of a given key in a dictionary.

    Args:
        dict_receiver (dict): The dictionary to be searched for the key.
        key: The key to be searched for in the dictionary.

    Returns:
        int: The index of the key in the dictionary.

    Raises:
        ValueError: If the given key is not found in the dictionary.

    Example:
        >>> get_key_index({'a': 1, 'b': 2, 'c': 3}, 'b')
        1
    '''

    return list(dict_receiver.keys()).index(key)


def insert_keys_values(dict_receiver: dict, dict_add: dict, position: int):
    '''
    Inserts key-value pairs from a dictionary into another dictionary at a specified position.

    Args:
        dict_receiver (dict): The dictionary receiving the key-value pairs.
        dict_add (dict): The dictionary containing the key-value pairs to be added.
        position (int): The position in the receiver dictionary 
        where the key-value pairs should be inserted.

    Returns:
        None: This function does not return anything. 
        The job dictionary is modified in place.
    '''

    tuples_add = dict_to_tuples(dict_add)

    items = list(dict_receiver.items())

    for key_value in tuples_add:
        items.insert(position, key_value)
        position += 1

    dict_receiver.clear()  # to be sure of the right order of keys
    dict_receiver.update(dict(items))


def get_pay_scale_ranges(salary: str) -> str:
    '''
    Extracts pay-scale ranges from the given input string 
    using regular expressions.

    Args:
        salary (str): Input string containing pay-scale ranges.

    Returns:
        str: Pay-scale range extracted from the input string. 
        If multiple ranges are present, returns the first one.

    Raises:
        IndexError: If the match is a None type.
    '''

    # https://regex101.com/r/AY8ag3/1 read "$200K - $300K"
    pattern_pay_scale = r'\$\d+[Kk]? - \$\d+[Kk]?'
    pay_scale_match = re.search(pattern_pay_scale, salary)

    if pay_scale_match is None:
        raise IndexError(
            f"There is no return from the match:\n{pay_scale_match}"
        )

    pay_scale = pay_scale_match[0]  # type: ignore [index]

    return pay_scale


def get_is_provided(salary: str) -> bool | NA_value:
    '''
    Checks if the salary string contains "Employer Provided Salary" or "Glassdoor est".

    Args:
        salary: A string representing the salary.

    Returns:
        A boolean value of True if the salary is employer provided, 
        False if it's estimated by Glassdoor, 
        or a NA_value if the salary is not provided.
    '''

    if "Employer Provided Salary" in salary:
        return True
    if "Glassdoor est" in salary:
        return False

    return get_NA_value()


def _get_currency(salary_range: str) -> str:
    '''
    Returns the currency from the salary range string.

    Args:
        salary_range (str): The salary range string.

    Returns:
        str: The currency string.

    Raises:
        IndexError: If the match is a None type.
    '''

    # https://regex101.com/r/FEKvy6/387
    currency_match = re.search(r"^.+?(?=\d)", salary_range)

    if currency_match is None:
        raise IndexError(
            f"There is no return from the match:\n{currency_match}"
        )

    currency = currency_match[0]
    currency_no_spaces = currency.strip()

    return currency_no_spaces


def assert_is_match(match: re.Match[str] | None):
    '''
    Check if a given regex match exists.

    Args:
        match (re.Match[str] | None): The regex match.

    Returns:
        None

    Raises:
        IndexError: If the match is a None type.
    '''


def _parse_to_int(salary: str) -> int:
    '''
    Parses the salary string to an integer.

    Args:
        salary (str): The salary string.

    Returns:
        int: The integer value of the salary string.
    '''

    if salary.endswith('K'):
        value = _change_to_integer(salary)
        value_K_ed = value * 1000
        return value_K_ed
    else:
        value = _change_to_integer(salary)
        return value


def _change_to_integer(salary: str) -> int:
    '''
    Converts the given string to an integer.

    Args:
        salary (str): The salary string.

    Returns:
        int: The integer value of the salary string.
    '''

    numeric_filter = filter(str.isdigit, salary)
    numeric_string = "".join(numeric_filter)
    integer = int(numeric_string)

    return integer
