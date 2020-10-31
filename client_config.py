#!/usr/bin/python
import os
import configparser
class client_config():
    def __init__(self, path):
        self.config_path = path
        self.is_debug = False
        self.log_file = None
    def get_config(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.config_path)
            self.is_debug = config["DEFAULT"].getboolean("is_debug")
            self.log_file = config["DEFAULT"]["log_file"]
        except Exception as e:
            print ("client config error:%s" %(e))
    def get_debug(self):
        return self.is_debug
    def get_log_file(self):
        return self.log_file