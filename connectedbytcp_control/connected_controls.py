from tcplights import TCPLights

class ConnectedLight:
    def __init__(self, lights, did, ipaddr='***REMOVED***'):
        self.lights = lights
        self.did = did

    def on(self, brightness=100):
        "Turns lights on at brightness passed in"
        self.lights.TCPSetLightValue(self.did, brightness)

    def off(self):
        "Turns light off"
        self.lights.TCPSetLightValue(self.did, 0)
