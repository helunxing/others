import piexif
import datetime
import os

# https://pypi.org/project/piexif/
# https://piexif.readthedocs.io/en/latest/


class exif_edit:
    # 自文件夹修正偏移
    def offset_form_fder(self, src_addr, dtn_addr, time_offset):
        for src_file_addr in os.listdir(src_addr):
            kind = src_file_addr.split('.')[1].lower()
            if kind != 'jpg':
                continue
            full_src_file_addr = src_addr+src_file_addr
            full_dtn_file_addr = dtn_addr+src_file_addr
            print(full_src_file_addr)
            print(full_dtn_file_addr)
            source_sess = piexif.load(full_src_file_addr)
            self.edit_time_by_offset(
                source_sess, full_dtn_file_addr, time_offset)

    # 将单个照片按照偏移量更正为为正确的时间
    def edit_time_by_offset(self, exif_source, destin_addr, time_offset):
        # 参数：源文件的连接，目标文件的地址，时间偏移量
        tags = [36868, 36867]
        for tag in tags:
            # print(exif_source["Exif"][tag])
            # print('相片内时间')

            time_str = str(exif_source["Exif"][tag], encoding='utf-8')
            # 将载入的时间转化为字符串

            time = datetime.datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S")
            # 将字符串转化为时间对象

            time = time + time_offset
            time_str_before_bytes = str(time).replace('-', ':')
            time_bytes = bytes(time_str_before_bytes, encoding="utf8")
            # 时间对象转化回二进制

            exif_source["Exif"][tag] = time_bytes  # 覆盖时间
            # print(exif_source["Exif"][tag])
            # print('修改后照片时间')

        dump = piexif.dump(exif_source)  # 卸下exif
        piexif.insert(dump, destin_addr)  # 修正后时间写回

    # 查看tag，字段内容，name三者的对应关系
    def view(self, exif_source):
        for ifd in ("0th", "Exif", "GPS", "1st"):
            for tag in exif_source[ifd]:
                name = piexif.TAGS[ifd][tag]["name"]
                if 'offset' in name.lower() or 'zone' in name.lower():
                    print(piexif.TAGS[ifd][tag]["name"], exif_source[ifd][tag])

        # for ifd in ("0th", "Exif", "GPS", "1st"):
        #     for tag in exif_source[ifd]:
        #         name = piexif.TAGS[ifd][tag]["name"]
        #         if 'timezone' in name.lower():
        #             print("编号："+str(tag)+";\n" + name+";")
        #             print(exif_source[ifd][tag])

        # for ifd in ("0th", "Exif", "GPS", "1st"):
        #     for tag in exif_source[ifd]:

        #         if '02' in value.lower():
        #             print(piexif.TAGS[ifd][tag]["name"], exif_source[ifd][tag])

    # 将所有与gps有关的exif信息复制到目标照片
    def copy_GPS(self, exif_source, exif_destin):
        GPS_arr = []
        for ifd in ("0th", "Exif", "GPS", "1st"):
            for tag in exif_source[ifd]:
                name = piexif.TAGS[ifd][tag]["name"]
                if 'gps' in name.lower():
                    GPS_arr.append([tag, exif_source[ifd][tag]])

        for i in GPS_arr:
            exif_source["Exif"][i[0]] = i[1]  # 覆盖时间
            # print(exif_source["Exif"][tag])
            # print('修改后照片时间')

        dump = piexif.dump(exif_source)
        piexif.insert(dump, exif_destin)  # 修正后时间写回
