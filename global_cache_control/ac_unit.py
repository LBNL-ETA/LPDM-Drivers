

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

from ac_control import ACController
from global_cache_controls import GlobalCacheBridge

# Defines interface for logic to use in controlling the air conditioner by adjusting the setpoint


class ACUnit:

    def __init__(self, ipaddr):
        "construct a new ACUnit with bridge passed in"
        self.bridge = GlobalCacheBridge(ipaddr)
        self.setpoint = 72
        self.control = ACController(self.bridge)
        self.control.power()
        self.control.cool()
        self.control.fan_slower()

    def setTo(self, temp):
        "Sets temperature to setpoint passed in"
        self.setpoint = temp
        while self.setpoint < temp:
            self.control.temp_timer_up()
        while self.setpoint > temp:
            self.control.temp_timer_down()

    def on(self):
        "Sets setpoint to a very low value such that compressor will turn on."
        self.setTo(50)

    def off(self):
        "Sets setpoint to a very high level so that the compressor will turn off"
        self.setTo(90)

    def getState(self):
        "Return true if setpoint is 50, false if it is 90"
        return self.setpoint == 50

    def getSetpoint(self):
        "Return current setpoint"
        return self.setpoint
