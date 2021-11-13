from datetime import datetime

from renameby_exif_or_name import renametool as rt

ori_path = ''

lr_path = ''


class filter_file:
    def __init__(self, ori_path, *other_paths):
        if input('filter by software? y/n:') == 'y':
            for path in [ori_path] + list(other_paths):
                print('filtering %s' % path)
                filter_file.filter_by_software(path)
            return

        self.dic = {}
        # for path in other_paths:
        # print(path)
        self.create_dic()

    def create_dic(self,):
        p = ''
        rt.get_photo_datestr_taken(p)

    @staticmethod
    def filter_by_software(path):
        pass


filter_file(ori_path, lr_path)
