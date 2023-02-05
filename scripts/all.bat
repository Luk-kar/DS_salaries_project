@ECHO OFF
ECHO Running all scripts...
call .\scripts\run_tests.bat
call .\scripts\check_types.bat
call .\scripts\run_linter.bat
call .\scripts\create_requirements.bat
call .\scripts\pipenv\update_libs\req.bat