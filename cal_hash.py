import os
import subprocess


class cal_hash:
    @staticmethod
    def cal_file(filepath):
        cmd = "shasum '%s'" % filepath
        output = subprocess.check_output(cmd, shell=True)
        h = output.decode("utf8").split(" ")
        return h[0]


path = "/Volumes/home"

a = cal_hash.cal_file(path)
b = cal_hash.cal_file(path)

print(a == b)

pass
