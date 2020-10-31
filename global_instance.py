from client_config import client_config
from global_log import global_log
config_path = './config.ini'
g_config = client_config(config_path)
g_config.get_config()
log_file = g_config.get_log_file()
is_debug = g_config.get_debug()
g_log = global_log.get_instance(log_file, is_debug)
g_latest_files_num = 10
INT = 'int'
STRING = 'string'
ES_IP = '127.0.0.1'
ES_PORT = 9200
ES_USER = 'elastic'
ES_PASSWORD = 'dbapp@es'
ES_BATCH_NUM = 1000
