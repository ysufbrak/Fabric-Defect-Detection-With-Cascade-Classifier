from tkinter import *
import customtkinter as ctk
from tkinter.filedialog import askopenfilename
import uifunctionsV2 as uiv2
import time

root=ctk.CTk(screenName="Fabric Defect Detection")
root.title("Fabric Defect Detection")

w = 1280
h = 720

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight() 
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

root.geometry('%dx%d+%d+%d' % (w, h, x, y-20))

#Needed Variables
isCamOn=False
isDetectionOn=False
logCam = False
indexlist = uiv2.importLog()+1

SwitchScreenC=ctk.CTkButton(root,text="Cam Page")
SwitchScreenC.place(relx=0.1,rely=0.1,anchor=CENTER)

SwitchScreenP=ctk.CTkButton(root,text="Picture Page",fg_color="#444444",hover_color="#666666")
SwitchScreenP.place(relx=0.1,rely=0.2,anchor=CENTER)


#Passive Functions

def startLog():
    global logCam
    if logCam==False:
        logCam=True
        ButtonLogStC.configure(text="Stop Log")
    elif logCam==True:
        logCam=False
        ButtonLogStC.configure(text="Start Log")

def saveLog():
    logDefect=CamListbox.get(0,END)
    f = open('log.txt', 'a')
    for t in logDefect:
        f.write(t + '\n')
    f.close()
    CamListbox.delete(0,END)

def activateCam():
    global isCamOn
    if isCamOn==False:
        isCamOn=True
        ButtonCamA.configure(text="Deactivate Camera")
        uiv2.camActivate()
    elif isCamOn==True:
        isCamOn=False
        ButtonCamA.configure(text="Activate Camera")
        CamStatus.configure(image="",text="Camera is not active")
        CamStatus.place(relx=0.5,rely=0.5,anchor=CENTER)
        uiv2.closeCam()

def activateDetection():
    global isDetectionOn
    if isDetectionOn==False:
        isDetectionOn=True
        ButtonCamDA.configure(text="Stop Detection")
    elif isDetectionOn==True:
        isDetectionOn=False
        ButtonCamDA.configure(text="Start Detection")
        CamStatus.configure(image="",text="Camera is not active")
        CamStatus.place(relx=0.5,rely=0.5,anchor=CENTER)

def openImage():
    global file
    file = askopenfilename(filetypes =[("jpg images", "*.jpg"),("png files","*.png")],initialdir='.')
    img = uiv2.resizeOpenedImage(file)
    PictureStatus.configure(image=img,text='')
    PictureStatus.image=img    
    PictureStatus.place(x=0,y=0,anchor=CENTER,relx=0.5,rely=0.5)

def detectPicture():
    global file
    detectedPicture = uiv2.pictureDetection(file)
    PictureStatus.configure(image=detectedPicture,text='')
    PictureStatus.image=detectedPicture    
    PictureStatus.place(x=0,y=0,anchor=CENTER,relx=0.5,rely=0.5)
    pass

def clearFrame():
    PictureStatus.configure(image='',text="Open an Image")   
    PictureStatus.place(x=0,y=0,anchor=CENTER,relx=0.5,rely=0.5)

def PicturePage():
    global isCamOn, isDetectionOn, PictureFrame,PictureStatus
    for widget in root.winfo_children():
        if widget!=SwitchScreenC and widget!=SwitchScreenP and widget!=CamStatus:
            widget.place(relx=-1,rely=-1)
    
    isCamOn=False
    isDetectionOn = False
    PictureCombo=LabelFrame(root,text="Controls",bg="#222325",fg="silver")
    PictureCombo.place(relx=0.80,rely=0.225,relheight=0.3,relwidth=0.1)

    PictureFrame=ctk.CTkFrame(root,width=640,height=480)
    PictureFrame.place(relx=0.25,rely=0.025)

    PictureStatus=ctk.CTkLabel(PictureFrame,text='There isnt an image selected.')
    PictureStatus.place(relx=0.5,rely=0.5,anchor=CENTER)

    ButtonOImage=ctk.CTkButton(PictureCombo,text='Choose an image',command=openImage)
    ButtonOImage.place(relx=0.06,rely=0.1,relwidth=0.9)

    ButtonDImage=ctk.CTkButton(PictureCombo,text='Detect',command=detectPicture)
    ButtonDImage.place(relx=0.06,rely=0.4,relwidth=0.9)

    ButtonCImage=ctk.CTkButton(PictureCombo,text='Clear',command=clearFrame)
    ButtonCImage.place(relx=0.06,rely=0.7,relwidth=0.9)

    PictureListbox=Listbox(root,bg="#222325",fg='silver',
    highlightcolor="#222325",
    highlightbackground='#222325',
    selectbackground="#343635")
    PictureListbox.place(relx=0.25,rely=0.75,relwidth=0.5)
    
    SwitchScreenC.configure(fg_color="#444444",hover_color="#666666")
    SwitchScreenP.configure(fg_color="#1F6AA5",hover_color="#144870")

