import time
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

class Light_Actuator(object):
    def __init__(self, sock):
        self.sock = sock
        
    def switch_to_battery(self):
        xml_to_write = "<LG_CMD><CMD><CMDID>SET_MODE_BC</CMDID><MODE>DISCHARGE</MODE></CMD></LG_CMD>"
        self.last_reading_timestamp = time.time()
        return self.write_to_lights(xml_to_write)

    def switch_to_grid_mode(self):
        """
        switch to grid mode (charging battery and powering light)
        """
        xml_to_write = "<LG_CMD><CMD><CMDID>SET_MODE_BC</CMDID><MODE>GRID</MODE></CMD></LG_CMD>"
        self.last_reading_timestamp = time.time()
        return self.write_to_lights(xml_to_write)
        
    def write_to_lights(self, xml_to_write):
        
        logger.debug("about to write the xml file to the socket")
        start_time = time.time()
       
        logger.debug("Trying to wake up socket for writing")
        logger.debug("Trying to write")
        self.sock.send(xml_to_write)

        