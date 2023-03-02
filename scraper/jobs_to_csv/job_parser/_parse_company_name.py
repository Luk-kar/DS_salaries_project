'''
The module parse_revenue takes a job dictionary as input 
and modifies the 'Revenue_USD' field of the dictionary by removing "(USD)" 
and any leading/trailing whitespaces if it is not a NA value.
'''
# Internal
from scraper.config.get import get_NA_value


def parse_revenue(job: dict[str, str]):
    '''
    Parses the 'Revenue_USD' field of a job dictionary if it is not a NA value.

    Args:
        job (dict): The dictionary containing job information.

    Returns:
        None. This function does not return anything. 
        The job dictionary is modified in place
    '''

    na_value = get_NA_value()

    if job['Revenue_USD'] != na_value:

        job['Revenue_USD'] = job['Revenue_USD'].replace("(USD)", "").strip()
