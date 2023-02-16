# Internal
from scraper._types import Job_values
from scraper.helpers.add_columns_to_row_from_dict import add_columns_to_row_from_dict
from scraper.helpers.get_values_from_source import get_values_from_source


def add_columns_to_row_from_source(job_row, values_source, values_to_add):
    '''In Python you do not have to return a dict from a function to change the dict'''

    values_to_add: Job_values = get_values_from_source(
        values_source, values_to_add)

    add_columns_to_row_from_dict(job_row, values_to_add)
