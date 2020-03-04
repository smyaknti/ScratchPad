"""
Author: Soumyakanti (r.soumyakanti@gmail.com)
Last Modified: 4th March, 2020

Module to run the store_battle_logs.py continuously using shelve.
The store_battle_logs function has to be recurrently called from 
another module to continuously update the data.

Recommended time intervals:
900 seconds for Professional Players
1800 seconds for Casual to Semi Professional Players

"""


import time
import subprocess

while True:
    subprocess.call(
        ["python.exe", "/path/to/store_battle_logs.py"])

    #please make sure the path is properly set,
    #can take a few tries, if it fails to call, just
    #terminate the program using Ctrl+C and try 
    #changing the path

    time.sleep(300) #in seconds


#you can increase the time delay to anything you prefer,
#but for pro players it is recommended to have a delay of
#less than 15 minutes (900 seconds) just in case a 
#particular API call fails!