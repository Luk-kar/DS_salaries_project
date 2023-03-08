'''
This module provides functions for loading configuration and URL data 
from a YAML file and returning it in a structured format, 
including the get_config() function which returns a Config object 
and the get_url() function which returns a HTTP string. 
It imports the yaml library and uses the SafeLoader to safely load the YAML data.
'''
# Python
import os
import platform
from datetime import datetime

# External
import yaml
from yaml.loader import SafeLoader
from pathvalidate import sanitize_filepath
from pathvalidate._common import PathType

# Internal
from scraper.config._types import Config, Url, JobDefault, NA_value


def get_config(path: str = "scraper\\config\\data.yaml") -> Config:
    '''
    Loads configuration data from a YAML file and returns it as a Config object.

    Args:
        path (str): Path to the YAML file to be loaded. Default is "scraper\\config\\data.yaml".

    Returns:
        Config: A Config object representing the configuration data loaded from the file.
    '''

    with open(path, encoding="utf-8") as file:
        return yaml.load(file, Loader=SafeLoader)


def get_url(url: Url, job_title: JobDefault) -> str:
    '''
    Constructs a HTTP URL string using the given `url` dictionary and `job_title`.

    Args:
        url (Url): A dictionary containing keys for constructing the HTTP URL string.
        job_title (JobDefault): The default job title to use in the HTTP URL string.

    Returns:
        str: The constructed HTTP URL string.
    '''

    http = url['001_base'] + job_title + \
        url['002_keyword'] + job_title + \
        url['003_location']

    return http


config = get_config()


def _get_path_csv(directory: str,
                  job_title: str = config['jobs_titles']['default'],
                  extension: str = "csv"
                  ) -> str:
    '''
    Returns a string representing the file path for a CSV file to be written. 

    Args:
        directory (str): A string representing the directory name for the CSV file.
        job_title (str): A string representing the job title. 
        Default is `config['jobs_titles']['default']`.
        extension (str): A string representing the file extension. Default is "csv".

    Returns:
        str: A string representing the file path where the CSV file should be written.

    Raises:
        OSError: If the generated file path is not a valid file path.
    '''

    directory_main = config['output_path']['main']
    directory_target = os.path.join(directory_main, directory)
    jobs_title = job_title.replace(" ", "_")
    jobs_title_sanitized = _my_sanitize_filepath(jobs_title)
    date_time = datetime.now().strftime("%d-%m-%Y_%H-%M")

    database_file = f"{jobs_title_sanitized}_{date_time}.{extension}"

    csv_file_target = os.path.abspath(
        os.path.join(directory_target, database_file))

    if is_possible_path(csv_file_target):
        return csv_file_target
    else:
        raise OSError(f"Wrong file path:\n{csv_file_target}")


def get_path_csv_raw() -> str:
    '''
    Returns the absolute path to the file where "the raw" 
    CSV files are saved based on the configuration.

    Returns:
        str: The absolute path to the directory where "the raw" CSV files are saved.
    '''

    return _get_path_csv(config['output_path']['raw'])


def get_path_csv_clean() -> str:
    '''
    Returns the absolute path to the file where "the clean" 
    CSV files are saved based on the configuration.

    Returns:
        str: The absolute path to the directory where "the clean" CSV files are saved.
    '''

    return _get_path_csv(config['output_path']['clean'])


def get_NA_value() -> NA_value:
    '''
    Returns the 'NA_value' from the configuration file.

    Returns:
        NA_value: A value representing the 'NA_value' defined in the configuration file.
    '''

    return get_config()['NA_value']


def get_encoding() -> str:
    '''
    Returns the encoding type to use for reading and writing csv as specified in the config file.

    Returns:
    - str: The encoding type to use for reading and writing files.
    '''
    return get_config()['encoding']


def is_possible_path(file_path: str) -> bool:
    '''
    Checks if the file path is valid and does not contain any illegal characters.

    Args:
        file_path (str): The file path to check.

    Returns:
        bool: True if the file path is valid 
        and does not contain any illegal characters, False otherwise.
    '''

    # https://stackoverflow.com/a/67119769/12490791
    is_possible = file_path == _my_sanitize_filepath(file_path)

    return bool(
        os.path.exists(file_path) or is_possible
    )


def _my_sanitize_filepath(path: str) -> PathType:
    '''
    Sanitize a file path for the current operating system.

    Args:
        path (str): A file path to sanitize.

    Returns:
        str: A sanitized version of the file path, 
        which is compatible with the current operating system.

    Raises:
        TypeError: If the input path is not a string.
    '''
    return sanitize_filepath(
        path, platform=platform.system())
