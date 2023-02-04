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
from typing import Union

JobDefault = str
JobSimilar = list[str]
JobTitles = dict[str, Union[JobDefault, JobSimilar]]
JobNumber = int
Url = dict[str, str]
DriverPath = str
DebugMode = bool
Config = dict[str, Union[JobTitles, JobNumber, Url, DriverPath, DebugMode]]
