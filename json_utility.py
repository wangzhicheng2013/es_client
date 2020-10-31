#!/usr/bin/python
import sys
import uuid
import re
import global_instance
class json_utility():
    def get_instance():
        if not hasattr(json_utility, '_json'):
            json_utility._json = json_utility()
        return json_utility._json
    def __init__(self):
        self.json_func_map = {"wdd_risk" : self.wdd_risk}
    def make_json(self, name, line):
        try:
            json = self.json_func_map[name](line)
            return json
        except Exception as e:
            global_instance.g_log.error("error:%s" %(e))
            return ""
    def handle_aggregation_data(self, data, type):
        t_data = data.replace('"', '')
        if global_instance.STRING == type:
            if '' == t_data:
                return "0"
            else:
                return t_data
        elif global_instance.INT == type:
            result = int(t_data)
            return result
    def wdd_risk(self, line):
        data_list = re.split(r',\s*(?![^"]*\"\,)', line)
        if (len(data_list) != 2):
            return None
        aggregation = [self.handle_aggregation_data(data_list[0], global_instance.STRING), self.handle_aggregation_data(data_list[1], global_instance.STRING)]
        aggregation_str = '-'.join(aggregation)
        result = {
            "_index": "risk-index",
            "_source":{
                'id':self.handle_aggregation_data(data_list[0], global_instance.STRING),
                'pod':self.handle_aggregation_data(data_list[1], global_instance.INT),
                'aggregation':aggregation_str
            }
        }
        global_instance.g_log.debug("risk json:%s" %(result))
        return result
        
json_utility_instance = json_utility.get_instance()