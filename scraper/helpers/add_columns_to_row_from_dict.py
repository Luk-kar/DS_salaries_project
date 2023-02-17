
# Internal
from scraper._types import Job, Job_elements


def add_columns_to_row_from_dict(job: Job, job_description: Job_elements) -> Job:
    '''updating value job values'''

    for key, value in job_description.items():
        job[key] = value["value"]
