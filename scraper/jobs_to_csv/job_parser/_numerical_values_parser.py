'''
This module provides functions to parse numerical values in a given job dictionary. 
The main function parse_numerical_values() converts positive numeric 
and percentage values in the input job dictionary to floats and integers.
'''


def parse_numerical_values(job: dict):
    '''
    Converts positive numeric and percentage values 
    in the input job dictionary 
    to floats and integers.

    Args:
        job (dict): The job dictionary to be cleaned.
    '''
    for key, value in job.items():

        if isinstance(value, str):

            if _is_positive_number(value):

                if _is_int(value):
                    job[key] = int(value)
                else:
                    job[key] = float(value)

            elif _is_percent_value(value):
                job[key] = _percent_string_to_float(value)


def _is_positive_number(string: str) -> bool:
    '''
    Determines whether a string represents a positive number.

    Args:
        string: A string to check.

    Returns:
        True if the string represents a positive number, False otherwise.

    Examples:
        >>> is_positive_number('1.23')
        True
        >>> is_positive_number('0')
        True
        >>> is_positive_number('-1')
        False
        >>> is_positive_number('abc')
        False
    '''

    if _is_number(string):

        return float(string) >= 0

    return False


def _is_number(string: str):
    '''

    Returns True if the input string can be converted to a floating point number, 
    and False otherwise.

    Args:
        string (str): The input string to be checked.

    Returns:
        bool: True if the input string is a number, False otherwise.

    Examples:
        >>> is_number('123')
        True
        >>> is_number('0.123')
        True
        >>> is_number('abc')
        False
    '''
    try:
        float(string)
        return True
    except ValueError:
        return False


def _is_int(string: str) -> bool:
    '''
    Returns True if the given string represents a positive integer, 
    and False otherwise.

    Args:
    string (str): The string to check.

    Returns:
    bool: True if the string represents an integer, and False otherwise.
    '''
    return string.isdigit()


def _is_percent_value(string: str) -> bool:
    '''
    Check whether the input string represents a valid percentage value.

    Args:
        string (str): The string to check.

    Returns:
        bool: True if the input string represents a valid percentage value, False otherwise.
    '''
    try:
        value = _get_percent_value(string)
        return _is_percent_valid(value)
    except ValueError:
        return False


def _is_percent_valid(value: float) -> bool:
    '''
    Determines if the input value is a valid percent value.

    Args:
        value (float): A numeric value representing a percent.

    Returns:
        bool: True if the input value is a valid percent value (i.e., between 0.0 and 1.0, inclusive),
              False otherwise.
    '''
    return 0.0 <= value <= 1.0


def _percent_string_to_float(string: str) -> float:
    '''
    Converts a string representing a percent value to a float between 0.0 and 1.0.

    Args:
        string: A string representing a percent value. The string should be in the
            format "<number>%" where <number> is a positive float or integer.

    Returns:
        A float value between 0.0 and 1.0 representing the percent value.

    Raises:
        ValueError: If the input string is not in the correct format or represents an
            invalid percent value.
    '''
    try:
        value = _get_percent_value(string)
    except ValueError as exception:
        raise ValueError(f"Invalid input string: {string}") from exception

    if not _is_percent_valid(value):
        raise ValueError("Invalid percent value")

    return value / 100


def _get_percent_value(string: str) -> float:
    '''
    Returns the percent value represented by the input string.

    Args:
        string (str): The input string that represents a percent value.

    Returns:
        float: The float value of the input percent string, without the "%" symbol.

    Raises:
        ValueError: If the input string cannot be converted to a float.

    Examples:
        >>> _get_percent_value("50%")
        0.5

        >>> _get_percent_value("2.5%")
        0.025

        >>> _get_percent_value("1.0")
        0.01

        >>> _get_percent_value("100.00%")
        1.0
    '''
    string = string.strip()
    if string.endswith('%'):
        string = string[:-1]
    return float(string)
