
# Internal
from scraper._types import Job_elements, Job_values, WebDriver
from scraper.helpers.add_columns_to_job_from_dict import add_columns_to_job_from_dict
from scraper.helpers.get_values_from_source import get_values_from_source


def add_columns_to_job_from_source(job: Job_values, values_source: WebDriver, values_to_add: Job_elements):
    '''In Python you do not have to return a dict from a function to change the dict'''

    values_to_add = get_values_from_source(
        values_source, values_to_add)

    add_columns_to_job_from_dict(job, values_to_add)
