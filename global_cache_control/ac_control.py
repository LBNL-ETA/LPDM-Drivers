

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

#Not all codes are trimmed properly. They all work, but some are extremely slow.


class ACController:
    def __init__(self, bridge, emitter=1, on=False, mode='off', temp=72, speed='low', timer=0):
        self.bridge = bridge
        self.emitter = 1
        self.on = on
        self.mode = mode
        self.temp = temp
        self.speed = speed
        self.timer = timer

    def power(self):
        "Sends the power function"
        self.on = not self.on
        return self.bridge.sendir(1, '1,1,38343,1,1,345,171,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,64,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,64,22,64,22,21,22,64,22,64,22,63,22,1561,342,86,22,3800')

    def temp_timer_up(self):
        "Sends the up function"
        if self.mode == 'timer':
            self.timer += 1
        else:
            self.temp += 1
        return self.bridge.sendir(1, '1,1,38343,1,1,345,172,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,21,22,64,22,64,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,64,22,64,22,64,22,63,22,1562,342,86,22,3670,340,86,22,3670,340,86,22,3670,340,86,22,3800')

    def temp_timer_down(self):
        "Sends the down function"
        if self.mode == 'timer':
            self.timer -= 1
        else:
            self.temp -= 1
        return self.bridge.sendir(1, '1,4,38343,1,1,342,172,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,64,22,21,22,64,22,64,22,21,22,21,22,21,22,21,22,21,22,64,22,21,22,21,22,64,22,64,22,64,22,63,22,1562,342,86,22,3670,340,86,22,3670,340,86,22,3670,340,86,22,3670,340,86,22,3800')

    def fan_slower(self):
        "Sends the fan slower function"
        if self.speed == 'high':
            self.speed = 'low'
        return self.bridge.sendir(1, '1,1,38343,1,1,343,171,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,21,22,64,22,64,22,21,22,64,22,64,22,64,22,64,22,63,22,3800')

    def fan_faster(self):
        "Sends the fan faster function"
        if self.speed == 'low':
            self.speed = 'high'
        return self.bridge.sendir(1, '1,1,38343,1,1,341,171,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,64,22,21,22,21,22,21,22,21,22,21,22,21,22,21,22,21,22,64,22,64,22,64,22,64,22,64,22,64,22,63,22,1563,342,86,22,3672,340,86,22,3671,340,86,22,3671,340,86,22,3671,340,86,22,3800')

    def cool(self):
        "Sends the cool setting function"
        self.mode = 'cool'
        return self.bridge.sendir(1, '1,1,38343,1,1,343,172,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,64,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,21,22,64,22,64,22,21,22,64,22,64,22,64,22,63,22,1563,342,86,22,3671,340,86,22,3671,340,86,22,3800')

    def energy_saver(self):
        "Sends the energy saver setting function"
        self.mode = 'energy_saver'
        return self.bridge.sendir(1, '1,1,38343,1,1,344,172,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,21,22,64,22,21,22,21,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,64,22,63,22,1563,342,86,22,3671,340,86,22,3671,340,86,22,3671,340,86,22,3800')

    def fan_only(self):
        "Sends the fan only setting function"
        self.mode = 'fan_only'
        return self.bridge.sendir(1, '1,4,38343,1,1,342,171,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,64,22,64,22,64,22,21,22,21,22,21,22,21,22,21,22,21,22,21,22,21,22,64,22,64,22,64,22,64,22,63,22,1563,342,86,22,3671,340,86,22,3671,340,86,22,3671,340,86,22,3800')

    def sleep(self):
        "Sends the sleep setting function"
        self.mode = 'sleep'
        return self.bridge.sendir(1, '1,5,38343,1,1,345,171,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,21,22,21,22,21,22,21,22,21,22,21,22,21,22,21,22,64,22,64,22,64,22,64,22,64,22,64,22,64,22,63,22,1562,342,86,22,3671,340,86,22,3671,340,86,22,3670,340,86,22,3670,340,86,22,3800')

    def auto_fan(self):
        "Sends the auto fan setting function"
        self.mode = 'auto_fan'
        return self.bridge.sendir(1, '1,6,38343,1,1,342,171,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,64,22,64,22,64,22,64,22,21,22,21,22,21,22,21,22,21,22,21,22,21,22,21,22,64,22,64,22,64,22,63,22,1562,342,86,22,3670,340,86,22,3670,340,86,22,3670,340,86,22,3800')

    def timer(self):
        "Sends the timer function"
        self.mode = 'timer'
        return self.bridge.sendir(1, '1,2,38343,1,1,342,172,22,21,22,21,22,21,22,64,22,21,22,21,22,21,22,21,22,64,22,21,22,64,22,21,22,64,22,64,22,64,22,64,22,21,22,64,22,64,22,21,22,21,22,21,22,21,22,21,22,64,22,21,22,21,22,64,22,64,22,64,22,64,22,63,22,3800')
