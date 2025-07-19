import mediapipe as mp
import cv2
import numpy as np
import pyautogui as pg

mpfaces=mp.solutions.face_detection
mpdrawings=mp.solutions.drawing_utils

faces=mpfaces.FaceDetection(min_detection_confidence=0.6)
threshold=30 # in pixels 
l=None

video=cv2.VideoCapture(0)
while True:
  suc,img=video.read()
  img=cv2.flip(img,1)
  img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
  result=faces.process(img1)
  h,w,_=img.shape
  cx=(w//2)-50
  cy=(h//2)+50
  cv2.circle(img,(cx,cy),3,(0,0,255),10)
  if result.detections:
    for detection in result.detections:    
      keypoints=detection.location_data.relative_keypoints
      nose_tip=keypoints[2]
      nose_x=int(nose_tip.x * w)
      nose_y=int(nose_tip.y * h)
      # cv2.circle(img,(nose_x,nose_y),5,(255,0,0),-1)
      dx=nose_x-cx
      dy=nose_y-cy
      if abs(dx)<threshold and abs(dy)<threshold: # to enable or to activate movement, when head is moved!!
        l=None
        continue
      d=None
      if abs(dx)>abs(dy): # to check if the direction is enable along x axis
        if dx<0:
          d='left'
        else:
          d='right'
      else:
        if dy<0:            
          d='up'
        else:
          d='down'
      if d!=l:
        print("Direction:",d)
        pg.press(d)
        l=d
  cv2.imshow("Image",img)
  if cv2.waitKey(1) & 0XFF==113:
    break
video.release()
cv2.destroyAllWindows()



