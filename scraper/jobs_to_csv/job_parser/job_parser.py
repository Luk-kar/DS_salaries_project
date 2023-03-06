'''
This module provides a function for cleaning a job dictionary by parsing 
and converting numeric and percentage values to floats and integers, bools,
providing NA values, and expanding data by feature engineering
'''
# Internal
from ._na_values_parser import parse_na_values
from ._numerical_values_parser import parse_numerical_values
from ._easy_apply_parser import parse_easy_apply
from ._revenue_parser import parse_revenue
from ._employees_parser import parse_employees
from ._company_name_parser import parse_company_name


def parse_data(job: dict):
    '''
    Cleans the input job dictionary by converting numeric 
    and percentage values to floats and integers.

    Args:
        job (dict): The job dictionary to be cleaned.
    '''

    # The order of the operations is important!
    # 1. parse_na_values
    # 2. parse_revenue

    parse_na_values(job)
    parse_revenue(job)
    parse_company_name(job)
    parse_numerical_values(job)
    parse_easy_apply(job)
    parse_employees(job)
