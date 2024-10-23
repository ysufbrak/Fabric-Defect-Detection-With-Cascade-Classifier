import tkinter as tk
from tkinter.messagebox import *
from tkinter.filedialog import askdirectory
import customtkinter as ctk
import os
import uimages

images=[] #Image Cache For Display
imagesrsz=[] #Image Cache For Buttons
button_dc={} #Dictionary for tk Buttons
imageNames={} #Dictionary for file names
coord=[] #Rectangle coordinate cache
rect_coord={} # Dictionary for calling back coordinates

global formatValue

root=ctk.CTk()
root.title('Annotation Tool')
w = 1280
h = 720

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight() 
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

root.geometry('%dx%d+%d+%d' % (w, h, x, y-20))

# Frame and canvas for displaying images and annotations
Frame=ctk.CTkFrame(root,border_color='black')
Frame.place(relwidth=1,relheight=0.25,relx=0,rely=0.75)

ImageCanvas=tk.Canvas(Frame,scrollregion=(0,0,0,0),bd=0,border=0,borderwidth=0,bg='gray20')
ImageCanvas.place(relheight=0.85,relwidth=1,relx=0)

# Canvas to display the selected image
DisplayCanvas=ctk.CTkCanvas(root,width=512,height=512,cursor="tcross",bg='gray20')
DisplayCanvas.place(relx=0.01,rely=0.075)

# Scrollbar for the image list
IScroll=ctk.CTkScrollbar(Frame,orientation='horizontal')
IScroll.place(relx=0,relwidth=1,rely=0.85,relheight=0.1)
IScroll.configure(command=ImageCanvas.xview)
ImageCanvas.configure(xscrollcommand=IScroll.set)

# Label to show image count
ImageCount=ctk.CTkLabel(ImageCanvas,text="0/0")
ImageCount.place(relx=0.95,rely=0.035)

var=tk.IntVar()

# Export options and file path input
ExportOpt=tk.LabelFrame(root,text="Export Options",background='gray20',font=('Arial',12),fg='silver')
ExportOpt.place(relx=0.60,relwidth=0.4,rely=0.01,relheight=0.72)

FilExport=ctk.CTkEntry(ExportOpt,placeholder_text='Select path',state='normal',fg_color='gray20')
FilExport.place(relx=0.025,rely=0.05,relwidth=0.85)

# Annotation format options
FormatOpt=tk.LabelFrame(ExportOpt,text='Format Options',bg='gray20',font=('Arial',12),fg='silver')
FormatOpt.place(relx=0.05,relwidth=0.4,rely=0.15,relheight=0.5)

yoloExp=ctk.CTkRadioButton(FormatOpt,text='YOLO Annotation Format',variable=var,value=1)
yoloExp.place(relx=0.05,rely=0.05)

cascadeExp=ctk.CTkRadioButton(FormatOpt,text='Cascade Annotation Format',variable=var,value=2)
cascadeExp.place(relx=0.05,rely=0.15)

# Listbox for annotation list
AnnotList=tk.Listbox(ExportOpt,bg='gray20',fg='silver',font=('arial',12))

AnnotList.place(relx=0.55,relwidth=0.4,rely=0.165,relheight=0.486)

AnnotListLabel=ctk.CTkLabel(ExportOpt,text='Annotation List')
AnnotListLabel.place(relx=0.57,rely=0.15,relheight=0.028)

AnnotList.insert(tk.END,'')

# Function to display the selected image and annotations
def displayImage(index,name):
    global nameimg
    global imageNames
    global coord
    global img
    coord=[]
    nameimg=name
    img=images[index]
    imageNames[img]=""
    DisplayCanvas.delete('all')
    imageNames[name] = DisplayCanvas.create_image(2,2,image=img,anchor=tk.NW)
    try:
        if rect_coord['{}'.format(nameimg)]:
            for element in rect_coord['{}'.format(nameimg)]:
                DisplayCanvas.create_rectangle(element[0],element[1],element[2],element[3],outline='red',tags='recs')
    except:
        pass

# Function to Save annotations
def saveannot():
    global annimage
    if tk.messagebox.askquestion('Annotation',message='Save Annotations?')=="yes":
        
        ImageCount.configure(text="{}/{}".format(len(rect_coord),items))
        if nameimg not in rect_coord.keys():
            AnnotList.insert(tk.END,nameimg)
            rect_coord['{}'.format(nameimg)]=coord
        else:
            pass

    else:
        pass

# Function to Clear annotations for the selected image
def clearannot():
    global tags,rect_coord
    try:
        DisplayCanvas.delete('recs')
        index1 = AnnotList.get(0, "end").index(tags[0])
        AnnotList.delete(index1,index1)
        rect_coord.pop('{}'.format(nameimg))
    except:
        pass
    ImageCount.configure(text="{}/{}".format(len(rect_coord),items))

