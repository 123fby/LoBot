@echo off
chcp 65001 >nul
cd /d %~dp0

call .venv\Scripts\activate.bat

setlocal enabledelayedexpansion

echo import psutil, os, time > monitor.py
echo process = psutil.Process(os.getpid()) >> monitor.py
echo while True: >> monitor.py
echo     try: >> monitor.py
echo         mem = process.memory_info().rss / 1024 / 1024 >> monitor.py
echo         cpu = process.cpu_percent(interval=0.1) >> monitor.py
echo         print(f"[Memory] Python Usage: {mem:.2f} MB | CPU: {cpu:.1f}%%", end='\r') >> monitor.py
echo         time.sleep(1) >> monitor.py
echo     except KeyboardInterrupt: >> monitor.py
echo         break >> monitor.py

start /b python monitor.py

timeout /t 1 /nobreak >nul

python bot.py

taskkill /f /im python.exe /fi "WINDOWTITLE eq Python" >nul 2>&1
del monitor.py

pause