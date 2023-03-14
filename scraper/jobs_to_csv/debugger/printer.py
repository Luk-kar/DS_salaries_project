'''
This module provides a functions
for printing info needed for debugging
'''
# Python
from datetime import datetime
import math
from os import get_terminal_size
from typing import Literal

# Internal
from scraper._types import Job


def print_key_value_pairs(job: Job):
    '''used for debugging, when parsing HTML'''

    for index, (key, value) in enumerate(job.items()):
        print(f"\r{index + 1}. {key}:\n{value}")

    _print_separator("=")


def _print_separator(char_separator: str):
    '''
    Prints a separator line composed of a single character.

    Args:
    - char_separator: a string with a single character that will be repeated
    to compose the separator line.

    Returns: None
    '''

    terminal_width = get_terminal_size().columns
    separator = f"\n{char_separator * terminal_width}\n"
    print(separator)


def print_current_page(jobs_so_far: int, jobs_per_page: int, number_of_pages: int | Literal["Unknown"]):
    '''
    Prints the current page number, calculated based on the number
    of jobs already scraped and the number of jobs displayed 
    per page on the website.

    Args:
    - jobs_so_far: an integer representing the total number of jobs already scraped.
    - jobs_per_page: an integer representing the number of jobs displayed per page on the website.

    Returns: None

    Note:
    It is strongly not advised to use extracted page footer element's text each time.
    Keep things less dependent on elements loaded from the site.
    The fewer interactions, the higher is chance that something will not break up.
    '''
    page_count = math.ceil(jobs_so_far / jobs_per_page)

    pagination_footer = f"Page {page_count} of {number_of_pages}"

    separator = "-"

    _print_separator(separator)

    print(pagination_footer)

    _print_separator(separator)


def print_current_date_time(intro_word: Literal["Start", "End"]):
    '''
    Prints the current date and time in ISO format with second precision.

    Args:
    - intro_word: Literal["Start", "End"]
        A string literal that indicates whether the current date and time
        are being printed at the start or end of an operation.

    Returns:
    - None

    Note:
    - This function does not return anything; it just prints the current
    date and time.
    '''
    now = datetime.now().isoformat(sep=" ", timespec="seconds")
    print(f"\r{intro_word}: {now}")
