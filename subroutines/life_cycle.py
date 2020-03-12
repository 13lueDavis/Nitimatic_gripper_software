import sys
import os
sys.path.append('../')
from gripper_v2 import Gripper

import glob
import time
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
import csv
from datetime import datetime

def gatherData():
    data = ''
    for sample in range(100):
        data += gripper.receive()
        data += '\n'

        time.sleep(0.02)

    print(data)

    dt = str(datetime.now()).replace(' ', '_')
    with open('data/life_cycle_initial/data_'+dt+'.csv', 'w+') as csvDataFile:
        csvDataFile.write(data)
    print(len(glob.glob('data/life_cycle_initial/*.csv')),' saved : ',dt)

if __name__ == '__main__':

    try:
        gripper = Gripper('/dev/cu.usbserial-1420')
    except:
        gripper = Gripper()

    scheduler = BackgroundScheduler()
    scheduler.add_job(gatherData, 'interval', seconds=10)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            gripper.setSMACurrent(0.0)
            time.sleep(0.7)
            gripper.setSMACurrent(0.4)
            time.sleep(0.7)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
