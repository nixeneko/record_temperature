#!/usr/bin/env python3
# coding: utf-8

import datetime
import os
import glob
import sys
import re

import settings

# ad hoc
temperature_file = settings.DS18B20_TEMPERATURE_FILE
temp_log_dir = settings.DS18B20_TEMP_LOG_DIR
#TEMP_LOG_DIR = "temp_log"
MONTH_DIR = "month"
month_dir_path = os.path.join(temp_log_dir, MONTH_DIR)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists(month_dir_path):
    os.makedirs(month_dir_path)

today = datetime.date.today()

# To get the newest date already written in files
month_files = glob.glob(os.path.join(month_dir_path, "*.tsv"))
# Take the newest one
newest_month_fn = None 
newest_date_str = ""
for fn in sorted(month_files, reverse=True):
    r = re.match(r".*\d{4}-\d{2}\.tsv$", fn)
    if r: # newest month file
        newest_month_fn = fn
        with open(newest_month_fn, "r") as f:
            for line in f:
                vals = line.strip().split("\t")
                if len(vals) == 3:
                    newest_date_str = vals[0]
        break

newest_date = None
if newest_date_str:
    newest_date = datetime.date.fromisoformat(newest_date_str)

# Reads files to extract min and max day temperatures,
# and writes them in file(s).
lines_to_write = {} # group by month
fns = glob.glob(os.path.join(temp_log_dir, "*/*.tsv"))
for fn in sorted(fns):
    date_str, _ = os.path.splitext(os.path.basename(fn))
    try:
        date = datetime.date.fromisoformat(date_str)
    except ValueError: # Ignores invalid date_str
        continue
    if newest_date and (date <= newest_date):
        continue
    # Ignores today
    if date == today:
        continue
    # Reads file to get max and min temps
    temp_min = sys.float_info.max
    temp_max = sys.float_info.min
    with open(fn, "r") as f:
        for line in f:
            vals = line.strip().split("\t")
            if len(vals) == 2:
                temp = float(vals[1])
                if temp_min > temp:
                    temp_min = temp
                if temp_max < temp:
                    temp_max = temp
    line_to_write = "{}\t{}\t{}\n".format(date_str, temp_min, temp_max)
    print("{}: min {}, max {}".format(date_str, temp_min, temp_max))
    month = date_str.rsplit("-", 1)[0]
    if month not in lines_to_write:
        lines_to_write[month] = []
    lines_to_write[month].append(line_to_write)

for month in lines_to_write:
    filename = os.path.join(month_dir_path, month + ".tsv")
    with open(filename, "a") as w:
        w.writelines(lines_to_write[month])
