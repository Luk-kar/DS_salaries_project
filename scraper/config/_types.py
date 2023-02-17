"""
This module defines several types used to describe the structure of a configuration data object.
The Config type is a dictionary that contains several other types:

    * JobTitles is a dictionary with keys "default" and "similar" that
    hold the default job title as a string and a list of similar job titles as strings.

    * JobNumber is an integer representing the number of jobs to retrieve.

    * Url is a dictionary holding different parts of a URL as strings.

    * DriverPath is a string representing the path to a web driver.

    * DebugMode is a boolean indicating whether debug mode is on or off.

    * All other types (JobDefault, JobSimilar, JobTitles, JobNumber, Url,
    DriverPath, and DebugMode) are used to describe the structure of these values.
"""
from typing import Annotated, Literal
from annotated_types import Gt

JobDefault = str
JobSimilar = list[str]
JobTitles = dict[str, {'default': JobDefault,  # type: ignore[valid-type, misc]
                       'similar': JobSimilar}]  # type: ignore[valid-type, index]
JobNumber = Annotated[int, Gt(0)]
Url = dict[str, str]
DriverPath = str
DebugMode = bool
NA_value = Literal[-1]
Config = dict[str, {'jobs_titles': JobTitles, 'jobs_number': JobNumber,  # type: ignore[valid-type, misc]
                    'url': Url, 'driver_path': DriverPath, 'debug_mode': DebugMode, "NA_value": NA_value}]  # type: ignore[valid-type, index]
