laptop_power_control:
	Module
		Adapter for remote control of a windows laptop's power settings.
		laptop_control.py:
			Python wrapper for system calls to powercfg on a Windows machine, changing between power profiles, power settings as well as battery status and information. 
		rest_server.py:
			Flask based restful API for laptop_control's system calls with ***REMOVED*** based authentication, meant to be used on windows laptops as a server for remote control of power profiles. 
		remote_laptop_control.py:
			Remote interface for the restful API implemented by rest_server.py, so that laptop can be controlled in discrete power levels from 1-10, allowing scalable power usage. 
