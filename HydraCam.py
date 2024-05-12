'''
Creating the commands for the PySimpleGUI
'''




def createDirectory(folderName): #Creates a directory if it does not exist
    if os.path.exists(folderName) == False:
        os.mkdir(folderName) #Creates a folder
    return None

def testCamera(camera:int,FPS:int,AUTOEXPOSURE:int=1,): #Checks if the camera is able to be connected to 
    cap=cv.VideoCapture(cameraInput)
    if cap.isOpened()==False:
        sg.popup_error('Camera not connected or detected',title='Connection Error')
    else:
        cap.set(cv.CAP_PROP_FPS,FPS)
        ret_test, cap_test=cap.read()
        #cap.set(cv.CAP_PROP_AUTO_EXPOSURE,3)
        cap.set(cv.CAP_PROP_AUTO_EXPOSURE,1.0)
        cap.set(cv.CAP_PROP_EXPOSURE,10.0)
        print(cap.get(cv.CAP_PROP_AUTO_EXPOSURE))
    return cap

'''
DEPRECATED


def frameCapture(timeInt:int,frameNum:int,folderName:str): #To capture the frame into a folder
    i=0
    j=0
    temp=os.path.join(folderName,'Run'+str(j))
    tempDir=createDirectory(temp)
    #window.hide()
    time1=-timeInt
    while cap.isOpened() :
        tempDir=os.path.join(folderName,'Run'+str(j))

        time2=int(time.time()*1000)
        if (time2-time1) >= timeInt:
            testtime=int(time.time()*1000)
            for x in range(0,frameNum):
                ret, frame = cap.read()
                if not ret:
                    sg.popup_error("Can't receive frame (stream end?). Exiting ...",auto_close=True)
                    return None
                frame = cv.flip(frame, 0)
                #cv.imwrite(tempDir+'/Test Frame'+str(i)+'.tiff',frame)
                cv.putText(frame,'Press "Space" to Exit',(10,30),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
                cv.imshow('Recording', frame)
                i+=1
                if cv.waitKey(1) == 32:
                    break

            time1=int(time.time()*1000)
            print(time1-testtime)
            i=0
            j+=1
            temp=os.path.join(folderName,'Run'+str(j))
            tempDir=createDirectory(temp)
        if cv.waitKey(1)==ord('v'):
            break
    cv.destroyWindow('Recording')
    #window.UnHide()
    return

'''

'''
DEPRECATED

def liveFeed(camera:int,FPS=30,capture=False):
    cap=testCamera(camera,FPS)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        #frame = cv.flip(frame, 0)
        cv.putText(frame,'Press "Space" to Exit',(10,30),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
        cv.imshow('Live Feed', frame)
        #window['-ENTER-'].update(data=img)
        if cv.waitKey(1) == 32:
            cv.destroyWindow('Live Feed')                
            break
    cap.release()
    return

'''

def runFeed(camera:int,FPS:int=30,capture:bool=False,timeRecord:int=None,timeInt:int=None,folder:str=None):

    if FPS>30: #Frame Rate Cap (Most Consistent Frame Rate)
        FPS=30

    if capture==True: #Check if the arguments entered are all met
        if folder==None or timeInt==None or timeRecord==None: #Checks if all parameters are met if capture was turned on
            return sg.PopupError("Missing Folder Name or Time Interval")
        elif os.path.exists(folder): #If capture was turned all and all parameters were entered
            j=0
            frameNum=FPS*timeRecord
            temp=os.path.join(folder,'Run'+str(j))
            createDirectory(temp)
            imageLabel=temp+'/Test Frame'
            timeInt=timeInt*1000
        else:
            return sg.PopupError("Error: Please Enter Valid Directory")
    else:
        frameNum=1

    i=0 #Temp Variable
    cap=testCamera(camera,FPS) #Establishes the camera object
    time1=-timeInt
    while cap.isOpened():
        time2=int(time.time()*1000)
        if (time2-time1) >= timeInt:
            testtime=int(time.time()*1000)
            while i<frameNum:
                ret, frame = cap.read()
                if not ret:
                    sg.popup_error("Can't receive frame (stream end?). Exiting ...",auto_close=True)
                    cap.release()
                    return None
                #frame = cv.flip(frame, 0)
                if capture==True:
                    cv.imwrite(imageLabel+str(i)+'.tiff',frame)
                    i+=1
                cv.putText(frame,'Press "Space" to Exit',(10,30),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),thickness=3)
                cv.imshow('Recording', frame)
                if cv.waitKey(1) == 32:
                    cv.destroyWindow('Recording')
                    cap.release()
                    return None
                            
            time1=int(time.time()*1000)
            print(i)
            print(time1-testtime)
            i=0
            j+=1
            temp=os.path.join(folder,'Run'+str(j))
            createDirectory(temp)
            imageLabel=temp+'/Test Frame'
        if cv.waitKey(1)==32:
            cv.destroyWindow('Recording')
            break
    cap.release()
    return None



if __name__=="__main__":
    import cv2 as cv
    import PySimpleGUI as sg
    import subprocess
    import os 
    import time

    cam_props = {'brightness': 128, 'contrast': 128, 'saturation': 180,
             'gain': 0, 'sharpness': 128, 'exposure_auto': 1,
             'exposure_absolute': 150, 'exposure_auto_priority': 0,
             'focus_auto': 0, 'focus_absolute': 30, 'zoom_absolute': 250,
             'white_balance_temperature_auto': 0, 'white_balance_temperature': 3300}


    cameraInput=0
    FPS=50 #Frames Per Second
    #liveFeed(cameraInput,FPS)
    runFeed(0,capture=True,folder='/home/bryan/Environments/project1_env/scripts/Tests',timeInt=10, timeRecord=10,FPS=FPS)
