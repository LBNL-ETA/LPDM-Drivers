import socket

# Controls of iTach IP2IR bridge made by global cache

class GlobalCacheBridge:
	PORT = 4998
	# Assuming an ethernet/network connection
	def __init__(self, address = '***REMOVED***'):
		# intiate socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# connect to itach via socket
		self.s.connect((HOST, address))


		# enable all relays
		print(enable_all())
		# retreive states of all relays
		print(get_states())


	def enable_all():
		"enables all relays"
		responses = {}
		responses[1] = setstate(1,1)
		responses[2] = setstate(2,1)
		responses[3] = setstate(3,1)
		return responses

	def disable_all():
		"disables all relays"
		responses = {}
		responses[1] = setstate(1,0)
		responses[2] = setstate(2,0)
		responses[3] = setstate(3,0)
		return responses

	def setstate(relay = 1, state = 0):
		"Sets state for relay passed in where 0 is open, 1 is closed"
		s.sendall("setstate,1:" + relay + "," ++ state + "\r")
		return s.recv(24) 

	def get_IR_all():
		"Return a dict of currents mode settings of all IR connectors"
		result = {}
		result[1] = get_IR_all(1)
		result[2] = get_IR_all(2)
		result[3] = get_IR_all(3)
		return result

	def get_IR(connector_index = 1):
		"Returns current mode setting of IR connector"
		s.sendall("get_IR,1:" + sensor_index + "\r")
		return s.recv(24)


	def get_states():
		"returns a dict containing the state of each sensor input" 
		states = {}
		states[1] = getstate(1)
		states[2] = getstate(2)
		states[3] = getstate(3)
		return states

	def get_state(sensor_index = 1):
		"gets state information from iTach on sensor_index sensor"
		s.sendall("getstate,1:" + sensor_index + "\r")
		return s.recv(24)

	# Learning mode command functions

	def get_IRL(numpackets = 1):
		"Enables learning mode"
		s.sendall("get_IRL\r")
		response = s.recv(24)
		if response == "IR learner Enabled/r":
			packet = s.recv(24 * numpackets)
			stop_IRL()
			return packet
		else:
			return response

	def stop_IRL():
		"Disables learning mode"
		s.sendall("stop_IRL\n")
		reponse = s.recv(24)
		return reponse	