# Load images from the selected directory 
def listImages():
    global images,imageNames,rect_coord,coord,items,annimage,imgname,button_dc,imagesrsz,ImageCanvas

    annimage=0
    relx=60
    
    try:
        path = askdirectory(initialdir='.')
        images,imagesrsz,coord=[],[],[]
        button_dc,imageNames,rect_coord={},{},{}
        DisplayCanvas.delete('all')
        ImageCanvas.delete('all')
        items=0
        AnnotList.delete(0,tk.END)
        AnnotList.insert(tk.END,' ')
        for img in  os.listdir(path):
            if '.jpg' in img:
                imagesOrg = uimages.getimg(path+'/'+img)
                imgname=img
                images.append(imagesOrg)
                imgrsz = uimages.resizeOpenedImage(path+'/'+img,100,100)
                imagesrsz.append(imgrsz)
                button_dc[img]=ImageCanvas.create_image(relx,100,image=imgrsz,anchor=tk.CENTER,tags=imgname+" "+str(items))
                relx+=110
                items+=1
        ImageCount.configure(text="{}/{}".format(annimage,items))
        ImageCanvas.configure(scrollregion=ImageCanvas.bbox('all'))
    except:
        showwarning(title='Warning',message='Please Select a Valid File Path\n'+
        'No Image Found in Selected Directory or Directory Not Selected')

# Get the export path
def getpath():
    pathexp=askdirectory()
    FilExport.insert(0,pathexp)

# Handle image selection click
def onClick(event):
    global tags
    try:
        tags=ImageCanvas.gettags('current')
        displayImage(int(tags[1]),tags[0])
        ImageCanvas.delete('selection')
        ImageCanvas.create_rectangle(5+(int(tags[1])*110),45,115+(int(tags[1])*110),155,outline='silver',tags='selection',width=2)
    except:
        pass

# Start drawing a rectangle on button press
def on_button_press(event):
    global start_x,start_y,rect
    start_x = DisplayCanvas.canvasx(event.x)
    start_y = DisplayCanvas.canvasy(event.y)
    rect = DisplayCanvas.create_rectangle(x, y, x, y, outline='red',tags='recs')

# Update rectangle size while dragging
def on_move_press(event):
    global curX,curY
    
    curX = DisplayCanvas.canvasx(event.x)
    curY = DisplayCanvas.canvasx(event.y)

    # Check if the user dragged out of the canvas borde for x axis
    if curX>512:
        curX = 512
    elif curX < 0:
        curX = 0
        
    # Check if the user dragged out of the canvas borde for y axis
    if curY>512:
        curY = 512
    elif curY < 0:
        curY = 0

    DisplayCanvas.coords(rect, start_x, start_y, curX, curY)

# Finalize rectangle drawing on button release
def on_button_relase(event):           
    global curX,curY,start_x,start_y
    
    # These conditions are for chechking if user started from right to left or top the bottom and fix the coordinates accordingly.
    if int(curX) < int(start_x):
        curX,start_x = start_x,curX
    else:
        pass
    
    if int(curY) < int(start_y):
        curY, start_y = start_y,curY
    else:
        pass
    if int(curX) == int (start_x) or int(curY) == int(start_y):
        showwarning('Warnig','Please select a valid area')
    else:
        coord.append([int(start_x), int(start_y), int(curX), int(curY)])

# Export annotations to selected path
def exportAs():
    toBeExported = []
    if var.get() == 1:
        if FilExport.get():
            for element in rect_coord.keys():
                strAnnot = f'{element} '
                for coords in rect_coord[element]:
                    strAnnot = strAnnot + f'{((coords[2]-coords[0])/2)/512} {((coords[3]-coords[1])/2)/512} {(coords[2]-coords[0])/512} {(coords[3]-coords[1])/512} '
                toBeExported.append(strAnnot[0:len(strAnnot)-1]+'\n')
                try:
                    with open(f'{FilExport.get()}/annot.txt','w',encoding='utf-8') as f:
                        f.writelines(toBeExported)
                except:
                    showwarning('Warning',f'No such file or directory: {FilExport.get()}')
        else:
            showwarning('Warning','Please select a valid path')

# Buttons for image loading, annotation saving, and clearing
btn=ctk.CTkButton(root,text='Open Image Folder',command=listImages)
btn.place(relx=0.45,rely=0.30,relwidth=0.1)

btnsaveann=ctk.CTkButton(root,text='Save Annotations',command=saveannot)
btnsaveann.place(relx=0.45,rely=0.35,relwidth=0.1)

btnclear=ctk.CTkButton(root,text='Delete Annotations',command=clearannot)
btnclear.place(relx=0.45,rely=0.4,relwidth=0.1)

# Path selection and export buttons
btnico=uimages.resizeOpenedImage('uimages/pathico.png',30,30)
BtnExportpath=ctk.CTkButton(ExportOpt,image=btnico,text='',command=getpath,fg_color='gray20',hover_color='gray20')
BtnExportpath.place(relx=0.925,rely=0.0756,relwidth=0.08,relheight=0.08,anchor=tk.CENTER)

BtnExport=ctk.CTkButton(ExportOpt,text='Export',command=exportAs)
BtnExport.place(relx=0.5,rely=0.9,anchor=tk.CENTER)

# Set up event bindings
ImageCanvas.bind('<Button-1>',onClick)
DisplayCanvas.bind('<ButtonPress-1>',on_button_press)
DisplayCanvas.bind('<B1-Motion>',on_move_press)
DisplayCanvas.bind('<ButtonRelease-1>',on_button_relase)

root.mainloop()