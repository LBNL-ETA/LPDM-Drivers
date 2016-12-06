

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

global_cache_control:
		Hardware adapters for control of global cache iTach IP to IR bridge.
		global_cache_controls.py:
			API for communication to iTach bridge including fuctionality for obtaining device state, as well as sending IR coded messages to IR receiving devices.
		dvd_controls.py:
			A sample implementation of IP2IR communication API exposed in global_cache_controls.py.	 
		ac_control.py:
			Implementation of IP2IR communicated API to control a Frigidaire air conditioning system.
