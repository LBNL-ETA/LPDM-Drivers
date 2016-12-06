

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
import requests

class PWMfan:

	def __init__(self,login_at_ip):

        # login_at_ip is a string, i.e. "debian@192.168.xx.xx"
		self.login_at_ip = login_at_ip

	def set_fan_speed(self,speed):
		# speed is a string representing 0% to 100%, i.e. "50"

		if speed == "0":
			pass
			# need to shut off switch associated with the fan
		else:
			subprocess.call(["ssh",self.login_at_ip,"sudo","python","fan_speed.py","-i",speed])
