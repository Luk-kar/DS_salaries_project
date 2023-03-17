@ECHO OFF
ECHO Running linter...
pylint config
pylint scraper
pylint _001_data_collection.py
pylint test