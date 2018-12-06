import openpyxl
import datetime

import icalendar
import pytz


def cal_create(lsns_list, cal_temp_list):
    cal = icalendar.Calendar()

    # cal.add('prodid', 'test_prodid')
    # cal.add('version', '2.0')

    for lsn in lsns_list:

        # lsn_name = '日程名'
        # srt_time = datetime.datetime(2018, 1, 22, 8, 0, 0, tzinfo=tz)
        # end_time = datetime.datetime(2018, 1, 22, 10, 0, 0, tzinfo=tz)
        # lct = 'somewhere1'

        alerm_info = icalendar.Alarm()
        alerm_info.add('action', 'dispaly')
        alerm_info.add('trigger', datetime.timedelta(minutes=-90))
        alerm_info.add('discription', 'Reminder')

        e = icalendar.Event()
        for i in cal_temp_list:
            e.add(i, lsn[i])

        e.subcomponents = [alerm_info]
        cal.add_component(e)

    f = open('C:\\result.ics', 'wb')
    f.write(cal.to_ical())
    f.close()


class excel_trans:
    # 导入ics文件值的关键字列表
    cal_temp_list = [
        'summary',
        'dtstart',
        'dtend',
        'location',
        'rrule']
    # 节数与对应的开始时间
    lsn_num_sta_time = {}
    # 节数与对应的结束时间
    lsn_num_end_time = {}
    # 表格中偏移量及其含义
    cell_offset_means = {0: 'summary', 1: 'location',
                         2: 'thr_name', 3: 'period_and_lsn_num'}
    # 课程信息模板
    course_dict_temp = {'lsn_num': '', 'day_of_week': datetime.date(year=2018, month=9, day=3),
                        'dtstart': datetime.time(), 'dtend': datetime.time(),
                        'week_period': [], 'lsn_num_period': [],
                        'rrule': {}}
    fst_week_date = datetime.date(year=2018, month=9, day=3)

    def __init__(self):
        # week_num_date_rel={}
        self.course_dict_temp['day_of_week'] = self.fst_week_date

        for i in self.cell_offset_means.values():
            self.course_dict_temp[i] = ''
        lsn_num_time = dict(
            zip(range(1, 16), [datetime.time() for i in range(1, 16)]))

        tz = pytz.timezone('Asia/Shanghai')
        # 节数与对应的开始时间
        self.lsn_num_sta_time = lsn_num_time.copy()
        sta_temp = {1: [8, 0],
                    3: [9, 45],
                    6: [12, 15],
                    8: [14, 0],
                    11: [16, 30],
                    13: [19, 0]}
        for i in sta_temp:
            time = sta_temp[i]
            self.lsn_num_sta_time[i] = datetime.time(
                hour=time[0], minute=time[1], tzinfo=tz)

        # 节数与对应的结束时间
        self.lsn_num_end_time = lsn_num_time.copy()
        end_temp = {2: [9, 30],
                    4: [11, 15],
                    5: [12, 0],
                    7: [13, 45],
                    9: [15, 30],
                    10: [16, 15],
                    12: [18, 0],
                    14: [20, 30],
                    15: [21, 15]}
        for i in end_temp:
            time = end_temp[i]
            self.lsn_num_end_time[i] = datetime.time(
                hour=time[0], minute=time[1], tzinfo=tz)

    def excel_trans(self, source_file_addr):
        # print(type(wb))  # 数据类型
        # os.getcwd()  # 当前目录
        # os.chdir()  # 更改工作目录

        wb = openpyxl.load_workbook(source_file_addr)
        sheet = wb[wb.sheetnames[0]]
        courses = []

        # C~G：周一到周五
        # 3开始a[4]:名 地 师 节数。每隔4个，一共十五节。
        # 64到76：C编号、D课名、E开课时间、F开课周期、G师名、H地点
        for d_of_w_os in range(5):
            col_chr = chr(ord('c')+d_of_w_os)  # 日期所在的列的字母

            for lsn_offset in range(15):
                lsn_num = lsn_offset+1
                row_deoffset = 3+lsn_offset*4

                course = self.course_dict_temp.copy()

                for k, v in self.cell_offset_means.items():
                    row = str(row_deoffset+k)  # 行号等于未偏移量加偏移量
                    course[v] = sheet[col_chr+row].value if sheet[
                        col_chr + row].value != None else ''

                if '体操' in course[self.cell_offset_means[0]]:
                    course['l'] = course['period_and_lsn_num'][:-
                                                               2].split('周上(')
                    course['week_period'] = course['l'][0].split('-')
                    course['lsn_num_period'] = course['l'][1].split('-')

                    course['summary'] = '体操'
                    course['lsn_num'] = str(lsn_num)
                    course['day_of_week'] += datetime.timedelta(
                        days=d_of_w_os)
                    course['dtstart'] = datetime.datetime.combine(
                        course['day_of_week'],
                        self.lsn_num_sta_time[lsn_num])
                    course['dtend'] = datetime.datetime.combine(
                        course['day_of_week'],
                        self.lsn_num_end_time[lsn_num])

                    rep_freq = 'weekly'
                    rep_times = str(
                        int(course['week_period'][1])-int(course['week_period'][0])+1)
                    course['rrule'] = {'freq': rep_freq, 'count': rep_times}
                    course['feature'] = course['lsn_num_period'][0]
                    course['end_lsn_num'] = course['lsn_num_period'][1]

                    courses.append(course)

        self.merge(courses)
        return courses

    def merge(self, courses):
        last = 0
        i = 1
        while i < len(courses):
            if courses[i]['feature'] == courses[last]['feature']:
                if courses[i]['lsn_num'] == courses[i]['end_lsn_num']:
                    courses[last]['dtend'] = courses[i]['dtend']
                del courses[i]
            else:
                i += 1
                last += 1

    def out(self, course):
        print(course['feature'], course['summary'],
              course['location'], course['week_period'])
        print(course['dtstart'], course['dtend'])
        print()


e = excel_trans()

# addr = 'C:\\source.xlsx'
# lsns_list = e.excel_trans(addr)
# cal_create(lsns_list, e.cal_temp_list)

tz = pytz.timezone('Asia/Shanghai')
date = datetime.date(year=2018, month=12, day=3)
time = datetime.time(hour=13, minute=40, tzinfo=tz)
time2 = datetime.time(hour=15, tzinfo=tz)
test_list = [{
    'summary': '名称',
    'dtstart': datetime.datetime.combine(date, time),
    'dtend': datetime.datetime.combine(date, time2),
    'location': '位置',
    'rrule': {}}]
cal_create(test_list, e.cal_temp_list)

# 写了这个程序，我发现抽象业务逻辑的能力不强。
# 想写出易于修改、通用性强的代码并非易事。
