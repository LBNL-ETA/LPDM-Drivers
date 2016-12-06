

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

from hue_control import HueBridge


# Controls for a group of one or more lights within the system
class HueLight:

    def __init__(self, bridge, light='1'):
        "Instantiates control over properties of light"
        if isinstance(bridge, HueBridge):
            self.bridge = bridge
        else:
            print('No bridge provided, assuming default bridge')
            self.bridge = HueBridge()

        self.light = light

    def get_info(self):
        "Returns a dict holding info about this light/lights"
        return self.bridge.get_light(self.light)

    def rename(self, name):
        "Changes name of light in Hue system to that passed in"
        self.bridge.update_light_attributes(self.light, {'name': name})

    def on(self, brightness=200, color=160):
        "Turns light on at brightness and color passed in"
        resource = {'on': (not brightness == 0), 'hue': color, 'bri': brightness}
        self.bridge.update_light_state(self.light, resource)

    def update_state(self, state):
        "Updates state information to brightness and color passed in"
        self.bridge.update_light_state(self.light, state)

    def off(self):
        "Turns light off"
        resource = {'on': False}
        self.bridge.update_light_state(self.light, resource)
