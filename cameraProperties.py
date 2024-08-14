
import shlex, subprocess
import re
import numpy
import pandas as pd
import PySimpleGUI as sg
def cleanCMD(__cmd:str):
    cmd =__cmd[14:].replace('  ', '')
    new=re.split('0x|:|\n',cmd)#delimits
    temp=[x for x in new if x]#removes empty strings
    temp.remove('Camera Controls')
    classType_=temp[1::3]
    i=0
    for item in classType_:
        item=re.sub(' ','',item)
        classType_[i]=item[9:-1:]
        i+=1
    #classType_=classIdent_(classType_)
    ctrls=temp[0::3]
    vals=temp[2::3]
    #print(ctrls)
    key, vals=returnNums(ctrls,vals)
    return createDict(key,vals), classType_

def returnNums(keys:list,vals:list):
    i=0
    for item in vals:
        item=re.sub(r'[a-z]|[A-Z]|=|\([^)]*\)','',item)
        item=list(filter(None,re.split(' ',item)))
        vals[i]=item
        i+=1
    return keys, vals

def createDict(keys:list,vals:list):
    camera_controls=dict.fromkeys(keys)
    for key, value in zip(camera_controls.keys(), vals):
        camera_controls[key] = value
    return camera_controls

def classIdent_(classTypes:list):
    i=0
    tempDict={'int':1,
              'bool':2,
              'menu':3}
    for item in classTypes:
        item=tempDict[item]
        classTypes[i]=item
        i+=1
    return classTypes

def optionCreator(camera_controls, classType,toggleswitch):
    test=list()
    i=0
    for key in camera_controls:
        tempKey=camera_controls.get(key)
        match classType[i]:
            case 'int':
                print('int')
                tempSlide=[sg.Text(key),sg.Slider((int(tempKey[0]),int(tempKey[1])),orientation='horizontal')]
            case 'bool':
                print('bool')
                tempSlide=[sg.Button('',image_data=toggleswitch, key='-TOGGLE-GRAPHIC-', button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)]
            case 'menu':
                print('menu')
                tempSlide=[sg.Slider((int(tempKey[0]),int(tempKey[1])),orientation='horizontal')]
        #print(type(tempSlide))
        test.append(tempSlide)
        i+=1
    return test
    


#start_process()
if __name__=='__main__':
    import PySimpleGUI as sg
    #hellotest()
    #start_process()
    cmd='v4l2-ctl --device /dev/video2 --list-ctrls'
    args=shlex.split(cmd)
    process=subprocess.run(args,stdout=subprocess.PIPE).stdout.decode('utf -8')
    #print(process)
    camera_controls, classType_ =cleanCMD(process)
    print(camera_controls)
    print(classType_)

    '''
    brightness=camera_controls.get(' brightness ')
    print(int(brightness[0]))
    test=list()
    print(type(test))
    i=0
    for key in camera_controls:
        tempKey=camera_controls.get(key)
        
        tempSlide=[sg.Slider((int(temp[0]),int(temp[1])),orientation='horizontal')]
        print(type(tempSlide))
        test.append(tempSlide)
    '''
    toggleswitch=b'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'
    test=optionCreator(camera_controls,classType_,toggleswitch)
    #slider=[[sg.Slider((int(brightness[0]),int(brightness[1])),orientation='horizontal',default_value=int(brightness[3]))]]
    window=sg.Window('test',layout=test)
    while True:
        event, values = window.read()
        if event==sg.WIN_CLOSED or event=='Exit':
            break