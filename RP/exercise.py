#!/usr/bin/env python

import time, os, subprocess, multiprocessing

from static_funcs import distance
from static_funcs import debug_print
from static_funcs import init_func

def beep_func(printOutput = True, GPIO_ECHO_INPUT = None ):
    # - STEP 1) define your  values
    #           Replace the XX with your numbers
    GPIO_ECHO_BEEP = XX
    GPIO_TRIG_BEEP = YY
    while True:        
        calc_dist = distance(GPIO_ECHO_BEEP,GPIO_TRIG_BEEP)
    # - STEP 2) Set the desired distance in cm to start beeping
    #           Replace the XX with your number
    #           Recommended values 35-70
        if calc_dist < XX:
            cmd = "(speaker-test -t sine -f " + str(75*calc_dist) + " -l 1 -p 1024 -P 4 > /dev/null)& pid=$!; sleep 0.25s; kill -9 $pid"
            os.system(cmd)
        time.sleep(0.1)
        
# A couple of variables
# ---------------------
EXIT = 0                        # Infinite loop
loop_sleep = 5                  # sleep period between loops
# Seperate process that play the bg music
proc = subprocess.Popen("echo")

# Go
# --
init_func()
beep_proc = multiprocessing.Process(target=beep_func, args=(False,))
beep_proc.start()


# Never ending loop
# -----------------
while EXIT == 0:

    alive = proc.poll()
    if alive is not None:
        print "Start me" + "alive is " + str(alive)
        proc = subprocess.Popen(["/usr/bin/aplay", "/home/pi/SAP-dokm-handson/RP/background150.wav"])
    time.sleep(loop_sleep)
    
subprocess.Popen.kill(proc)
beep_proc.terminate()

