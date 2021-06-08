#!/usr/bin/env python3
# coding: utf-8

import subprocess
import datetime
import os

import settings

func_logdir_pairs = settings.FUNC_LOGDIR_PAIRS
#data_get_funcs = settins.DATA_GET_FUNCS
#data_log_dirs = settings.DATA_LOG_DIRS

# change current directory to the directory this script is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

now = datetime.datetime.now()
nowstr = now.isoformat().split(".")[0]
year = str(now.year)
for func, logdir in func_logdir_pairs:
    dirpath = os.path.join(logdir, year)
    data = func()
    if data is None:
        continue
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    filename = now.strftime("%Y-%m-%d") + ".tsv"
    filepath = os.path.join(logdir, year, filename) 
    
    with open(filepath, "a") as w:
        w.write(nowstr + "\t" + str(temperature) + "\n")

