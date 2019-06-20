import cv2
import numpy as np
import time

lowerBound=np.array([0,50,200])
upperBound=np.array([180,128,255])

cam= cv2.VideoCapture("MOV_0840.mp4")

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

while True:
    start = time.time()
    ret, img=cam.read()
    img=cv2.resize(img,(340,220))
    
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    mask=cv2.inRange(imgHSV,lowerBound,upperBound)

    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    maskFinal=maskClose

    _ , conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    cv2.drawContours(img,conts,-1,(255,0,0),3)
    statusText = "standby"
    colorRed = (0,0,255)
    colorGreen = (0,255,0)
    statusColor = colorRed

    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
	cv2.putText(img,"TARGET",(x - 5 , y - 5), cv2.FONT_HERSHEY_SIMPLEX,
	0.5, (0, 255 , 0),lineType=cv2.LINE_AA)
	if x + (h / 2) > 170:
		statusText = "RIGHT"
		statusColor = colorRed
	elif x + (h / 2) < 150:
		statusText = "LEFT"
		statusColor = colorRed
	else:
		statusText = "LINED"
		statusColor = colorGreen 
	cv2.putText(img, statusText ,(x , y + 5 + w),cv2.FONT_HERSHEY_SIMPLEX,0.5,
	statusColor,lineType=cv2.LINE_AA)
	cv2.imshow("maskClose",maskClose)
	end = time.time()
	seconds = end - start
	fps = "Current FPS is: " + str(1 / seconds)
	cv2.putText(img, fps ,(20 , 20),cv2.FONT_HERSHEY_SIMPLEX,0.5,
	colorGreen,lineType=cv2.LINE_AA)
    cv2.imshow("maskOpen",maskOpen)
    cv2.imshow("mask",mask)
    cv2.imshow("cam",img)
    
    
    cv2.imshow("mask",mask)
    cv2.imshow("cam",img)
    cv2.waitKey(10)
    
