#!/usr/bin/env python3
# coding: utf-8

import subprocess
import datetime
import os

import settings
temperature_file = settings.TEMPERATURE_FILE
temp_log_dir = settings.TEMP_LOG_DIR
#TEMPERATURE_FILE = "/sys/bus/w1/devices/28-xxxxxxxxxxxxxx/w1_slave"
#TEMP_LOG_DIR = "temp_log"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

tfiles = subprocess.check_output(['cat',temperature_file]).decode('utf-8')
#print(tfiles)
now = datetime.datetime.now()
nowstr = now.isoformat().split(".")[0]
year = str(now.year)
dirpath = os.path.join(temp_log_dir, year)
if not os.path.exists(dirpath):
    os.makedirs(dirpath)
filename = now.strftime("%Y-%m-%d") + ".tsv"
filepath = os.path.join(temp_log_dir, year, filename) 
if tfiles.find("YES",30,60) != -1:
    idx = tfiles.find("t=",50,80)
    temperature = int(tfiles[idx+2:])/1000.0
    with open(filepath, "a") as w:
        w.write(nowstr + "\t" + str(temperature) + "\n")

