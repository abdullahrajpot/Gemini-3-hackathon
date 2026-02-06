@echo off
echo ========================================
echo    ChronoVision AI - Quick Start
echo ========================================
echo.
echo Starting background collector...
python run_background.py
echo.
echo Starting search interface...
timeout /t 2 /nobreak >nul
python -m streamlit run search_app.py
