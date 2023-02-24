'''
This module provides a function to update a job dictionary 
with values obtained from an external web page source,
using XPATH expressions to extract the values.
'''

# Internal
from scraper._types import Job_elements, Job_values, MyWebElement
from ._dict_value_adder import add_values_to_job_from_dict
from ._element_value_getter import get_values_from_element


def get_and_add_element_value(
    job: Job_values,
    values_source_element: MyWebElement,
    job_values_to_add: Job_elements
):
    '''
    Update job dictionary using values from an external source (web page).

    Args:
    - job (dict): a dictionary representing a job and its properties.
    - values_source (webdriver): representing the source of the job properties.
    - values_to_add (dict): a dictionary representing the properties of a job and their associated XPATH expressions.

    Returns:
    - None

    It extracts the values from the web page using XPATH expressions and updates
    the associated job property in the job dictionary. 
    '''

    job_values_to_add = get_values_from_element(
        values_source_element, job_values_to_add)

    add_values_to_job_from_dict(job, job_values_to_add)
