@echo off
SET PYTHON=C:\Users\hp\AppData\Local\Programs\Python\Python313\python.exe
echo Starting AI SOP Generator on port 8080...
%PYTHON% -m uvicorn backend.main:app --host 127.0.0.1 --port 8080 --reload
pause
