@echo off
:: =========================================================================
:: DiagnoveraAI Pro - Automated Run Script
:: =========================================================================
:: This script automates the process of installing dependencies and 
:: running the main Flask web application.
:: =========================================================================

echo =======================================================
echo Checking and Installing Dependencies...
echo =======================================================
:: Install dependencies from requirements.txt
:: Using --quiet to reduce terminal spam, remove it to see detailed logs
pip install -r requirements.txt
pip install seaborn

echo.
echo =======================================================
echo Starting the DiagnoveraAI Pro Web Application...
echo =======================================================
echo The server will start shortly.
echo Open your browser and go to: http://127.0.0.1:5000/
echo Press CTRL+C in this window to stop the server.
echo =======================================================
echo.

:: Run the Flask application
python app.py

pause