def CamPage():
    global CamStatus, ButtonCamA, ButtonCamDA, ButtonLogStC, CamListbox
    
    for widget in root.winfo_children():
        if widget!=SwitchScreenC and widget!=SwitchScreenP:
            widget.place(relx=-1,rely=-1)
    
    CamFrame=ctk.CTkFrame(root,width=640,height=480)
    CamFrame.place(relx=0.25,rely=0.025)

    CamStatus=ctk.CTkLabel(CamFrame,text='Camera is not active')
    CamStatus.place(relx=0.5,rely=0.5,anchor=CENTER)

    CamCombo=LabelFrame(root,text="Camera Controls",bg="#222325",fg="silver")
    CamCombo.place(relx=0.80,rely=0.225,relheight=0.3,relwidth=0.12)

    ButtonCamA=ctk.CTkButton(CamCombo,text='Activate Camera',command=activateCam)
    ButtonCamA.place(relx=0.06,rely=0.1,relwidth=0.9)

    ButtonCamDA=ctk.CTkButton(CamCombo,text='Start Detection',command=activateDetection)
    ButtonCamDA.place(relx=0.06,rely=0.7,relwidth=0.9)

    CamListC=LabelFrame(root,text="Log",bg="#222325",fg="silver")
    CamListC.place(relx=0.80,rely=0.76,relheight=0.2,relwidth=0.08)

    ButtonLogStC=ctk.CTkButton(CamListC,text='Start Logging',command=startLog)
    ButtonLogStC.place(relx=0.06,rely=0.1,relwidth=0.9)

    ButtonLogSaveC=ctk.CTkButton(CamListC,text='Save Log',command=saveLog)
    ButtonLogSaveC.place(relx=0.06,rely=0.7,relwidth=0.9)

    CamListbox=Listbox(root,bg="#222325",fg='silver',
    highlightcolor="#222325",
    highlightbackground='#222325',
    selectbackground="#343635")
    CamListbox.place(relx=0.25,rely=0.75,relwidth=0.5)

    SwitchScreenC.configure(fg_color="#1F6AA5",hover_color="#144870")
    SwitchScreenP.configure(fg_color="#444444",hover_color="#666666")

CamPage()

#Active Functions(Checks Statements and Apply)

def PutImage():
    if isCamOn==True and isDetectionOn==False:
        imgCam=uiv2.camPutImage()
        try:
            CamStatus.configure(image=imgCam,text='')
            CamStatus.image=imgCam    
            CamStatus.place(relx=0.5,rely=0.5,anchor=CENTER)
        except:
            pass

    elif isCamOn==True and isDetectionOn==True:
        imgCam=uiv2.detectionActivate()
        CamStatus.configure(image=imgCam)
        CamStatus.image=imgCam    
        CamStatus.place(relx=0.5,rely=0.5,anchor=CENTER)
    elif isCamOn==False and isDetectionOn==True:
        CamStatus.configure(image="",text="Can not start detection because camera is not active")
        CamStatus.place(relx=0.5,rely=0.5,anchor=CENTER)
    root.after(10,PutImage)

def addLog():
    global indexlist
    if isCamOn==True and isDetectionOn==True and logCam==True:
        defects=uiv2.getLogDescription()
        CamListbox.insert(indexlist,defects)
        indexlist+=1
    root.after(10000,addLog)

SwitchScreenC.configure(command=CamPage)

SwitchScreenP.configure(command=PicturePage)

root.after_idle(addLog)
root.after_idle(PutImage)
root.mainloop()