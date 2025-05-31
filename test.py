import cv2
from Image_Processing import *

#cv2.namedWindow("preview")
cam = cv2.VideoCapture(0)

while True:
    #process camera inputs
    ret, frame = cam.read()
    #cv2.imshow("preview", frame)
    data = get_target_data(find_largest_ellipse(frame))
    if data is not None:
        print(data)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

#cv2.destroyWindow("preview")
cam.release()