from datetime import datetime
import os
import sys

#use this sample file to test 
print(os.getcwd())
def write_file(filename, data):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:
            f.write('\n'+data)

def print_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    date = "Current Time = " + current_time
    return date

write_file('test.txt',print_time())
print("complete")
locate_python = sys.exec_prefix
print(locate_python)