'''
The module adds values from a dictionary to a job dictionary.
'''
# Internal
from scraper._types import Job_values, Job_elements


def add_columns_to_job_from_dict(
    job: Job_values,
    values_to_add: Job_elements
):
    """
    Adds the values in the `values_to_add` dictionary to the `job` dictionary.

    Parameters:
        - job (Job): A dictionary containing job data to which the values will be added.
        - values_to_add (Job_elements): A dictionary containing the keys 
        and values to be added to the `job` dictionary.

    Returns:
        - None: This function does not return a value; 
        it updates the `job` dictionary in place.
    """

    for column, field in values_to_add.items():
        job[column] = field["value"]
