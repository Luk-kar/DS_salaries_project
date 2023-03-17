@ECHO OFF
ECHO Running diagnostic tests...
coverage run -m unittest
coverage report -m
coverage html