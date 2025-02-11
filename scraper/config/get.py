'''
This module provides functions for loading configuration and URL data 
from a YAML file and returning it in a structured format, 
including the get_config() function which returns a Config object 
and the get_url() function which returns a HTTP string. 
It imports the yaml library and uses the SafeLoader to safely load the YAML data.
'''
# Python
import os
from datetime import datetime

# External
import yaml
from yaml.loader import SafeLoader
from pathvalidate import sanitize_filepath, sanitize_filename

# Internal
from scraper.config._types import Config, Url, JobDefault, NA_value, Location


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


def _get_path_csv(
    directory: str,
    job_title: str = config['jobs_titles']['default'],
    location: Location = "",
    extension: str = "csv"
) -> str:
    '''
    Returns a string representing the file path for a CSV file to be written. 

    Args:
        directory (str): A string representing the directory name for the CSV file.
        job_title (str): A string representing the job title.
        location (str): A string representing the location for the job. 
        Default is `config['jobs_titles']['default']`.
        extension (str): A string representing the file extension. Default is "csv".

    Returns:
        str: A string representing the file path where the CSV file should be written.

    Raises:
        OSError: If the generated file path is not a valid file path.
    '''

    directory_main = os.path.join(
        config['output_path']['main'], config['output_path']["raw"]
    )
    directory_target = os.path.join(directory_main, directory)
    jobs_title = job_title.replace(" ", "_")
    jobs_title_sanitized = sanitize_filename(jobs_title, platform="universal")
    location = location.replace(" ", "_")
    location_sanitized = sanitize_filename(location, platform="universal")
    date_time = datetime.now().strftime("%d-%m-%Y_%H-%M")

    database_file = f"{jobs_title_sanitized}_{location_sanitized}_{date_time}.{extension}"

    csv_file_target = os.path.abspath(
        os.path.join(directory_target, database_file))

    csv_file_target_sanitized = sanitize_filepath(
        csv_file_target,
        platform="auto"
    )

    return csv_file_target_sanitized


def get_path_csv_raw(
        job_title: JobDefault = config['jobs_titles']['default'],
        location: Location = config['locations']['default']
) -> str:
    '''
    Returns the absolute path to the file where "the raw" 
    CSV files are saved based on the configuration.

    Args:
        directory (str): A string representing the directory name for the CSV file.
        job_title (str): A string representing the job title.

    Returns:
        str: The absolute path to the directory where "the raw" CSV files are saved.
    '''

    return _get_path_csv(directory=job_title, location=location)


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
