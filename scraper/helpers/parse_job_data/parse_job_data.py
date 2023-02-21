# Internal
from .parse.parse_NA_values import parse_NA_values
from .parse.parse_numerical_values import parse_numerical_values
from .parse.parse_salary import parse_salary
from .parse.parse_easy_apply import parse_easy_apply
from .parse.parse_revenue import parse_revenue
from .parse.parse_employees import parse_employees


def parse_job_data(job: dict):
    """
    Cleans the input job dictionary by converting numeric 
    and percentage values to floats and integers.

    Args:
        job (dict): The job dictionary to be cleaned.
    """

    # The order of the operations is important!
    # parse_NA_values should be first!
    parse_NA_values(job)
    parse_numerical_values(job)
    parse_salary(job)
    parse_easy_apply(job)
    parse_employees(job)
    parse_revenue(job)
