#!/bin/bash

echo Creating virtual environment...
python3 -m venv env

echo Activating virtual environment...
source env/bin/activate

echo Installing required packages...
pip3 install -r requirements.txt

echo Starting the application...
python3 app.py

read -p "Press [Enter] key to exit."
