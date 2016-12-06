

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

variable_speed_fan_control:
		Hardware interface for remotely controllable variable speed fan connected by a Beaglebone Black through its PWM interface.
		fan_control.py: 
			Remote control API of beaglebone fan through remote login and requests.
		fan_speed.py:
			Hardware controls of beaglebone pwm fan.
