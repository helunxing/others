from datetime import datetime
import subprocess
import datetime

import os


class renametool:
    # TODO 按名称排序再读取
    # TODO 生成命名计划后,询问是否执行
    @staticmethod
    def get_photo_softwarestr_taken(filepath):
        cmd = "exiftool -software '%s'" % filepath
        output = subprocess.check_output(cmd, shell=True)
        lines = output.decode("utf8").split("\n")
        for l in lines:
            if "Software" in l:
                return l.split(': ')[1]
        return ''

    @staticmethod
    def get_photo_datestr_taken(filepath):
        """Gets the date taken for a photo through a shell."""
        cmd = "exiftool -DateTimeOriginal -createdate -model '%s'" % filepath
        output = subprocess.check_output(cmd, shell=True)
        lines = output.decode("utf8").split("\n")

        havecd = False

        for l in lines:
            if "Create Date" in l or "Date/Time Original" in l:
                havecd = True
                datetime_str = l.split(": ")[1]
                if datetime_str.endswith("+08:00"):
                    datetime_str = datetime_str[:-6]
                dt = datetime.datetime.strptime(
                    datetime_str, "%Y:%m:%d %H:%M:%S")
            if "iPhone" in l and filepath.endswith('.mov'):
                # 修正苹果视频的时差
                dt += datetime.timedelta(hours=8)
        # raise DateNotFoundException(
        #     "No EXIF date taken found for file %s" % filepath)
        if not havecd:
            return ''
        return dt.strftime("%y%m%d_%H%M%S")

    @staticmethod
    def create_repli_str(old_file_path, new_file_path, exte_name):
        cnt = 0
        repli_str = ''
        if new_file_path+repli_str+exte_name == old_file_path:
            return old_file_path
        while os.path.exists(new_file_path+repli_str+exte_name):
            cnt += 1
            repli_str = 'P%d' % cnt
        return repli_str

    @staticmethod
    def rename_single_folder(p):
        if not p.endswith('/'):
            p += '/'
        for file_name in os.listdir(p):
            renametool.rename_single_file(p, file_name)

    @staticmethod
    def rename_single_file(p, file_name):

        if '.' not in file_name or file_name.startswith('.') or os.path.isdir(p+file_name):
            return

        if len(file_name.split('.')[0]) == 13 and ' ' not in file_name:
            # TODO 合法文件名判断函数
            return

        old_file_path = p+file_name
        new_file = old_file_path[:]
        exte_name = '.'+file_name.split('.')[-1]

        # 获取新文件名
        if file_name.startswith('IMG_20') or file_name.startswith('VID_20'):
            new_file = p+file_name[6:-1*len(exte_name)]
        else:
            date_str = renametool.get_photo_datestr_taken(old_file_path)
            if not date_str:
                return
            new_file = p + date_str

        print('renaming %s' % file_name, end='\t')

        # 判断重复
        repli_str = renametool.create_repli_str(
            old_file_path, new_file, exte_name)

        # 执行改名
        new_file_path = new_file+repli_str+exte_name
        if old_file_path != new_file_path:
            os.rename(old_file_path, new_file_path)
            print('renamed as %s' % new_file_path.split('/')[-1])
        else:
            print('same')


p = '/Volumes/Untitle/DCIM/101_FUJI'

renametool.rename_single_folder(p)

# renametool.rename_single_file("/Users/h/Downloads/", "IMG_0711.JPG")

# 开发参考 https://juejin.cn/post/6844904158269702151
# 开发想法：读取目录下所有文件名，生成重命名计划，统一生成


# os.listdir(p)

# print(sorted())

# print(os.walk(p))
