import os
import xml.etree.ElementTree as ET


def merge_gpx(sour_folder, dest_file):
    '''
    将多个gpx文件的轨迹和标注点合并
    '''
    sour_folder += '' if sour_folder.endswith('\\') else '\\'

    sour_list = os.listdir(sour_folder)
    print('共有%s个文件' % (len(sour_list)))

    with open(dest_file, "wb") as fo:
        fo.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.1">')

        xmlns = '{http://www.topografix.com/GPX/1/1}'

        for i, sour_file in enumerate(sour_list):
            print('正处理第%s个文件' % (i+1), end='')

            tree = ET.parse(sour_folder+sour_file)
            root = tree.getroot()
            # root.tag = root.tag[35:]

            wpts = root.findall(xmlns+'wpt')
            trks = root.findall(xmlns+'trk')
            for item in wpts+trks:
                # del item.attrib['xmlns:ns']
                # 标记点标注改为文件名
                for d in item.findall(xmlns+'desc'):
                    d.text = sour_file
                fo.write(b'\n')
                fo.write(ET.tostring(item, encoding="utf-8"))

            print(' 已完成')

        fo.write(b'\n</gpx>')
        print('文件生成完成')


if __name__ == "__main__":
    merge_gpx("C:\\workspace\\gpxs", "C:\\workspace\\gpxs_out.gpx")
