'''
The module _company_name_parser takes a job dictionary as input 
and modifies the 'Company_name' field of the dictionary by removing rating e.g. "4.0" 
and any leading/trailing whitespaces if it is not a NA value.
'''
# Python
import re

# Internal
from scraper.config.get import get_NA_value


def parse_company_name(job: dict[str, str]):
    '''
    Parses the 'Company_name' field of a job dictionary if it is not a NA value.

    Args:
        - job (dict): The dictionary containing job information.

    Returns:
        - None. This function does not return anything. 
        - The job dictionary is modified in place
    '''

    na_value = get_NA_value()

    if job['Company_name'] != na_value:

        rating_v1 = str(job['Rating'])
        rating_v2 = rating_v1.replace(".", ",")

        company_name = re.sub('\n|\t|', '', job['Company_name']).strip()

        ratings = [rating_v1, rating_v2]

        for rating in ratings:

            company_name = company_name.replace(rating, "")

        job['Company_name'] = company_name
