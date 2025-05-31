from Image_Processing import *
import numpy as np
import cv2

# Open the default camera
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    data = get_target_data(find_largest_ellipse(frame))
    print(data)