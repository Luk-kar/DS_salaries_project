'''
This module provides functions to parse numerical values in a given job dictionary. 
The main function parse_numerical_values() converts positive numeric 
and percentage values in the input job dictionary to floats and integers.
'''
# Python
import re

Match = re.Match[str]


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

            if _is_positive_float(value):

                # Replace commas with decimal points for consistency
                job[key] = value.replace(",", ".")

            else:
                percent_value = _get_percent_value(value)

                if percent_value:
                    job[key] = _convert__percent_to_float(percent_value)


def _convert__percent_to_float(percent_value: Match) -> float:
    '''
    Converts a percentage string to a float between 0.0 and 1.0.

    Args:
        percent_value (Match): A match object containing a percentage string in the format
            "n%", "n %" where n is a positive float or integer.

    Returns:
        float: The decimal fraction equivalent of the percentage value.

    Raises:
        TypeError: If percent_value is not a valid string.
        AttributeError: If percent_value is not a match object.
        ValueError: If the numeric part of percent_value is not a valid float or integer,
            or if the resulting decimal fraction is not between 0.0 and 1.0.
    '''

    try:
        # Replace commas with decimal points for consistency
        numeric_part = percent_value.group(1).replace(',', '.')
        decimal_fraction = float(numeric_part) / 100

        if 0.0 <= decimal_fraction <= 1.0:
            return decimal_fraction
        else:
            raise ValueError(
                f"The value is not between 0.0 and 1.0.\nError value:{decimal_fraction}"
            )

    except (TypeError, AttributeError) as error:
        raise f"Input value must be a string:{percent_value}\n{error}" from error

    except ValueError as error:
        raise f"Invalid numeric part:{percent_value}\n{error}" from error


def _get_percent_value(value: str) -> Match | None:
    """
    Gets a string representing a percentage value.

    Args:
        - value (str): The string to be checked.

    Returns:
        - match (re.Match | None): A Match object if the input string 
        is a valid percentage value, or None otherwise.
    Examples:
        >>> get_percent_value("25%")
        <re.Match object; span=(0, 3), match='25%'>

        >>> get_percent_value("12.5%")
        <re.Match object; span=(0, 5), match='12.5%'>

        >>> get_percent_value(" 123,5 %")
        <re.Match object; span=(0, 9), match=' 123,5 % '>

        >>> get_percent_value("25.0")
        None
    """

    # https://regex101.com/r/YhKtm0/1
    pattern = r"^\s*([\,\.]*\d+|\d+[\,\.]*\d*)\s*%\s*$"
    match = re.match(pattern, value)
    return match


def _is_positive_float(value: str) -> bool:
    """
    Check if the given string is a positive float.

    Args:
        value: A string to check if it's a positive float.

    Returns:
        A boolean value indicating whether the string is a positive float or not.

    Examples:
        >>> is_positive_float("3.14")
        True
        >>> is_positive_float("0.00")
        True
        >>> is_positive_float("0,00")
        True
        >>> is_positive_float("10")
        False
        >>> is_positive_float("-2.5")
        False
        >>> is_positive_float("abc")
        False
    """
    try:
        float_value = float(value.replace(",", "."))
        return float_value >= 0.0
    except ValueError:
        return False
