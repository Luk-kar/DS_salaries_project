# Internal
from scraper.config.get import get_NA_value


def parse_employees(job: dict):
    """
    Parses the 'Employees' field of a job dictionary if it is not a NA value.

    Args:
        job (dict): The dictionary containing job information.

    Returns:
        None. This function does not return anything. 
        The job dictionary is modified in place
    """

    na_value = get_NA_value()

    if job['Employees'] != na_value:
        job['Employees'] = job['Employees'].replace("Employees", "").strip()
