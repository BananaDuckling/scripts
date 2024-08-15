import cv2
import time
import multiprocessing as mp
import shlex, subprocess

def open_cam(camID,check):
    count = 0
    timePass=[]
    cam = cv2.VideoCapture(camID)
    while True:
        ret_val, img = cam.read()
        timePass.append(int(time.time())*1000)
        cv2.imshow("Image", img)
        count += 1
        if (cv2.waitKey(1) & 0xFF) == ord('q') or check.value==0:
            check.value=0
            break

    cv2.destroyAllWindows()

def open_cam2(camID):
    count = 0
    cam = cv2.VideoCapture(camID)
    while True:
        ret_val, img = cam.read()
        #print(ret_val)
        cv2.imshow("Image", img)
        count += 1
        if count == 100:
            break
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            break
    cv2.destroyAllWindows()


def start_process():
    print("CREATING process")
    x=mp.Value('i',1)
    cam_process = mp.Process(name='Cam1',target=open_cam,args=[2,x])
    cam_process2 = mp.Process(name='Cam2',target=open_cam,args=[4,x])
    print("STARTING process")
    cam_process.start()
    cam_process2.start()

def start_process2(cameraID):
    print("CREATING process")
    cam_process = multiprocessing.Process(target=open_cam2(cameraID))
    print("STARTING process")
    cam_process.start()


def add(x,y):
    for i in range(0,10):
        time.sleep(2)
        print(x+y)
    pass

def sub(x,y):
    for i in range(0,10):
        time.sleep(2)
        print(x-y)
    pass
def hellotest():
    x=2
    y=3
    test1= multiprocessing.Process(target=add,args=[x,y])
    test2= multiprocessing.Process(target=sub,args=[x,y])
    test1.start()
    test2.start()

#start_process()
if __name__=='__main__':
    #hellotest()
    start_process()
    #cmd='v4l2-ctl --device /dev/video2 --list-ctrls'
    #args=shlex.split(cmd)
    #process=subprocess.check_output(args)
    #output, err = process.communicate()
    #print(process)