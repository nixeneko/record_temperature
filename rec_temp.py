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
for logdir, func in func_logdir_pairs:
    dirpath = os.path.join(logdir, year)
    try:
        data = func()
    except subprocess.CalledProcessError:
        continue
    if data is None:
        continue
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    filename = now.strftime("%Y-%m-%d") + ".tsv"
    filepath = os.path.join(logdir, year, filename) 
    
    with open(filepath, "a") as w:
        data_str = "\t".join([str(datum) for datum in data])
        w.write(nowstr + "\t" + data_str + "\n")

