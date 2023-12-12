import sys

log_DIR = "Log.txt"

def log_print(log_str):
    file = open(log_DIR,'a')
    sys.stdout = file
    from datetime import datetime; print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    print(log_str)
    file.close()
    sys.stdout = sys.__stdout__
