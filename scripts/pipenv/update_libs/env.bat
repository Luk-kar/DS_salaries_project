@ECHO OFF
ECHO updating pipfile...
pipenv run pip freeze > requirements.txt
ECHO Alternatively, you can update Pipfile with: pipenv install -r requirements.txt