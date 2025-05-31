import cv2
from Image_Processing import *

#cv2.namedWindow("preview")
cap = cv2.VideoCapture("/dev/video10")

while cap.isOpened():
    #process camera inputs
    ret, frame = cap.read()
    #cv2.imshow("preview", frame)
    data = get_target_data(find_largest_ellipse(frame))
    if data is not None:
        print(data)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
print("cap not open")
#cv2.destroyWindow("preview")
cap.release()