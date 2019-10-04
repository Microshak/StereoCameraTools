import numpy as np
import cv2
import glob
import pickle


cap = cv2.VideoCapture(0)


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

cap.set(3, 1920)
cap.set(4, 1080)
mtx, dist, rvecs, tvecs,h,  w ,newcameramtx, roi = None,None,None,None,None,None,None,None
Calebrated = False
while(True):
# Capture frame-by-frame
    ret, frame = cap.read()

    if frame.any() and Calebrated == False:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
        print(ret)
        
        if ret == True:
                objpoints.append(objp)

                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2)

                # Draw and display the corners
                img = cv2.drawChessboardCorners(frame, (7,6), corners2,ret)
                cv2.imshow('frame',img)
                Calebrated = True
            # cv2.waitKey(5000)
                ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
                h,  w = img.shape[:2]
                newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
                tupl = (mtx, dist, rvecs, tvecs,h,  w ,newcameramtx, roi)
                with open('calibration.pickle', 'wb') as f:
                    pickle.dump(tupl, f)
        else:
            cv2.imshow('frame',frame)
    elif Calebrated == True:
            
            cv2.imshow('uncalibrated',frame)
            dst1 = cv2.undistort(frame, mtx, dist, None, newcameramtx)
            print('Calibrating')
            # crop the image
            x1,y1,w1,h1 = roi
            dst1 = dst1[y1:y1+h1, x1:x1+w1]
            cv2.imshow('Calibration 1',dst1)


            # undistort
            mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w1,h1),5)
            dst2 = cv2.remap(frame,mapx,mapy,cv2.INTER_LINEAR)
            dst2 = dst2[y1:y1+h1, x1:x1+w1]
            cv2.imshow('Calibration 2',dst2)
            
    else:
            cv2.imshow('frame',gray)
            pass
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()