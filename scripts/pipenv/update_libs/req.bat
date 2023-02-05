@ECHO OFF
ECHO updating pipfile...
pipenv install -r requirements.txt
ECHO Alternatively, you can update Pipfile with: pipenv run pip freeze ^> requirements.txt