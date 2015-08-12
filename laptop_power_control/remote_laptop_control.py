import requests
import json

# Defines a class which uses requests in order to implement remote
# power control of a rest API accessible laptop computer's power
# profiles.


class RemoteLaptopControl:

    def __init__(self, ipaddr):
        "IP address of computer"
        self.ipaddr = ipaddr
        # Power levels from 1 to 10 for plan
        # Request current state and go from there
        self.plan = self.getPlan

    def lowerPower(self):
        "Lowers power level by 1"
        self.plan = self.getPlan()
        if self.plan > 1:
            payload = {'name': str(self.plan - 1)}
            r = requests.post(self.ipaddr + '/laptoppower/api/v1.0/profiles/setprofilebyname', auth=('***REMOVED***', '***REMOVED***'), params = payload)
            # Check that post was successful
            if r.status_code == 201:
                self.plan = self.plan - 1
            else:
                print('lowerPower request failed with error' + str(r.status_code))
        elif self.plan == 1:
            # Turn off computer? I don't think we want to do this...
        else:
            print('Cannot lower power level further')

    def increasePower(self):
        "Increases power level by 1"
        self.plan = self.getPlan()
        if self.plan < 11:
            payload = {'name': str(self.plan + 1)}
            r = requests.post(self.ipaddr + '/laptoppower/api/v1.0/profiles/setprofilebyname', auth=('***REMOVED***', '***REMOVED***'), params = payload)
            # Check that post was successful
            if r.status_code == 201:
                self.plan = self.plan + 1
            else:
                print('increasePower request failed with error' + str(r.status_code))
        else:
            print('Power level cannot be further increased')

    def setPower(self, powerLevel):
        "Sets power level to value passed in"
        if powerLevel < 11 and powerLevel > 0:
            payload = {'name': str(powerLevel)}
            r = requests.post(self.ipaddr + '/laptoppower/api/v1.0/profiles/setprofilebyname', auth=('***REMOVED***', '***REMOVED***'), params = payload)
            # Check that post was successful
            if r.status_code == 201:
                self.plan = powerLevel
            else:
                print('setPower request failed with error' + str(r.status_code))
        else:
            print('Provided powerLevel is not within acceptable bounds.')

    def getPlan(self):
        "Updates the value of the plan"
        r = requests.get(self.ipaddr + '/laptoppower/api/v1.0/profiles/active', auth=('***REMOVED***', '***REMOVED***'))
        if r.status_code == 201:
            response = int(json.loads(r.text)['plan'])
            if response < 11:
                return response
            else:
                return -100

    def getSoc(self):
        "Returns an integer which represents the percent charge. 111 means charging."
        "Returns -100 if the request fails"
        r = requests.get(self.ipaddr + '/laptoppower/api/v1.0/battery/soc', auth=('***REMOVED***', '***REMOVED***'))
        if r.status_code == 201:
            return json.loads(r.text)['soc']
        else:
            print('getSoc request failed with error' + str(r.status_code))
            return -100
