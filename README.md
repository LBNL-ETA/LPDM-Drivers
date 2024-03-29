Hardware adapters (WeMo lights and switches, Hue Lights, IP IR Bridge, Connected by TCP lights, PWM fan)

Documentation for each system can be found here:
 https://docs.google.com/a/lbl.gov/document/d/1Q6v6Al0Q7rn_3mdpHLPZaN-xkiN_Z2TM1xf0hcFDm8U/edit?usp=sharing

Contains hardware adapters for various network controllable lights, PWM controllable fan, and other devices through IR communication.

Sub Directories:
	connectedbytcp_control:
	Module
		Hardware adapter for connected by TCP lighting environment.
		connected_controls.py:
			Contains a wrapper for TCP light functionality as described in tcplights.py.
		tcplights.py:
			API for TCP light connectivity and use, allows configuration of rooms and scenes as well as configuration of individual lights.

	global_cache_control:
	Module
		Hardware adapters for control of global cache iTach IP to IR bridge.
		global_cache_controls.py:
			API for communication to iTach bridge including fuctionality for obtaining device state, as well as sending IR coded messages to IR receiving devices.
		dvd_controls.py:
			A sample implementation of IP2IR communication API exposed in global_cache_controls.py.	 
		ac_control.py:
			Implementation of IP2IR communicated API to control a Frigidaire air conditioning system.


	hue_control:
	Module
		Wrappers around beautifulhue python API for bridge and for lights.
		hue_control.py:
			Wraps beautifulhue api to control functionality of hue bridge and connected devices.
		hue_light.py:
			Wrapper for hue_control.py which allows simple control of one light.

	variable_speed_fan_control:
	Module
		Hardware interface for remotely controllable variable speed fan connected by a Beaglebone Black through its PWM interface.
		fan_control.py: 
			Remote control API of beaglebone fan through remote login and requests.
		fan_speed.py:
			Hardware controls of beaglebone pwm fan.

	wemo_control:
	Module
		Hardware adapter for control of WeMo networked lights and switching devices. 
		wemo_light.py:
			Wrapper for 3rd party wemo API called ouixmeaux which provides interface for controlling connected lights.
		wemo_switch.py:
			Wrapper for 3rd party wemo API called ouimeaux, allowing control of a WeMo Insight switch and reading of state information from it. 			

	laptop_power_control:
	Module
		Adapter for remote control of a windows laptop's power settings.
		laptop_control.py:
			Python wrapper for system calls to powercfg on a Windows machine, changing between power profiles, power settings as well as battery status and information. 
		rest_server.py:
			Flask based restful API for laptop_control's system calls with password based authentication, meant to be used on windows laptops as a server for remote control of power profiles. 
		remote_laptop_control.py:
			Remote interface for the restful API implemented by rest_server.py, so that laptop can be controlled in discrete power levels from 1-10, allowing scalable power usage. 

				