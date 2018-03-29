import requests
from datetime import datetime, timedelta

class Light_Driver(object):
    def __init__(self, url, auth, switch_point_low = 0.05, switch_point_high = 0.50):
        self.url = url
        self.auth = auth
        self.command_template = "<?xml version=\"1.0\" encoding=\"utf-8\"?><LG_CMD><CMD><CMDID>SET_MODE_BC</CMDID><MODE>{mode}</MODE></CMD></LG_CMD>\n\n"
        self.switch_point_low = switch_point_low
        self.switch_point_high = switch_point_high
        self.last_set_time = datetime.now() - timedelta(minutes=10)
        self.time_between_commands = timedelta(minutes=5)
        self.last_command = None
    
    def get_charge_command(self):
        return self.command_template.format(mode="CHARGE")
    
    def get_discharge_command(self):
        return self.command_template.format(mode="DISCHARGE")
    
    def get_grid_command(self):
        return self.command_template.format(mode="GRID")
    
    def send_command(self, command):
        cmd = {"data": command}
        response = requests.post(self.url, data = cmd, auth=self.auth)
        return response
    
    def set_to_charge(self):
        cmd = self.get_charge_command()
        return self.send_command(cmd)
    
    def set_to_discharge(self):
        cmd = self.get_discharge_command()
        return self.send_command(cmd)
    
    def set_to_grid(self):
        cmd = self.get_grid_command()
        return self.send_command(cmd)
    
    def set_power_availablity(self, power_level):
        """
            Expects power_level to be between 0 and 1.
            Light is set to charge if the level is below the low switch point
            Set to grid if between the two points and set to discharge
            if above the high switch point
        """        
        command_to_run = None        
        if power_level < self.switch_point_low:
            command_to_run = self.set_to_charge
        elif self.switch_point_low <= power_level <= self.switch_point_high:
            command_to_run = self.set_to_grid
        else:
            command_to_run = self.set_to_discharge
        
        now = datetime.now()
        
        if ((now - self.last_set_time) < self.time_between_commands) or (command_to_run == self.last_command):
            return
            
        self.last_command = command_to_run
        self.last_set_time = now
        return command_to_run()
            
        
