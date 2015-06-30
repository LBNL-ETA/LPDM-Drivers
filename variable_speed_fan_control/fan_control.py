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
