@echo off
:: 1. Move to the directory using explicit quotes
cd /d "C:\Users\PRS\project_1.0"

:: 2. Let's use the universal system path for python to make it bulletproof
python main.py >> windows_cron_log.txt 2>&1