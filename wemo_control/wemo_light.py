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
