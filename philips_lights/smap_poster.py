import threading
import logging
logging.basicConfig()
from smap_tools import smap_post 


source_name= "Test Posting"
smap_api_key = "REMOVED"
smap_root = "REMOVED"
timezone_string = "REMOVED"
als_unit=""
additional_metadata = {"location":"REMOVED"}

def convert_presence_to_number(presence):
    mapping = {"No" : 0, "Yes" : 1}
    res = mapping.get(presence, -1)
    return res

def convert_mode_to_number(mode):
    mapping = {"NOCHARGE" : 0, "CHARGE" : 1, "DISCHARGE" : 2}
    res = mapping.get(mode, -1)
    return res
 
class Smap_Poster(threading.Thread):
    def __init__(self, read_event):
        super(Smap_Poster, self).__init__()
        self.read_event = read_event
        self._stop = False
        
    def stop(self):
        self._stop = True
        
    def post_readings(self, readings):
        total_power_used = 0
        latest_timestamp = readings[0].timestamp
        power_from_wall = 0
        for reading in readings:
            latest_timestamp = max(latest_timestamp, reading.timestamp)
            path_base="/Philips/" + reading.id
            als_path = path_base + "/ALS"
            led_power_path = path_base + "/LedPwr"
            battery_charge_power_path = path_base + "/BatChgPwr"
            presence_path = path_base + "/Presence"
            mode_path = path_base + "/Mode"
            discharge_power_path = path_base + "/BatDChgPwr"
            soc_path = path_base + "/SOC"
            soh_path = path_base + "/SOH"
                        
            smap_post(smap_root, smap_api_key, als_path, als_unit, "double", [[reading.timestamp, reading.als]], source_name, timezone_string, additional_metadata)
            smap_post(smap_root, smap_api_key, led_power_path, "W", "double", [[reading.timestamp, reading.led_power]], source_name, timezone_string, additional_metadata)
            smap_post(smap_root, smap_api_key, battery_charge_power_path, "W", "double", [[reading.timestamp, reading.battery_charge_power]], source_name, timezone_string, additional_metadata)
            smap_post(smap_root, smap_api_key, presence_path, "", "double", [[reading.timestamp, convert_presence_to_number(reading.presence)]], source_name, timezone_string, additional_metadata)
            smap_post(smap_root, smap_api_key, mode_path, "", "double", [[reading.timestamp, convert_mode_to_number(reading.mode)]], source_name, timezone_string, additional_metadata)
            smap_post(smap_root, smap_api_key, discharge_power_path, "W", "double", [[reading.timestamp, reading.discharge_power]], source_name, timezone_string, additional_metadata)
            smap_post(smap_root, smap_api_key, soc_path, "%", "double", [[reading.timestamp, reading.soc]], source_name, timezone_string, additional_metadata)
            smap_post(smap_root, smap_api_key, soh_path, "%", "double", [[reading.timestamp, reading.soh]], source_name, timezone_string, additional_metadata)
            
            total_power_used += reading.battery_charge_power + reading.led_power
            power_from_wall += reading.battery_charge_power + reading.led_power - reading.discharge_power
            
        smap_post(smap_root, smap_api_key, "/Philips/total_power", "W" , "double", [[latest_timestamp, total_power_used]], source_name, timezone_string, additional_metadata)
        smap_post(smap_root, smap_api_key, "/Philips/power_from_wall", "W" , "double", [[latest_timestamp, power_from_wall]], source_name, timezone_string, additional_metadata)
        
    def run(self):
        while not self._stop:
            self.read_event.wait()
            self.post_readings(self.read_event.light_data)
            
    def init(self):
        self.driver.init()
