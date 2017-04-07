# Python 3.5
# Script that invokes web scrapper at a random time during the working hours.

from datetime import datetime
import time
import random
import threading
import requests
import scrapper_deptford
from config import deptford_upload_url

work_start = 9
work_end = 16

# TODO SET THIS!
download_now = True
# =========

def main():

    current_time = datetime.now()
    current_hour = current_time.hour

    if download_now:
        download_all_data()
    else:
        if current_hour >= 0 and current_hour < work_start:
            print('Will download today')
            schedule_next_download("today")
        elif current_hour >= work_start and current_hour < work_end:
            print('Downloading now')
            download_all_data()
            schedule_next_download("tomorrow")
        elif current_hour >= work_end:
            print('Will download tomorrow')
            schedule_next_download("tomorrow")
        else:
            print('Error!')

def download_all_data():

    data = scrapper_deptford.scrape_data()
    
    session = requests.Session()
    returned = session.post(
        url=deptford_upload_url,
        data=data.encode('utf-8')
        )
    print(returned.text)

def schedule_next_download(day):
    download_at_hour = random.randint(work_start, work_end)
    download_at_minute = random.randint(0, 60)

    if day == "today":
        delay = ((download_at_hour - datetime.now().hour) * 60 + (download_at_minute - datetime.now().minute)) * 60    
    elif day == "tomorrow":
        delay = 86400 - ((download_at_hour - datetime.now().hour) * 60 + (download_at_minute - datetime.now().minute)) * 60
    else:
        print('Error! Could not schedule!')

    threading.Timer(delay, download_all_data).start()
    print('Will update data in', delay/3600, 'hours')

if __name__ == "__main__":
    main()