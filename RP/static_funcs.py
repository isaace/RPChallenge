#-------------------------------------------------------------------------------
# Name:        Static funcs
# Purpose:
#
# Author:      I070890
#
# Created:     18/01/2015
# Copyright:   (c) I070890 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time, os, subprocess, multiprocessing
import RPi.GPIO as GPIO

# A couple of variables
# ---------------------
debug = False                   # debug mode for console output
#debug = True                   # debug mode for console output
first_iter = True

def init_func():
    # Wait for 2 seconds to allow the ultrasonics to settle (probably not needed)
    # ---------------------------------------------------------------------------
    print "Waiting for 2 seconds....."
    time.sleep(2)

    # Go
    # --
    print "Running....\nStart Beep process...."
    GPIO.setmode(GPIO.BCM)

def distance(GPIO_ECHO,GPIO_TRIG):
    debug_print ("GPIO_TRIG = " + str(GPIO_TRIG) + ",GPIO_ECHO = " + str(GPIO_ECHO))
    # Set GPIO Channels
    # -----------------
    GPIO.setup(GPIO_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_TRIG, GPIO.OUT)
    GPIO.output(GPIO_TRIG, False)


    # A couple of variables
    # ---------------------
    EXIT = 0                        # Infinite loop
    decpulsetrigger = 0.0001        # Trigger duration
    inttimeout = 1000               # Number of loop iterations before timeout called


    min_dist = 100

    # Never ending loop
    # -----------------
    while EXIT < 10:

        # Trigger high for 0.0001s then low
        GPIO.output(GPIO_TRIG, True)
        time.sleep(decpulsetrigger)
        GPIO.output(GPIO_TRIG, False)

        # Wait for echo to go high (or timeout)
        i_countdown = inttimeout

        while (GPIO.input(GPIO_ECHO) == 0 and i_countdown > 0):
            i_countdown -=  1

        # If echo is high than the i_countdown not zero
        if i_countdown > 0:

            # Start timer and init timeout countdown
            echostart = time.time()
            i_countdown = inttimeout

            # Wait for echo to go low (or timeout)
            while (GPIO.input(GPIO_ECHO) == 1 and i_countdown > 0):
                i_countdown -= 1

            # Stop timer
            echoend = time.time()


            # Echo duration
            echoduration = echoend - echostart

        # Display distance
        if i_countdown > 0:
            i_distance = (echoduration*1000000)/58
            debug_print("Distance = " + str(i_distance) + "cm")
            min_dist = min(min_dist,i_distance)
        else:
            debug_print("Distance - timeout")

            # Wait at least .01s before re trig (or in this case .1s)
            time.sleep(.1)

        EXIT +=1
        return min_dist

def debug_print(line,must_print = False):
    if debug or must_print:
        print line

def beep_func(printOutput = True, GPIO_ECHO_INPUT = None ):
    while True:
        if GPIO_ECHO_INPUT != None:
            GPIO_ECHO_BEEP = [0]
            GPIO_TRIG_BEEP = [1]
        else:
            GPIO_ECHO_BEEP = 26
            GPIO_TRIG_BEEP = 27
        calc_dist = distance(GPIO_ECHO_BEEP,GPIO_TRIG_BEEP)
        print "BEEP dist is: " + str(calc_dist)
        if calc_dist < 60:
            cmd = "(speaker-test -t sine -f " + str(75*calc_dist) + " -l 1 -p 1024 -P 4 > /dev/null)& pid=$!; sleep 0.25s; kill -9 $pid"
            debug_print(cmd)
            os.system(cmd)
        time.sleep(0.1)


