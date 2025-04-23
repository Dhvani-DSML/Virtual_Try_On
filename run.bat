@echo off
echo Starting Virtual Try-On Application...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the Flask application
python app.py

:: Keep the window open if there's an error
pause 