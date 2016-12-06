

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

import sys
import getopt
import Adafruit_BBIO.PWM as PWM

def set_duty_cycle(duty_cycle):
    PWM.start("P9_14",duty_cycle)

def main(argv):
    duty_cycle = ''
    try:
        opts,args = getopt.getopt(argv, "hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'fan_speed.py -i <duty_cycle>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
           print 'tcx_correct.py -i <duty_cycle>'
           sys.exit()
        elif opt in ("-i", "--ifile"):
             duty_cycle = arg

    print 'Duty cycle is', duty_cycle

    set_duty_cycle(float(duty_cycle))

if __name__ == "__main__": main(sys.argv[1:])

