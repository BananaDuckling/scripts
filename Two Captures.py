import cv2 as cv
import subprocess
import PySimpleGUI as sg
import time

from HydraCam import testCamera
def initCam(camID:int=0):
    pass

def imageCap(camID:int=0):
    cap=testCamera(camID,30)
    cap2=testCamera(4,30)
    while cap.isOpened() & cap2.isOpened():
        ret1, frame1 =cap.read()
        time1=int(time.time()*1000)
        ret2, frame2 =cap2.read()
        time2=int(time.time()*1000)
        if not ret1 or not ret2:
            cap.release()
            cap2.release()
            return None
        frame=cv.hconcat([frame1,frame2])
        cv.putText(frame, str(time2-time1),(10,30),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),thickness=3)
        cv.imshow('Recording',frame)
        if cv.waitKey(1)==32:
            cv.destroyWindow('Recording')
            break
        pass



    pass

if __name__=="__main__":

    imageCap(2)
    pass
