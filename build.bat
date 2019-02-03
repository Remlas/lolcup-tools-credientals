@echo off
pyinstaller --clean --onefile --name server --icon=server.ico main.py
PAUSE