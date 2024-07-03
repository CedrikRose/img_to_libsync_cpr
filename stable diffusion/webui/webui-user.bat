@echo off

set PYTHON=.\venv\Scripts\python.exe
set GIT=git
set VENV_DIR=venv
set COMMANDLINE_ARGS=--api --xformers --no-half

call webui.bat
