import os
import time

files_path = 'C:\\'

file_names = os.listdir(files_path)

for name in file_names:
    time_pre = name[:16]
    temp_time = time.strptime(time_pre, '%d-%b-%Y-%H%M')
    res_time = time.strftime('%Y-%m-%d %H-%M', temp_time)
    os.rename(files_path+name, files_path+res_time+name[16:])
