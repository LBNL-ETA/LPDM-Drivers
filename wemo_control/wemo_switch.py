import requests

class WemoInsight:

	def __init__(self,device_name,server_url):

		self.device_name = device_name
		self.url = 'http://' + server_url + ':5000/api/device/' + device_name

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


		

