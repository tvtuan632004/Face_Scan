@echo off
echo Dang khoi dong Web Server...
start python app.py
timeout /t 3
start http://127.0.0.1:5000
echo Server da chay. Hay giu cua so nay mo.
pause
