'''
This module defines classes to handle writing to CSV files.
'''
# Python
import csv
import os
import sys
from typing import Literal


# Internal
from scraper.config.get import get_path_csv_raw, get_encoding
from scraper._types import Job


Mode = Literal["w", "a"]


class CSV_Writer():
    '''
    This class writes job posting to CSV files. 

    Attributes:
    - csv_path (str): Path to the CSV file.

    - directory_path (str): Path to the directory containing the CSV file.

    - encoding (str): The encoding of the CSV file.

    - counter (int): A counter used to keep track of the number of rows written.

    Methods:
    - write_observation(observation: Job): Write a row of job observation data to the CSV file.

    - write_row(row: Job): Writes a row of job observation data to the CSV file.

    - write_header(header: Job): Writes the header row to the CSV file.

    - _my_write_row(row: tuple | Job, file_path: str, mode: Mode, encoding: str): 
    A private method that writes a row to the CSV file.

    - _print_write_error(file_path: str, error: csv.Error): 
    A private method that prints an error message to the console 
    if there is an error writing to the CSV file.

    - _convert_dict_values_to_tuple(dictionary: dict) -> tuple: 
    A private method that converts a dictionary of job observation data to a tuple.

    '''

    def __init__(self, csv_path: str) -> None:

        self.csv_path = csv_path
        self.directory_path = os.path.dirname(csv_path)
        self.encoding = get_encoding()
        self.counter = 1

    def write_observation(self, observation: Job):
        '''
        Write a row of job observation data to the CSV file.

        Args:
        - observation (Job): A dictionary containing the job observation data 
        to write to the CSV file.

        '''

        if self.counter == 1:
            self.write_header(observation)

        self.write_row(observation)

        self.counter += 1

    def write_row(self, row: Job):
        '''
        Writes a row of job observation data to the CSV file.

        Args:
        - row (Job): A dictionary containing the job observation data to write to the CSV file.

        '''

        file_path = self.csv_path
        encoding = self.encoding

        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"To add row to the csv, you need a initialized file first.\
                    \nNon existing file:\
                    \n{file_path}")

        row_tupled = self._convert_dict_values_to_tuple(row)

        self._my_write_row(row_tupled, file_path, "a", encoding)

    def write_header(self, header: Job):
        '''
        Writes the header row to the CSV file.

        Args:
        - header (Job): A dictionary containing the header data to write to the CSV file.

        '''

        file_path = self.csv_path
        encoding = self.encoding

        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)

        self._my_write_row(header, file_path, "w", encoding)

    def _my_write_row(self, row: tuple | Job, file_path: str, mode: Mode, encoding: str):
        '''
        A private method that writes a row to the CSV file.

        Args:
        - row (tuple | Job): A tuple or dictionary containing the job observation data
          to write to the CSV file.
        - file_path (str): Path to the CSV file.
        - mode (Mode): Write mode ("w" for overwrite or "a" for append).
        - encoding (str): The encoding of the CSV file.

        '''

        with open(file_path, mode, newline="", encoding=encoding) as csv_file:

            csv_writer = csv.writer(csv_file)

            try:
                csv_writer.writerow(row)

            except csv.Error as error:
                self._print_write_error(file_path, error)

    def _print_write_error(self, file_path: str, error: csv.Error):
        '''
        A private method that prints an error message to the console 
        if there is an error writing to the CSV file.

        Args:
        - file_path (str): Path to the CSV file.
        - error (csv.Error): The error that occurred while writing to the CSV file.
        '''

        line_number = self.counter + 1  # + 1 (header)

        sys.exit(
            f'File:\n\
                    {file_path}\n\
                    Line:\
                    \n{line_number}\
                    \n Error:\
                    \n{error}'
        )

    def _convert_dict_values_to_tuple(self, dictionary: dict) -> tuple:
        '''
        A private method that converts a dictionary of job observation data to a tuple.

        Args:
        - dictionary (dict): A dictionary containing job observation data.

        Returns:
        - tuple: A tuple containing the values of the input dictionary.
        '''
        return tuple(dictionary.values())


class CSV_Writer_RAW(CSV_Writer):
    '''
    This class writes job information to the raw CSV file.

    Attributes:
    - None

    Methods:
    - __init__(): Constructs the CSV_Writer_RAW instance by calling 
    the parent class constructor with the path to the raw CSV file.

    '''

    def __init__(self) -> None:
        super().__init__(
            get_path_csv_raw()
        )
