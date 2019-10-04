# Sterio Camera

# Step 1 see if the camera is working
```cmd
cd C:\Temp\OpenCV2Cam\
py -3.6 test.py

```
You should see a video feed

# Step 2 Calibrate the Camera
To Calibrate:
1. print the checker board in the scripts folder.  Attach the image to a flat board.


```cmd
cd C:\Temp\OpenCV2Cam\Calibration
py -3.6 CalibrateCamera.py

```

# Step 3 sterio record video



To Run
```cmd
cd C:\Temp\OpenCV2Cam
py -3.6 2cam.py -folder=test
```

# Step 4 (Optional)
Run scripts from the scripts folder to make the job faster