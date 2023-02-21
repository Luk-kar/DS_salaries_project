def parse_easy_apply(job: dict):
    """
    Parse the 'Easy_apply' field in the input job dictionary.

    Args:
        job (dict): The job dictionary to be cleaned.
    """

    job['Easy_apply'] = bool(job['Easy_apply'])
