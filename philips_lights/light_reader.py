import threading
import socket
import xml.etree.ElementTree as ET
from time import time
logging.basicConfig()
logger = logging.getLogger(__name__)

from dateutil.parser import parse
from light_data import Light_Data


class Light_Reader(threading.Thread):
    def __init__(self, read_event, reading_timestamps_queue, sock):
        super(Light_Reader, self).__init__()
        self.read_event = read_event
        self._stop = False
        self.reading_timestamps_queue = reading_timestamps_queue
        self.sock = sock
        
    def stop(self):
        self._stop = True
        
    def parse_response(self, response):        
        tree = ET.ElementTree(ET.fromstring(response))
        root = tree.getroot()
        luminares = root.findall('./Luminare')
        
        readings = []
        
        for lum in luminares:
            path_base=""
            for e in lum:
                if e.tag.upper()=="LUMID":
                    lumin=e.text
                    path_base="/Philips/"+lumin                    
                if e.tag.upper()=="DATETIME":
                    timestamp = parse(e.text)
                if e.tag.upper()=="ALS":
                    level=int(e.text)
                if e.tag.upper()=="LEDPWR":
                    if e.text[-1].upper() == "W":
                        light_power = float(e.text[:-1])
                    else:
                        light_power=float(e.text)
                if e.tag.upper()=="BATCHGPWR":
                    if e.text[-1].upper() == "W":
                        charge_power = float(e.text[:-1])
                    else:
                        charge_power=float(e.text)
                        
                if e.tag.upper()=="BATDCHGPWR":
                    if e.text[-1].upper() == "W":
                        dcharge_power = float(e.text[:-1])
                    else:
                        dcharge_power=float(e.text)
                    
                if e.tag.upper()=="PRESENCE":
                    presence = e.text
                    
                if e.tag.upper()=="MODE":
                    mode = e.text
                    
                if e.tag.upper()=="SOC":
                    soc = e.text
                    
                if e.tag.upper()=="SOH":
                    soh = e.text                    
                    
            if path_base:
                    light_data = Light_Data(lumin, timestamp, level, light_power, charge_power, presence, mode, dcharge_power, soc, soh)
                    readings.append(light_data)
        
        return readings
        
    def run(self):
        while not self._stop:    
            try:
                #packets are sent every 30 seconds, so this should work
                #sock = socket.create_connection(address, timeout=35)
    
                #print "socket created"
                #sock.settimeout(None)
                #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #s.connect((ip,port))
                #s.send("my request\r")
                #read one character at a time to find the end of the XML
                #
                # Due to issues with lights switched socket to nonblocking to
                # try to resolve problems with overlapping xml.  Didn't help
                # but didn't hurt either and not enough time to roll back to blocking
                # currently
                chunk = ""#self.sock.recv(1)
                while (chunk.find("</LightStatus>") < 0):
                    try:
                        chunk += self.sock.recv(1)
                    except Exception as e:
                        pass
                
                #only take the part that starts with the proper tag
                response=chunk[chunk.find('<LightStatus>'):]
            except socket.timeout:
                print('I timed out.')
                #sock.close()
    
            try:
                readings = self.parse_response(response)
                ts = time() 
                print "Got reading at {t}".format(t = ts)
                self.read_event.timestamp = ts
                self.read_event.light_data = readings
                self.read_event.set()
                self.read_event.clear()
                
                try:
                    self.reading_timestamps_queue.get(False)
                except:
                    pass                                
                
                self.reading_timestamps_queue.put(ts)
                   
            except (KeyboardInterrupt, SystemExit):
                raise   
            except Exception as e:            
                print "problem with getting xml: {e}".format(e = e)
                print "Chunk: {c}".format(c = chunk)
                print "Response: {r}".format(r = response)
                
            #sleep for a while until next anticipated post from lights
            time.sleep(20)
                   