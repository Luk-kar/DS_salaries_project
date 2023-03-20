'''
Mostly used during debugging to remove unnecessary scraped data
'''
# Python
import os

# Internal
from scraper.config.get import get_path_csv_raw

raw_folder = os.path.dirname(get_path_csv_raw())
is_answer = False

while not is_answer:
    answer = input(
        f"Are you sure to delete all CSV files in?:\n{raw_folder}\nY/N: ")
    if answer in ["Y", "y", "Yes", "YES", "yes"]:
        is_answer = True
        pass
    elif answer in ["N", "n", "No", "NO", "no"]:
        exit()

files = os.listdir(raw_folder)
files_to_remove = []

for file in files:
    if file.endswith(".csv"):
        files_to_remove.append(os.path.join(raw_folder, file))

print(f"\rIn folder {raw_folder}:")
if files_to_remove:
    for file in files_to_remove:
        os.remove(file)
        print(f"\rREMOVED FILE: {os.path.basename(file)}")
else:
    print("\rNO FILES TO DELETE!")
