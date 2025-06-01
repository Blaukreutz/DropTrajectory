from Image_Processing import *
import numpy as np
import cv2
import pigpio
from time import sleep

#accessing the camera feed
cam = cv2.VideoCapture("/dev/video17", cv2.CAP_V4L2)

pi = pigpio.pi()  # Connect to pigpiod

# Define GPIOs for the servos
servos = [
    18,  # HW PWM0
    19,  # HW PWM1
    17,  # SW PWM
    27   # SW PWM
]

min_pulse_width = 600 #conservative estimate, likely closer to 500
max_pulse_width = 2400 #conservative estimate, likely closer to 2500

# Set initial pulse widths (1500us = center position)
for gpio in servos:
    pi.set_servo_pulsewidth(gpio, 1500)

angles = [0, 0, 0, 0]

#execution
while True:
    #process camera inputs
    ret, frame = cam.read()
    data = get_target_data(find_largest_ellipse(frame))
    if data is not None:
        print(data) #TODO: this is diagnotic-only. remove for final tests
    
    #TODO: ANGLE MATH GOES HERE

    #update servos
    for i, angle in enumerate(angles):   
        pulse_width = min_pulse_width + (angle/180.0)*(max_pulse_width-min_pulse_width) #angles in degrees
        pi.set_servo_pulsewidth(servos[i], pulse_width)