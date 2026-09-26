@echo off
echo Starting Travel Blog Backend...
call venv\Scripts\activate.bat
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
