

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

laptop_power_control:
	Module
		Adapter for remote control of a windows laptop's power settings.
		laptop_control.py:
			Python wrapper for system calls to powercfg on a Windows machine, changing between power profiles, power settings as well as battery status and information. 
		rest_server.py:
			Flask based restful API for laptop_control's system calls with ***REMOVED*** based authentication, meant to be used on windows laptops as a server for remote control of power profiles. 
		remote_laptop_control.py:
			Remote interface for the restful API implemented by rest_server.py, so that laptop can be controlled in discrete power levels from 1-10, allowing scalable power usage. 
