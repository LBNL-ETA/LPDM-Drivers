from hue_control import HueBridge

# Controls for a group of one or more lights within the system
class HueLight:

	def __init__(self, bridge, light = '1'):
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
		self.bridge.update_light_attributes(self.light, {'name':name})

	def on(self, color = '160', brightness = '200'):
		"Turns light on at brightness and color passed in"
		resource = {'on':True, 'ct':color, 'bri':brightness}
		self.bridge.update_light_state(self.light, resource)  

	def update_state(self, state):
		"Updates state information to brightness and color passed in"
		self.bridge.update_light_state(self.light, state)		

	def off(self):
		"Turns light off"	
		resource = {'on':False}
		self.bridge.update_light_state(self.light, resource)				