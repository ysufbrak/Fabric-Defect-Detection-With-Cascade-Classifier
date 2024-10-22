from PIL import ImageTk,Image

def getimg(path):
    img = Image.open(path)
    img = ImageTk.PhotoImage(img)
    return img

def resizeOpenedImage(path,w,h):
    img=Image.open(path)
    imgTK=ImageTk.PhotoImage(img)
    width=imgTK.width()
    height=imgTK.height()
    if width>height:
        multiplier=width/w
    elif height>width:
        multiplier=height/h
    else:
        multiplier=width/w

    imgResized= img.resize((int(width/multiplier),int(height/multiplier)))

    return ImageTk.PhotoImage(imgResized)