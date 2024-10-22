import cv2 as cv
from PIL import ImageTk, Image
import vision
from datetime import datetime
from customtkinter import CTkImage


def importLog():
    with open('log.txt') as f:
        lines = f.readlines()
    i=len(lines)
    return i

i=importLog()+1

def camActivate():
    global cap
    cap = cv.VideoCapture(0)
    cap.set(4,640)
    cap.set(3,480)
    cap.set(cv.CAP_PROP_BUFFERSIZE,0)


def camPutImage():
    global cap
    img=cv.cvtColor(cap.read()[1],cv.COLOR_BGR2RGB)
    img=cv.flip(img,1)
    im = Image.fromarray(img)
    imgCam=CTkImage(light_image=im,dark_image=im,size=(640,480))
    return imgCam

def detectionActivate():
    global cap
    cascade_defect=cv.CascadeClassifier('cascade/cascade.xml')
    vision_defect = vision.Vision(None)
    img = cap.read()[1]
    img = cv.flip(img,1)
    rectangles = cascade_defect.detectMultiScale3(
        img,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(20, 20),
        maxSize=(200, 200),
        flags = cv.CASCADE_SCALE_IMAGE,
        outputRejectLevels = True
    )
    imgDetect = vision_defect.draw_rectangles(img,rectangles[0])
    imgDetect=cv.cvtColor(imgDetect,cv.COLOR_BGR2RGB)
    im = Image.fromarray(imgDetect)
    imgDetect=CTkImage(light_image=im,dark_image=im,size=(640,480))
    return imgDetect

def closeCam():
    global cap
    cap.release()

def getLogDescription():
    global i,cap

    cascade_defect=cv.CascadeClassifier('cascade/cascade.xml')
    vision_defect = vision.Vision(None)
    img=cv.cvtColor(cap.read()[1],cv.COLOR_BGR2RGB)
    img = cv.flip(img,1)
    rectangles = cascade_defect.detectMultiScale3(
        img,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(20, 20),
        maxSize=(200, 200),
        flags = cv.CASCADE_SCALE_IMAGE,
        outputRejectLevels = True
    )
    imgDetect = vision_defect.draw_rectangles(img,rectangles[0])
    imgDetect = cv.cvtColor(imgDetect,cv.COLOR_BGR2RGB)
    description ="defect_log/detected-{}.jpg -- {} Defects Detected -- {}".format(i,len(rectangles),datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    cv.imwrite("defect_log/detected-{}.jpg".format(i),imgDetect)
    i+=1
    return description

def resizeOpenedImage(obj):
    if isinstance(obj,str):
        img=Image.open(obj)
    else:
        img=Image.fromarray(obj)

    imgTK=ImageTk.PhotoImage(img)
    width=imgTK.width()
    height=imgTK.height()
    if width>height:
        multiplier=width/640

    elif height>width:
        multiplier=height/480

    elif width>640 and width == height:
        multiplier=width/640

    else:
        multiplier=640/width
    # imgResized= img.resize((int(width/multiplier),int(height/multiplier)), Image.LANCZOS)
    return CTkImage(img,size=(int(width/multiplier*0.8),int(height/multiplier*0.8)))

def pictureDetection(path):
    img = cv.imread(path)
    cascade_defect=cv.CascadeClassifier('cascade/cascade.xml')
    vision_defect = vision.Vision(None)
    rectangles = cascade_defect.detectMultiScale3(
            img,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(20, 20),
            maxSize=(200, 200),
            flags = cv.CASCADE_SCALE_IMAGE,
            outputRejectLevels = True
        )
    imgDetect = vision_defect.draw_rectangles(img,rectangles[0])
    imgDetect = cv.cvtColor(imgDetect,cv.COLOR_BGR2RGB)
    imgResized = resizeOpenedImage(imgDetect)
    return imgResized