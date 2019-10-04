import cv2
import threading
import datetime
import pickle
import argparse
import os
import time
import sys

class camThread(threading.Thread):
    def __init__(self, previewName, camID, folder):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.folder = folder
    def run(self):
        print ("Starting " + self.previewName)
        camPreview(self.previewName, self.camID, self.folder)

    
def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
        return datetime.datetime.now().strftime(fmt).format(fname=fname)

def camPreview(previewName, camID, folder):
    mtx, dist, rvecs, tvecs,h,  w ,newcameramtx, roi = None,None,None,None,None,None,None,None
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
    print(folder)
    with open('Calibration/calibration.pickle', 'rb') as f:
        data = pickle.load(f)
        (mtx, dist, rvecs, tvecs,h,  w ,newcameramtx, roi) = data
    x1,y1,w1,h1 = roi

    out = cv2.VideoWriter(VideoPath+timeStamped(previewName)+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 5, (w1,h1))
    
    start = time.time()
    while rval:


        dst1 = cv2.undistort(frame, mtx, dist, None, newcameramtx)
            # crop the image
        
        dst1 = dst1[y1:y1+h1, x1:x1+w1]

        if (time.time()- start) > 3:
            out.write(dst1)

        cv2.imshow(previewName, dst1)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            print('break')
            sys.exit()
            break
        
        
         
        if (time.time()- start) > 13:
            cv2.destroyWindow(previewName)
            out.release()
            sys.exit()
            
    cv2.destroyWindow(previewName)

# Create two threads as follows
def makeFolder(directory):

    VideoPath = 'Videos/' +directory + '/'

    if not os.path.exists(VideoPath ):
        os.makedirs(VideoPath)
    return VideoPath


parser = argparse.ArgumentParser(description='This is a 2 camera recorder')
parser.add_argument('-folder', default="", type=str,    help='what folder do you want the videos')
args = parser.parse_args()
VideoPath = makeFolder(args.folder)



thread1 = camThread("Camera 1", 0, VideoPath)
thread2 = camThread("Camera 2", 1, VideoPath)
thread1.start()
thread2.start()


