import cv2
import numpy as np
import math

'''finds all the ellipses in an image'''
def find_largest_ellipse(frame):
    #Isolating the color red
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(frame, (0,50,20), (5,255,255))
    mask2 = cv2.inRange(frame, (175,50,20), (180,255,255))
    mask = cv2.bitwise_or(mask1, mask2)

    #finding ellipses
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ellipses = [None]*len(contours)
    contour_areas = [None]*len(contours)
    count1 = 0
    for c in contours:
        if len(c) > 5:
            ellipses[count1] = cv2.fitEllipse(c)
            contour_areas[count1] = cv2.contourArea(c)
            count1 = count1 + 1
    
    biggest_real_ellipse = None
    biggest_index = 0
    for i, x in enumerate(ellipses):
        if x is not None and contour_areas[i] != 0:
            area = np.pi*max(x[1])*min(x[1])/4 #calculate area of the ellipse from the major and minor axes
            if area/contour_areas[i] > 0.9 and area/contour_areas[i] < 1.1: #threshholds chosen arbitrary TODO: fine tune
                if biggest_real_ellipse is None:
                    biggest_real_ellipse = x
                    biggest_index = i
                else:
                    if contour_areas[i] > contour_areas[biggest_index]:
                        biggest_real_ellipse = x
                        biggest_index = i

    return biggest_real_ellipse

'''returns a tuple of the angle of incidence and the angle at which the ellipse is slanted.'''
def get_target_data(target):
    if target is None:
        # print("no target visible")
        return
    theta = math.acos(np.min(target[1])/np.max(target[1])) # angle of incidence, measured from the normal. radians
    angle_of_ellipse = math.radians(target[2]) # radians
    #focal_length = 0.00474 #meters TODO: is this correct?
    #corrected_diameter = 
    #distance = math.cos(theta)
    return (theta, angle_of_ellipse)

#test purposes
# if __name__ == '__main__':
#     image = cv2.imread("Ellipses.png")
#     filtered_ellipses = [find_largest_ellipse(image)]

#     print(get_target_data(filtered_ellipses[0]))

#     test = np.zeros(image.shape, np.uint8)
#     box_points = [None]*len(filtered_ellipses)
#     for i, x in enumerate(filtered_ellipses):
#         if x is not None:
#             box_points[i] = cv2.boxPoints(x).astype(np.int32)
#         #print(box_points)
#     for y in box_points:
#         if y is not None:
#             cv2.fillConvexPoly(img=test, points=y, color=(255, 0, 0))
#             cv2.imshow("test", test)

#     cv2.waitKey(0)

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Failed to read frame")
            break

        filtered_ellipses = [find_largest_ellipse(frame)]
        print(get_target_data(filtered_ellipses[0]))

        box_points = [None]*len(filtered_ellipses)
        for i, x in enumerate(filtered_ellipses):
            if x is not None:
                box_points[i] = cv2.boxPoints(x).astype(np.int32)
            #print(box_points)
        for y in box_points:
            if y is not None:
                cv2.fillConvexPoly(img=frame, points=y, color=(255, 0, 0))
        cv2.imshow("test", frame)
        cv2.waitKey(1)