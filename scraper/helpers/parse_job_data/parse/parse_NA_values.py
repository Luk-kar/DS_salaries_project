
# Internal
from scraper.config.get import get_NA_value


def parse_NA_values(job: dict):
    """
    Replaces all NA values in the input job dictionary with the NA value specified
    in the configuration.

    Args:
        job (dict): The job dictionary to parse.

    Returns:
        None: This function does not return anything. 
        The job dictionary is modified in place.
    """

    na_value = get_NA_value()
    for key, value in job.items():
        if _is_NA_value(value):
            job[key] = na_value


def _is_NA_value(value):
    """
    Checks whether the given value is an NA value.

    Args:
        value (any): The value to check.

    Returns:
        bool: True if the value is NA, False otherwise.
    """
    NA_VALUES = [[], "N/A", "Unknown / Non-Applicable"]

    return bool(
        _is_emptish_string(value) or value in NA_VALUES
    )


def _is_emptish_string(value: str) -> bool:
    """
    Check if a string is empty or contains only whitespace characters.

    Args:
        value (str): The string to check.

    Returns:
        bool: True if the string is empty or contains only whitespace characters, False otherwise.
    """
    return isinstance(value, str) and len(value.strip()) == 0
