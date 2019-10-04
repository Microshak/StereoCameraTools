import numpy as np
import cv2
import glob




import cv2
import threading
import datetime


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.



class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print ("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

    
def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
        return datetime.datetime.now().strftime(fmt).format(fname=fname)

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID + cv2.CAP_DSHOW)
    
    cam.set(3, 1920)
    cam.set(4, 1080)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))
    out = cv2.VideoWriter('Videos/'+timeStamped(previewName)+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
 
    while rval:
 #       out.write(frame)
      #  cv2.imshow(previewName, frame)

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
                break      
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        rval, frame = cam.read()

    # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
        print(ret)
    # If found, add object points, image points (after refining them)
    
        if ret == True:
            objpoints.append(objp)
            img = frame
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
            cv2.imshow(previewName, img)
            
        
    
        
    cv2.destroyWindow(previewName)

# Create two threads as follows
thread1 = camThread("Camera 1", 0)
thread2 = camThread("Camera 2", 1)
thread1.start()
thread2.start()













