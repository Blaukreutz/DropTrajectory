import cv2
from Image_Processing import *

cap = cv2.VideoCapture("/dev/video10", cv2.CAP_V4L2)

if not cap.isOpened():
    print("Failed to open video capture")
    exit()

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Failed to read frame")
        break

    # If you're debugging, show the frame:
    # cv2.imshow("preview", frame)

    try:
        data = get_target_data(find_largest_ellipse(frame))
        if data is not None:
            print(data)
    except Exception as e:
        print(f"Processing error: {e}")

    key = cv2.waitKey(20)
    if key == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()