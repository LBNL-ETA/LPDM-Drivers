import requests

class Light_Driver(object):
    def __init__(self, url, auth):
        self.url = url
        self.auth = auth
        self.command_template = "<?xml version=\"1.0\" encoding=\"utf-8\"?><LG_CMD><CMD><CMDID>SET_MODE_BC</CMDID><MODE>{mode}</MODE></CMD></LG_CMD>\n\n"
        
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
    
    def set_light_level(self, light_level):
        """
            Expects light_level to be between 0 and 1.
            If light_level < .50 sets lights to discharge
            Otherwise sets lights to charge.
        """
        if light_level < .50:
            return self.set_to_discharge()
        else:
            return self.set_to_charge()
            
        