# coding: utf-8
# あ
import subprocess

def get_func_read_data(temperature_file):
    return lambda: read_data(temperature_file)

def read_data(temperature_file):
    tfiles = subprocess.check_output(['cat',temperature_file]).decode('utf-8')
    if tfiles.find("YES",30,60) != -1:
        idx = tfiles.find("t=",50,80)
        temperature = int(tfiles[idx+2:])/1000.0
        return (temperature, )

    return None