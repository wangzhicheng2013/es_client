#!/usr/bin/python
import log_utility
class global_log:
    def get_instance(log_file, verbose):
        if not hasattr(global_log, '_logger'):
            global_log._logger = log_utility.get_logger(log_file, verbose)
        return global_log._logger