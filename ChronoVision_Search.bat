@echo off
echo Starting ChronoVision Search Interface...
start http://localhost:8501
python -m streamlit run search_app.py
