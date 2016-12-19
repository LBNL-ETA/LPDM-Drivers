

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

from tcplights import TCPLights

class ConnectedLight:
    def __init__(self, lights, did, ipaddr=None):
        self.lights = lights
        self.did = did

    def on(self, brightness=100):
        "Turns lights on at brightness passed in"
        self.lights.TCPSetLightValue(self.did, brightness)

    def off(self):
        "Turns light off"
        self.lights.TCPSetLightValue(self.did, 0)
