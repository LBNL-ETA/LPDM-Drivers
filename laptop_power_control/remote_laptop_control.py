

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
import json

# Defines a class which uses requests in order to implement remote
# power control of a rest API accessible laptop computer's power
# profiles.

# Currently not using multiple power level functionality

# Requires user to have set up linear levels of power profiles to use
# Variable power use profiles. with lowerPower, increasePower, setPower

# Otherise plan can be acquired and the SoC can be acquired with getPlan
# and getSoc


class RemoteLaptopControl:

    def __init__(self, ipaddr):
        "IP address of computer"
        self.ipaddr = 'http://' + ipaddr
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
            pass
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

    def updatePlan(self):
        "Updates the value of the plan"
        r = requests.get(self.ipaddr + '/laptoppower/api/v1.0/profiles/active', auth=('***REMOVED***', '***REMOVED***'))
        if r.status_code == 200:
            response = int(json.loads(r.text)['name'])
            if response < 11:
                return response
            else:
                return -100

    def getPlan(self):
        "Returns the active power profile on the laptop"
        r = requests.get(self.ipaddr + '/laptoppower/api/v1.0/profiles/active', auth=('***REMOVED***', '***REMOVED***'))
        if r.status_code == 200:
            response = json.loads(r.text)['plan']['name']
            return response
        else:
            print('getPlan request failed with error' + str(r.status_code))
            return {'Error': r.status_code}

    def getSoc(self):
        "Returns an integer which represents the percent charge. 111 means charging."
        "Returns -100 if the request fails"
        r = requests.get(self.ipaddr + '/laptoppower/api/v1.0/battery/soc', auth=('***REMOVED***', '***REMOVED***'))
        if r.status_code == 200:
            return json.loads(r.text)['EstimatedChargeRemaining']
        else:
            print('getSoc request failed with error' + str(r.status_code))
            return -100
