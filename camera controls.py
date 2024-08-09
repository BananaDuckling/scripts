import shlex, subprocess
import re
import numpy
def cleanCMD(__cmd:str):
    cmd =__cmd[14:].replace('  ', '')
    new=re.split('0x|:|\n',cmd)#delimits
    temp=[x for x in new if x]#removes empty strings
    temp.remove('Camera Controls')
    ctrls=temp[0::3]
    vals=temp[2::3]
    key, vals=returnNums(ctrls,vals)
    camera_controls=createDict(key,vals)
    return createDict(key,vals)

def returnNums(keys:list,vals:list):
    i=0
    camCtrls={}
    for item in vals:
        item=re.sub(r'[a-z]|[A-Z]|=|\([^)]*\)','',item)
        item=re.split(' ',item)
        item=list(filter(None,item))
        vals[i]=item
        i+=1
    return keys, vals

def createDict(keys:list,vals:list):
    camera_controls=dict.fromkeys(keys)
    for key, value in zip(camera_controls.keys(), vals):
        camera_controls[key] = value
    return camera_controls

#start_process()
if __name__=='__main__':
    import PySimpleGUI as sg
    #hellotest()
    #start_process()
    cmd='v4l2-ctl --device /dev/video2 --list-ctrls'
    args=shlex.split(cmd)
    process=subprocess.run(args,stdout=subprocess.PIPE).stdout.decode('utf -8')
    camera_controls=cleanCMD(process)
    brightness=camera_controls.get(' brightness ')
    print(int(brightness[0]))
    test=list()
    print(type(test))
    i=0
    for key in camera_controls:
        temp=camera_controls.get(key)
        tempSlide=[sg.Slider((int(temp[0]),int(temp[1])),orientation='horizontal')]
        print(type(tempSlide))
        test.append(tempSlide)
    
    slider=[[sg.Slider((int(brightness[0]),int(brightness[1])),orientation='horizontal',default_value=int(brightness[3]))]]
    window=sg.Window('test',test,finalize=True)
    while True:
        event, values = window.read()
        if event==sg.WIN_CLOSED or event=='Exit':
            break
    