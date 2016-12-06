

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

import requests

class WemoInsight:

	def __init__(self,device_name,server_url):

		self.device_name = device_name
		self.url = 'http://' + server_url + ':5000/api/device/' + device_name
                # server_url is ip address of volttron90

	def on(self):

		requests.post(self.url, {'state':'on'})

	def off(self):

		requests.post(self.url, {'state':'off'})

	def toggle(self):

		requests.post(self.url, {'state':'toggle'})

	def current_power(self):

		r = requests.get(self.url)
		status = r.json()
                p_raw = float(status['currentpower'])
		return p_raw/1000


		

