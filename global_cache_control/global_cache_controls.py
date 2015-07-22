import socket

# Controls of iTach IP2IR bridge made by global cache


class GlobalCacheBridge:
    def __init__(self, address='***REMOVED***'):
        # Assuming an ethernet/network connection
        PORT = 4998
        # intiate socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to itach via socket
        self.s.connect((PORT, address))

        # enable all relays
        print(self.enable_all())
        # retreive states of all relays
        print(self.get_states())

    def enable_all(self):
        "enable all relays"
        responses = {}
        responses[1] = self.setstate(1, 1)
        responses[2] = self.setstate(2, 1)
        responses[3] = self.setstate(3, 1)
        return responses

    def disable_all(self):
        "disables all relays"
        responses = {}
        responses[1] = self.setstate(1, 0)
        responses[2] = self.setstate(2, 0)
        responses[3] = self.setstate(3, 0)
        return responses

    def setstate(self, relay=1, state=0):
        "Sets state for relay passed in where 0 is open, 1 is closed"
        self.s.sendall("setstate,1:" + relay + "," + state + "\r")
        return self.s.recv(24)

    def get_IR_all(self):
        "Return a dict of currents mode settings of all IR connectors"
        result = {}
        result[1] = self.get_IR_all(1)
        result[2] = self.get_IR_all(2)
        result[3] = self.get_IR_all(3)
        return result

    def get_IR(self, connector_index=1):
        "Returns current mode setting of IR connector"
        self.s.sendall("get_IR,1:" + connector_index + "\r")
        return self.s.recv(24)

    def get_states(self):
        "returns a dict containing the state of each sensor input"
        states = {}
        states[1] = self.getstate(1)
        states[2] = self.getstate(2)
        states[3] = self.getstate(3)
        return states

    def get_state(self, sensor_index=1):
        "gets state information from iTach on sensor_index sensor"
        self.s.sendall("getstate,1:" + sensor_index + "\r")
        return self.s.recv(24)

    # Learning mode command functions

    def get_IRL(self, numpackets=1):
        "Enables learning mode"
        self.s.sendall("get_IRL\r")
        response = self.s.recv(24)
        if response == "IR learner Enabled/r":
            packet = self.s.recv(24 * numpackets)
            stop_IRL()
            return packet
        else:
            return response

    def stop_IRL(self):
        "Disables learning mode"
        self.s.sendall("stop_IRL\n")
        reponse = self.s.recv(24)
        return reponse
        