import cv2 as cv
import numpy as np
video = "/path/to/video"

cam = cv.VideoCapture(video)

while cam.isOpened():
    isReadingOK, newFrame = cam.read()
    grayFrame = cv.cvtColor(newFrame, cv.COLOR_BGR2GRAY)
    args = cv.SimpleBlobDetector_Params()
    args.filterByCircularity = True
    args.minCircularity = 0.1
    args.filterByConvexity = True
    args.minConvexity = 0.1
    args.filterByInertia = True
    args.minInertiaRatio = 0.01
    args.filterByArea = True
    args.maxArea = 1000000
    args.minArea = 300

    finder = cv.SimpleBlobDetector_create(args)
    door = finder.detect(grayFrame)

    blank = np.zeros((1,1))
    drawing = cv.drawKeypoints(newFrame, door, blank, (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.imshow("deneme", drawing)
    if cv.waitKey(1) == ord('q'):
        break
