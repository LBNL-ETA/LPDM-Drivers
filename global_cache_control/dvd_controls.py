

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

from global_cache_controls import GlobalCacheBridge


class DVDController:
    def __init__(self, bridge, emitter=1):
        self.bridge = bridge
        self.emitter = 1

    def power(self):
        "Sends the power function to dvd player"
        return self.bridge.sendir(1, '1,1,38226,1,1,342,171,22,21,22,21,21,21,22,21,22,21,21,21,22,21,22,21,21,64,22,63,22,64,21,64,22,63,22,64,21,64,22,63,22,21,22,63,22,21,22,63,22,21,22,21,21,64,22,21,21,64,22,21,21,64,22,21,21,64,22,63,22,21,22,63,22,1523,341,85,22,3660,342,85,21,3660,342,85,22,3660,341,85,22,3800')
    
    # Need to fix signal for this
    def open(self):
        "Sends the power function to dvd player"
        return self.bridge.sendir(1, '1,6,38109,1,1,341,171,21,22,21,22,21,21,21,22,21,22,21,21,21,22,21,22,21,64,10,3800')