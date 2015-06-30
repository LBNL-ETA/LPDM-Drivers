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

