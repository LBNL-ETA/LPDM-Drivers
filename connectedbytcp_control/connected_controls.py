import requests

class ConnectedControls: 

	def change_state(deviceID, isOn = True):
		"Switches state to either on or off based on isOn"

	def set_brightness(deviceID, brightness = 100):
		"Sets brightness to value passed in"

	def get_system_status():
		"Returns a struct representing the current status of the system"