# Python
import csv
import os
import sys
from typing import Literal
import _csv


# Internal
from scraper.config.get import get_path_csv_raw, get_encoding
from scraper._types import Job


Mode = Literal["w", "a"]


class CSV_Writer():

    def __init__(self, csv_path: str) -> None:
        self.csv_path = csv_path
        self.directory_path = os.path.dirname(csv_path)
        self.encoding = get_encoding()
        self.counter = 1

    def write_observation(self, observation: Job):

        if self.counter == 1:
            self.write_header(observation)

        self.write_row(observation)

        self.counter += 1

    def write_row(self, row: Job):
        '''
        appends list of tuples in specified output csv file
        a tuple is written as a single row in csv file
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

        file_path = self.csv_path
        encoding = self.encoding

        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)

        self._my_write_row(header, file_path, "w", encoding)

    def _my_write_row(self, row: tuple, file_path: str, mode: Mode, encoding: str):

        with open(file_path, mode, newline='', encoding=encoding) as csv_file:

            csv_writer = csv.writer(csv_file)

            try:
                csv_writer.writerow(row)

            except csv.Error as error:
                self._print_write_error(file_path, csv_writer, error)

    def _print_write_error(self, file_path: str, csv_writer: _csv.writer, error: csv.Error):

        sys.exit(
            f'File:\n\
                    {file_path}\n\
                    Line:\
                    \n{csv_writer.line_num}\
                    \n Error:\
                    \n{error}'
        )

    def _convert_dict_values_to_tuple(self, dictionary: dict) -> tuple:
        return tuple(dictionary.values())


class CSV_Writer_RAW(CSV_Writer):

    def __init__(self) -> None:
        super().__init__(
            get_path_csv_raw()
        )
