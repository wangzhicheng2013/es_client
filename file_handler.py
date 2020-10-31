#!/usr/bin/python
import os
import global_instance
class file_handler():
    def __init__(self, path):
        self.dir_path = path
        self.file_list = []
    def get_file_list(self):
        try:
            file_list = os.listdir(self.dir_path)
            if not file_list:
                return False
            self.file_list = sorted(file_list, key = lambda x : os.path.getmtime(os.path.join(self.dir_path, x)))
            if (len(self.file_list) >= global_instance.g_latest_files_num):
                self.file_list = self.file_list[0:global_instance.g_latest_files_num]
            return True
        except Exception as e:
            global_instance.g_log.error("error:%s" %(e))
    def show_file_list(self):
        for file in file_list:
            path = self.dir_path + "/" + file
            print (path)
    def remove_file_list(self):
        for file in self.file_list:
            path = self.dir_path + "/" + file
            if os.path.isfile(path):
                os.remove(path)
    def clear_file_list(self):
        self.file_list = []
    def get_table_name(self, file):
        tmp_list = file.split(".")
        return tmp_list[0]

