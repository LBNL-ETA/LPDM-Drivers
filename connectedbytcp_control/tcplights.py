#   Connected By TCP light control class
#   Copyright (C) 2014 Michael Hespenheide
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import httplib, urllib
import ssdp
from xml.etree import ElementTree

class TCPLights:
    '''A class for discovering and controlling TCP smart lights over http'''
    #Private vars
    gateway_ipaddr = None
    rooms = {}
    lights = {}
    scenes = {}
    dimRate = 25
    TCP_DISC_ST = "urn:greenwavereality-com:service:gop:1"

    # Constructor, will  use SSDP to discover the gateway unless specified
    def __init__(self, discover=True, ipaddr=None):
        if discover:
            resp = ssdp.discover(self.TCP_DISC_ST)
            if resp:
                self.gateway_ipaddr = resp[0].location.split('http://')[1]
                self.TCPGetLights()
        
            else:
                raise Exception('No gateway found')
        else:
            self.gateway_ipaddr = ipaddr
            self.TCPGetLights()

    def getRoomsList(self):
        roomList = []
        for room in self.rooms:
            roomList.append(self.rooms[room]['name'])
        return roomList

    def setDimRate(self, newRate):
        self.dimRate = newRate

    def TCPRaiseLight(self, light, done=True):
        if isinstance(light, dict):
            light = light['did']

        newValue = self.lights[light]['value'] + self.dimRate;
        self.TCPSetLightValue(light, newValue)
        if not self.lights[light]['state']:
            self.TCPSetLightBinary(light, 1)

        if done:
            self.TCPUpdateLights()

    def TCPRaiseRoom(self, room):
        for l in room['lights']:
            self.TCPRaiseLight(light=l, done=False)
            
        self.TCPUpdateLights()

    def TCPDimLight(self, light, done=True):
        if isinstance(light, dict):
            light = light['did']
        newValue = self.lights[light]['value'] - self.dimRate;
        self.TCPSetLightValue(light, newValue)
        if not self.lights[light]['state']:
            self.TCPSetLightBinary(light, 1)
        
        if done:
            self.TCPUpdateLights()

    def TCPDimRoom(self, room):
        for l in room['lights']:
            self.TCPDimLight(light=l, done=False)
            
        self.TCPUpdateLights()

    def TCPSetRoomBinary(self, room, value):
        for l in room['lights']:
            self.TCPSetLightBinary(l['did'], value, done=False)

        self.TCPUpdateLights()

    def TCPSetRoomValue(self, room, value):
        for l in room['lights']:
            self.TCPSetLightValue(l['did'], value, done=False)

        self.TCPUpdateLights()

    def TCPGetLightState(self, search):
        if isinstance(search, dict):
            return self.lights[search['did']]['value']
        else:
            return self.lights[search]['value']
        return -1 

    def TCPGetLight(self, search):
        if isinstance(search, int):
            return self.lights[search]
        else:
            for l in self.lights:
                l = self.lights[l]
                if l['name'] == search:
                    return l

    def TCPGetRoom(self, search):
        if isinstance(search, int):
            return self.rooms[search]
        else:
            for r in self.rooms:
                r = self.rooms[r]
                if r['name'] == search:
                    return r

    def TCPUpdateLights(self):
        params = urllib.urlencode( {'cmd': 'GWRBatch',
                                    'data': '<gwrcmds><gwrcmd><gcmd>RoomGetCarousel</gcmd><gdata><gip><version>1</version><token>1234567890</token><fields>name,control,power,product,class,realtype,status</fields></gip></gdata></gwrcmd></gwrcmds>',
                                    'fmt': 'xml' } )

        headers = { "Content-type": "application/x-www-form-urlencoded", 'Accept': 'en-US,en;q=0.8'}
        conn = httplib.HTTPConnection(self.gateway_ipaddr)
        conn.request("POST", "/gwr/gop.php", params, headers)
        response = conn.getresponse()
        data = response.read()
        if response.status==200 and response.reason=='OK':
            root = ElementTree.XML(data)
            xdict = XmlDictConfig(root)
            rooms = xdict['gwrcmd']['gdata']['gip']['room']
            for room in rooms:
                try:
                    for light in room['device']:
                        self.lights[light['did']]['value'] = int(light['level'])
                        self.lights[light['did']]['name'] = light['name']
                        self.lights[light['did']]['state'] = int(light['state'])
                except TypeError:
                    light = room['device']
                    self.lights[light['did']]['value'] = int(light['level'])
                    self.lights[light['did']]['name'] = light['name']
                    self.lights[light['did']]['state'] = int(light['state'])

    def TCPGetLights(self):
        params = urllib.urlencode( {'cmd': 'GWRBatch',
                                    'data': '<gwrcmds><gwrcmd><gcmd>RoomGetCarousel</gcmd><gdata><gip><version>1</version><token>1234567890</token><fields>name,control,power,product,class,realtype,status</fields></gip></gdata></gwrcmd></gwrcmds>',
                                    'fmt': 'xml' } )

        headers = { "Content-type": "application/x-www-form-urlencoded", 'Accept': 'en-US,en;q=0.8'}
        conn = httplib.HTTPConnection(self.gateway_ipaddr)
        conn.request("POST", "/gwr/gop.php", params, headers)
        response = conn.getresponse()
        data = response.read()
        if response.status==200 and response.reason=='OK':
            root = ElementTree.XML(data)
            xdict = XmlDictConfig(root)
            for room in xdict['gwrcmd']['gdata']['gip']['room']:
                self.rooms[room['name']] = { 'name': room['name'],
                                        'rid': room['rid'],
                                        'lights': [] }
                try:
                    for light in room['device']:
                        l =  {'name': light['name'], 'did': light['did'], 'value': int(light['level']), 'state': int(light['state'])}
                        self.rooms[room['name']]['lights'].append(l)
                        self.lights[light['did']] = l
                except TypeError:
                    light = room['device']
                    l =  {'name': light['name'], 'did': light['did'], 'value': int(light['level']), 'state': int(light['state'])}
                    self.rooms[room['name']]['lights'].append(l)
                    self.lights[light['did']] = l
        else:
            raise Exception('Unable to communicate with gateway')

        conn.close()


    def TCPSetLightBinary(self, did, value, done=True):
        if isinstance(did, dict):
            did = did['did']
        if value > 0 and self.lights[did]['value'] < 100:
            self.TCPSetLightValue(did, 100)

        params = urllib.urlencode( {'cmd': 'DeviceSendCommand',
                                    'data': '<gip><version>1</version><token>1234567890</token><did>%s</did><value>%d</value></gip>' % (did, value),
                                    'fmt': 'xml' } )

        headers = { "Content-type": "application/x-www-form-urlencoded", 'Accept': 'en-US,en;q=0.8'}
        conn = httplib.HTTPConnection(self.gateway_ipaddr)
        conn.request("POST", "/gwr/gop.php", params, headers)
        response = conn.getresponse()
        conn.close()
        if done:
            self.TCPUpdateLights()

    def TCPSetLightValue(self, did, value, done=True):
        if isinstance(did, dict):
            did = did['did']
        params = urllib.urlencode( { 'cmd': 'DeviceSendCommand',
                                     'data': '<gip><version>1</version><token>1234567890</token><did>%s</did><value>%s</value><type>level</type></gip>' % (did, value),
                                     'fmt': 'xml' } )
        headers = { "Content-type": "application/x-www-form-urlencoded", 'Accept': 'en-US,en;q=0.8'}
        conn = httplib.HTTPConnection(self.gateway_ipaddr)
        conn.request("POST", "/gwr/gop.php", params, headers)
        response = conn.getresponse()
        conn.close()
        if done:
            self.TCPUpdateLights()

# Because I HATE dealing with XML
#  This class converts from XML tree to Python Dict
#  Taken from here: http://code.activestate.com/recipes/410469-xml-as-dictionary/
#  Use the code in the second comment from "Alex" for correct operation
class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:
    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)
    Or, if you want to use an XML string:
    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)
    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        childrenNames = []
        for child in parent_element.getchildren():
            childrenNames.append(child.tag)

        if parent_element.items(): #attributes
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                #print len(element), element[0].tag, element[1].tag
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))

                if childrenNames.count(element.tag) > 1:
                    try:
                        currentValue = self[element.tag]
                        currentValue.append(aDict)
                        self.update({element.tag: currentValue})
                    except: #the first of its kind, an empty list must be created
                        self.update({element.tag: [aDict]}) #aDict is written in [], i.e. it will be a list

                else:
                     self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})