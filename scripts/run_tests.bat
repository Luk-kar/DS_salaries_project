@ECHO OFF
ECHO Running diagnostic tests...
coverage run tests.py
coverage report -m
coverage html