from typing import Union

Job_Default = str
Job_Similar = list[str]
Job_Titles = dict[str, Union[Job_Default, Job_Similar]]
Job_Number = int
Url = dict[str, str]
Driver_Path = str
Debug_Mode = bool
Config = dict[str, Union[Job_Titles, Job_Number, Url, Driver_Path, Debug_Mode]]
