@echo off
title 📱 Launching Mobile Price Prediction App
color 0F
echo =======================================
echo   Starting Mobile Price App...
echo =======================================
echo.

REM Optional: Activate virtual environment
REM call venv\Scripts\activate

REM Start Streamlit app
streamlit run main.py

echo.
echo App closed. Press any key to exit.
pause > nul