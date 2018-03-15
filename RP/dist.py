#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, os, subprocess, multiprocessing

from static_funcs import distance
from static_funcs import beep_func
from static_funcs import debug_print
from static_funcs import init_func

# Which GPIO's are used [0]=BCM Port Number [1]=BCM Name [2]=Use [3]=Pin
# ----------------------------------------------------------------------
GPIO_ECHO = 17
GPIO_TRIG = 4

# A couple of variables
# ---------------------
EXIT = 0                        # Infinite loop
loop_sleep = 1                  # sleep period between loops
# Seperate process that play the bg music
proc = subprocess.Popen("echo")


# Go
# --
init_func()
beep_proc = multiprocessing.Process(target=beep_func)
beep_proc.start()


# Never ending loop
# -----------------
while EXIT == 0:

    # Display distance


    intdistance = distance(GPIO_ECHO,GPIO_TRIG)
    print "Distance = " + str(intdistance) + "cm"
    alive = proc.poll()
    if intdistance < 20:
        print "Start me" + "alive is " + str(alive)
        if alive is not None:
            print "Start me" + "alive is " + str(alive)
            proc = subprocess.Popen(["/usr/bin/aplay", "/home/pi/VC/CSH6XuazmB8.wav"])
    elif alive is None:
            subprocess.Popen.kill(proc)

    time.sleep(loop_sleep)

beep_proc.terminate()
