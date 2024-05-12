'''
Creating a GUI Interface
'''

#Step 0, Library Installations

import PySimpleGUI as sg
import cv2 as cv
import os
import time


def testCamera(cameraInput,FPS): #Checks if the camera is able to be connected to 
    cap=cv.VideoCapture(cameraInput)
    if cap.isOpened()==False:
        sg.popup_error('Camera not connected or detected',title='Connection Error')
    else:
        cap.set(cv.CAP_PROP_FPS,FPS)
    return cap

def checkParam(values): #Checks if there are any key parameters missing
    if '' in values.values() : 
        sg.PopupError('Error Missing Parameters')
        liveCapture=False
    else:
        liveCapture=True
    return liveCapture

def createDirectory(folderName): #Creates a directory if it does not exist
    print(folderName)
    if os.path.exists(folderName) == False:
        print('Making Dir')
        os.mkdir(folderName) #Creates a folder
    return folderName

def frameCapture(timeInt,frameNum,folderName,cap): #To capture the frame into a folder
    i=0
    j=0
    temp=os.path.join(folderName,'Run'+str(j))
    createDirectory(temp)
    tempDir=os.path.join(temp,'Test Frame')
    print(tempDir+str(i)+'.tiff')
    window.hide()
    time1=-timeInt
    while cap.isOpened() :

        time2=int(time.time()*1000)
        if (time2-time1) >= timeInt:
            testtime=int(time.time()*1000)
            for x in range(0,frameNum):
                ret, frame = cap.read()
                if not ret:
                    sg.popup_error("Can't receive frame (stream end?). Exiting ...",auto_close=True)
                    return
                frame = cv.flip(frame, 0)
                timeThen=int(time.time()*1000)
                cv.imwrite(tempDir+str(i)+'.jpg',frame)
                #cv.putText(frame,'Press "v" to Exit',(10,30),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
                print(int(time.time()*1000)-timeThen)
                cv.imshow('Recording', frame)
                i+=1
                if cv.waitKey(1) == ord('v'):
                    break

            time1=int(time.time()*1000)
            print(time1-testtime)
            i=0
            j+=1
            temp=os.path.join(folderName,'Run'+str(j))
            createDirectory(temp)
            tempDir=os.path.join(temp,'Test Frame')

        if cv.waitKey(1)==ord('v'):
            break
    cv.destroyWindow('Recording')
    window.UnHide()
    return

###Creating a new folder with user input###

path=os.path.join(os.getcwd(),'Testing Runs') #Combines the directory and folder name together
if os.path.exists(path) == False:
    os.mkdir(path) #Creates a folder

liveToggle=False


sg.theme('DarkBlack')

###Camera Settings###
camFrame= [[sg.Text('Camera Channel'), sg.Combo([0,1,2],s=(2,1),enable_events=True,key='-CAM-',readonly=True,default_value=0)],
           [sg.Text('Frame Rate'), sg.Combo([10,20,30],s=(2,1),enable_events=True,key='-INPUT-',readonly=True,default_value=30)]]
           
#Recording Parameters UI
paraFrame= [[sg.Text('Hr:'), sg.Input(s=5,enable_events=True,key='-HRS-'),
          sg.Text('Min:'),sg.Input(s=5,enable_events=True,key='-MIN-'),
          sg.Text('Sec:'),sg.Input(s=5,enable_events=True,key='-SEC-')]]

#Test Folder Button
folderButton= [sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLD-'), sg.FolderBrowse(initial_folder=path)]

### Edit the layout of the GUI ###
layout= [[sg.Frame('Camera Settings',camFrame)], #Camera Settings
         #[sg.Text('Enter Folder Name'), sg.Input(s=15,enable_events=True,key='-FOLDER-'), sg.Text('',key='-ERR-',text_color='red',)],
         folderButton,
         [sg.Text('Time per Recording (s)'), sg.Input(s=10,enable_events=True,key='-RECORDING-')],
         [sg.Frame('Recording Interval',paraFrame)], #Recording Parameters
         [sg.Push(),sg.Button(button_text='Live Camera',s=15,enable_events=True,key='-ENTER-'),sg.Button(button_text='Record',s=15,enable_events=True,key='-CAPTURE-'),sg.Push()]]
         
### Finalize the Window ###
window=sg.Window('Hydra in a Box',layout,finalize=True)

### Actions ###
while True:
    event, values =window.read()
    
    ### Folder Name ###
    if event=='-FOLD-':
        print(values['-FOLD-'])

    ### Frame Rate Input ###
    if event == '-INPUT-' :
        print(values['-INPUT-'])

    ### Recording Parameters ###
    if (event == '-RECORDING-' or event == '-HRS-' or event == '-MIN-' or event== '-SEC-') and len(values[event])!=0:
        if values[event][-1].isnumeric()==False:
            window[event].Update(values[event][:-1])

    ### Live Capture Button ###
    if event == '-ENTER-':
        cap=testCamera(values['-CAM-'],values['-INPUT-'])
        window.hide()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            frame = cv.flip(frame, 0)
            cv.imshow('Live Feed', frame)
            #window['-ENTER-'].update(data=img)
            if cv.waitKey(1) == ord('q'):
                cv.destroyWindow('Live Feed')                
                break
        window.UnHide()
        cap.release()

    ### Record Button ###
    if event == '-CAPTURE-':
        liveCapture=checkParam(values)
        userDir=createDirectory(values['-FOLD-'])
        if liveCapture==True: #If all boxes are filled, proceed with live capturing
            cap=testCamera(values['-CAM-'],values['-INPUT-'])
            timeInt=(int(values['-HRS-'])*3600+int(values['-MIN-'])*60+int(values['-SEC-']))*1000
            frameNum=int(values['-RECORDING-'])*int(values['-INPUT-'])
            print(timeInt)
            print(frameNum)
            #createDirectory()
            frameCapture(timeInt, frameNum,userDir,cap)

        liveCapture=False 
        
    ### Exit Protocol ###
    if event == sg.WIN_CLOSED or event =='Exit':
        break

cv.destroyAllWindows()