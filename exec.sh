#!/bin/bash

cd /home/kate/Dailyquotes || exit


#Activate virtual environment 
source venv/bin/activate

#Run all tasks sequentially

python3 quotefetcher.py

python3 emailsender.py

python3 adminsummary.py

#Add log
echo "$(date): Daily run completed" >> logs/exec.log
