

################################################################################################################################
# *** Copyright Notice ***
#
# "Price Based Local Power Distribution Management System (Local Power Distribution Manager) v1.0" 
# Copyright (c) 2016, The Regents of the University of California, through Lawrence Berkeley National Laboratory 
# (subject to receipt of any required approvals from the U.S. Dept. of Energy).  All rights reserved.
#
# If you have questions about your rights to use or distribute this software, please contact 
# Berkeley Lab's Innovation & Partnerships Office at  IPO@lbl.gov.
################################################################################################################################

from beautifulhue.api import Bridge


# Control functionality of bridge system wrapper to simplify interface
class HueBridge:
    def __init__(self, ip=None, user_name=None):
        #New Hue control with ip and user name
        self.ip = ip
        self.user_name = user_name
        self.bridge = Bridge(device={'ip': ip}, user={'name': user_name})

    #ideally this has already been configured
    def create_config(self):
        "Configures the Hue bridge"
        created = False
        print 'Press the button on the Hue bridge'

        # Looks for hue, continually sending message until successfull
        while not created:
            # Test message to the hue
            resource = {'user': {'devicetype': 'beautifulhuetest', 'name': self.user_name}}            # Attempt config with message
            response = self.bridge.config.create(resource)['resource']
            if 'error' in response[0]:
                if response[0]['error']['type'] != 101:
                    raise RuntimeError('Unhandled error creating configuration on the Hue')
            else:
                created = True

    def get_system_data(self):
        "Return a dict object containing system information"
        resource = {'which': 'system'}
        return self.bridge.config.get(resource)['resource']

    def get_new_lights(self):
        "Returns a dict object containing all newly added hue lights"
        resource = {'which': 'new'}
        return self.bridge.light.get(resource)['resource']

    def get_all_lights(self):
        "Returns a dict object containing all hue lights"
        resource = {'which': 'all'}
        return self.bridge.light.get(resource)['resource']

    def get_light(self, lightIndex):
        "Returns a dict object containing values of particular light"
        resource = {'which': lightIndex}
        return self.bridge.light.get(resource)['resource']

    def find_new_lights(self):
        "Discovers new lights associated with bridge"
        resource = {'which': 'new'}
        return self.bridge.light.find(resource)['resource']

    def update_light_attributes(self, whichLights, data):
        "Updates light attributes such as name, etc"
        resource = {
            'which': whichLights,
            # Data is an object in the form {'name', etc}
            'data': {'attr': data}
        }
        self.bridge.light.update(resource)

    def update_light_state(self, whichLights, data):
        "Updates light state such as on, brightness, hue, etc"
        resource = {
            'which': whichLights,
            # Data is an object in the form {'on', 'ct', 'bri', etc}
            'data': {'state': data}
        }
        self.bridge.light.update(resource)
