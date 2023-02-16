
# Internal
from scraper._types import Job, Job_values


def add_columns_to_row_from_dict(job: Job, job_description: Job_values) -> Job:
    '''updating value job values'''

    for key, value in job_description.items():
        job[key] = value["value"]
