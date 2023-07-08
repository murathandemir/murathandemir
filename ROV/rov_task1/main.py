import numpy as np # importing numpy library for further use
import cv2 as cv # importing opencv for door detecting
import move # importing "move" class which contains basic move simulation with command line printing and i have written
video = "/path/to/video" # set this variable as the video's path

flag = -1 # 0 means you are on the right respectively to the door, 1 means you are on the left ...

def callXTimes (x, function): # i will need this function for avoiding spaghetti-code
    for x in range(2) : function()

def focusToCenter(obj): # function that focuses the center of the given object as a parameter. (i will use for circle focusing)
    x = obj.pt[0] # finding obj's x coordinate
    y = obj.pt[1] # finding obj's y coordinate
    if y > 360 : # that means : if obj appears on the above of the video's center
        while y != 360: # while obj's y coordinate is not equal to video's center
            move.Move.Spin.axis_x_positive()
    elif y < 360 : # that means : if obj appears on the below of the video's center
        while y != 360: 
            move.Move.Spin.axis_x_negative()
    else : None 

    if x > 640 : # that means : if obj appears on the right of the video's center
        flag = 1 # flag setted up for saying me "you are on the left of the obj"
        while x != 640 : # while obj's x coordinate is not equal to video's center
            move.Move.Spin.axis_y_negative()
    elif x < 640 : # that means : if obj appears on the left of the video's center
        flag = 0 # flag setted up for saying me "you are on the right of the obj"
        while x != 640 : 
            move.Move.Spin.axis_y_positive()
    else : None 

##############################################
#### BEGINNING OF THE DETECT & PRINT PART ####
##############################################

def takeNewFrame():
    input = cv.VideoCapture(video) # read the video
    if input.isOpened(): # obvious
        isReadingOK, newFrame = input.read() # read a new frame from the input and save it on variable, also we have isReadingOK var, but now i won't need it.
        grayFrame = cv.cvtColor(newFrame, cv.COLOR_BGR2GRAY) # for a better detecting, frame to grayscale.
        # setting up the parameters for our door detector
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
        # everything set up

        # creating a finder with our above arguments.
        finder = cv.SimpleBlobDetector_create(args)
        door = finder.detect(grayFrame) # detecting the door from gray scaled frame

        blank = np.zeros((1,1)) # for drawing, empty array.
        drawing = cv.drawKeypoints(newFrame, door, blank, (0,0,255), # creating our drawing, but we won't use that on there. If you want to see it, look my other code
                                    cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        # for a precaution, if our circle cant be detected, this code runs for avoiding crash.
        try: 
            if door is not None : # if our circle is detected, return it.
                ourCircle = door[0]
                return ourCircle
        except IndexError :
            pass

    
circle = takeNewFrame() # take the our circle with taking new frame.
while circle is None: # for again precaution, if circle couldn't be detected, ...
    move.Move.Linear.forward() # ... go forward a bit ...
    circle = takeNewFrame() # ... and take the circle.
########################################
#### END OF THE DETECT & PRINT PART ####
########################################

########################################
#### BEGINNING OF THE DECISION PART ####
########################################
# videos' sizes : 1280 * 720
# midpoint : 640 * 360
# growth limit : circle.size == 150 (my experimental data for optimum process)

focusToCenter(circle) # wherever we are, firstly focus to the center of "circle"

size = circle.size # just for a better look
while size < 150 : # go forward until having an enough distance from circle for following process.
    move.Move.Linear.forward() 

circle = takeNewFrame() # take a new frame and change the circle view
justBeforeSize = circle.size # it's simply saves the just one before position's circle's size.
if flag == 1: # if we have spanned on the left of the circle
    while 1:
        move.Move.Linear.left() # go just an unit to the left
        circle = takeNewFrame() # take a new frame and change the circle view
        focusToCenter(circle) # and again focus the center of the circle
        if circle.size > justBeforeSize: # now, if we have bigger view of circle,
            justBeforeSize = circle.size # we will continue, so i am saving current moment's viewing size.
            continue
        else: break # after moving just a bit, if we have a smaller view of circle, that means we have already come the opposite
        # of the circle on our before move.
elif flag == 0: # if we have spanned on the right of the circle
    while 1:
        move.Move.Linear.right() # go just an unit to the right
        circle = takeNewFrame() # take a new frame and change the circle view
        focusToCenter(circle) # and again focus the center of the circle
        if circle.size > justBeforeSize: # same logic with above code.
            justBeforeSize = circle.size
            continue
        else: break
# so after that all process, we know we are exactly opposite of circle. that means we can go into circle.
focusToCenter(circle) # focus to center and ...
callXTimes(100, move.Move.Linear.forward) # dive into circle.
