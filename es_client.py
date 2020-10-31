#!/usr/bin/python
import sys
import os
import signal
import time
import global_instance
from client_config import client_config
from json_utility import json_utility_instance
from file_handler import file_handler
from daemonize import daemonize
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
class es_client(file_handler):
    def __init__(self, path):
        super(es_client, self).__init__(path)
        self.es_data = []
        try:
            self.es = Elasticsearch([global_instance.ES_IP], http_auth = (global_instance.ES_USER, global_instance.ES_PASSWORD),
                                    port = global_instance.ES_PORT, sniff_on_start = True, sniff_on_connection_fail = True,  
                                    sniff_timeout = 60, timeout = 30)
        except Exception as e:
            global_instance.g_log.error("es init error:%s" %(e))
    def import_data(self):
        try:
            helpers.bulk(self.es, self.es_data)
            global_instance.g_log.info("es import count:%d" %(len(self.es_data)))
        except Exception as e:
            global_instance.g_log.error("es import error:%s" %(e))
    def import_files(self):
        for file in self.file_list:
            path = self.dir_path + "/" + file
            if not os.path.isfile(path):
                continue
            table_name = self.get_table_name(file)
            try:
                with open(path, 'r', encoding = 'UTF-8') as file:
                    line = file.readline()
                    while line:
                        line = line.strip('\n')
                        es_data = json_utility_instance.make_json(table_name, line)
                        if not es_data is None:
                            self.es_data.append(es_data)
                        if len(self.es_data.append >= global_instance.ES_BATCH_NUM):
                            self.import_data()
                            del self.es_data[0 : len(self.es_data)]
                        line = file.readline()
            except Exception as e:
                global_instance.g_log.error("es import error:%s" %(e))
                continue
    def main(self):
        global_instance.g_log.info("es client start.")
        while True:
            if not self.get_file_list():
                time.sleep(5)
                continue
            self.import_files()
            self.remove_file_list()
            self.clear_file_list()
            if (len(self.es_data) > 0):
                self.import_data()
                del self.es_data[0 : len(self.es_data)]

if __name__ == '__main__':
    PID_FILE = '/var/run/es_client.pid'
    CONFIG_PATH = './config.ini'
    config = client_config(CONFIG_PATH)
    config.get_config()
    log_file = config.get_log_file()
    if len(sys.argv) != 2:
        print ('Usage: {} [start|stop]'.format(sys.argv[0]), file = sys.stderr)
        raise SystemExit(1)
    if sys.argv[1] == 'start':
        try:
            daemonize(PID_FILE, stdout = log_file, stderr = log_file)
        except RuntimeError as e:
            print (e, file = sys.stderr)
            raise SystemExit(1)
        client = es_client('./home/tmp')
        client.main()
    elif sys.argv[1] == 'stop':
        if os.path.exists(PID_FILE):
            with open(PID_FILE) as file:
                os.kill(int(file.read()), signal.SIGTERM)
        else:
            print ('not running', file = sys.stderr)
            raise SystemExit(1)
    else:
        print ('unknown command {!r}'.format(sys.argv[1]), file = sys.stderr)
        raise SystemExit(1)