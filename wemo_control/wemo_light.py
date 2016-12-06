

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

import subprocess
from subprocess import call

class WemoLight:

	def __init__(self,device_name):

	    self.device_name = device_name

	def on(self,light_level):
	# light_level is from 1 to 255

            cmd = ["wemo","light",self.device_name,"on",str(light_level)]
            try:
                call(cmd)
            except:
                print "Wemo light " + self.device_name + " on() at level: " + str(light_level) + " failed."

	def off(self):

            cmd = ["wemo","light",self.device_name,"off"]
            try:
                call(cmd)
            except:
                print "Wemo light " + self.device_name + " off() failed."
