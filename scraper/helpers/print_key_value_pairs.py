'''
This module provides a function that prints key-value pairs for a Job object, which is used for debugging when parsing HTML.
'''

# Internal
from scraper._types import Job


def print_key_value_pairs(job: Job):
    '''used for debugging, when parsing HTML'''

    for index, (key, value) in enumerate(job.items()):
        print(f"{index + 1}. {key}:\n{value}")

    print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
