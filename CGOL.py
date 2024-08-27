from PIL import Image, ImageDraw 
import numpy as np
import random
#Example Stats: Width:50, Height:60, Sizeinc: 15, Frames:120, Weight: 0.5, Seed: Sometext
images = [] 
def forceint(string):
    while True:
        try: 
            temp = int(input(string))
        except:
            print("Oops, that's gotta be an integer (1, 43, 576 etc), Please try again")
        else:
            break
    while temp < 5:
        print("Gotta give a bigger number than that :)")
        temp = forceint(string)
    return int(temp)
def forcedec(string):
    while True:
        try: 
            temp = float(input(string))
        except:
            print("Oops, that's gotta be decimal (.1, .4, .7 etc), Please try again")
        else:
            break
    while temp >= 1 or temp <= 0:
        print("Please give a decimal value between 0 and 1!")
        temp = forcedec(string)
    return float(temp)
width = forceint("Width: ")
height = forceint("Height: ")
sizeinc = int(1000/max(width, height))
frames = forceint("Frame Number: ")
weight = forcedec("Initial Density: ")
seed = input("Seed: ")
oldboard = np.zeros((height, width))
newboard = oldboard
def iter2D(f, ymax, xmax):
    for y in range(0, ymax):
        for x in range(0, xmax):
            f(y, x)
def setactive(basearr, startpoint, amount):
    for y in range(0, amount[0], 1):
        for x in range(0, amount[1], 1):
           basearr[startpoint[0]+y, startpoint[1]+x] = 255
def setactivelist(basearr, startpoint, pointlist):
    for y in range(0, len(pointlist)):
        for x in range(0, len(pointlist[y])):
            if pointlist[y][x] !=0:
                basearr[y+startpoint[0], x+startpoint[1]]=255
def setframe(old):
    new =  np.zeros((height, width))
    for y in range(0, height, 1): 
        for x in range(0, width, 1):
            neighbors = 0
            for yn in [0, 1, 2]:
                for xn in [0, 1, 2]:
                    if(yn==1 and xn==1):
                        continue
                    pointy = y+yn-1
                    pointx = x+xn-1
                    if(pointy<0):
                        pointy=height-1
                    elif(pointy>=height):
                        pointy=0
                    if(pointx<0):
                        pointx=width-1
                    elif(pointx>=width):
                        pointx=0
                    if(old[pointy, pointx]>1):
                        neighbors=neighbors+1
            if(neighbors == 2):
                new[y, x] = old[y, x]
            elif(neighbors ==3):
                new[y, x] = 255 if old[y, x]<1 else old[y, x]
            else:
                new[y, x] = 0 
            if(old[y, x]==new[y,x] and new[y, x]>1):
                new[y, x]=max(int(new[y, x]*0.85), 64)
    return new
def upscale(old, mult):
    temp = np.zeros((height*mult, width*mult))
    def inner(y, x):
        def inner2(yn, xn): temp[y*mult+yn, x*mult+xn]=old[y, x]
        iter2D(inner2, mult, mult)
    iter2D(inner, height, width)
    return temp
def addframe(obj):
    images.append(Image.fromarray(upscale(obj, sizeinc)))
numseed=0
for i in range(0, len(seed)):
    numseed+=ord(seed[i])*3**i
random.seed(numseed)
def randCell(rany, ranx):
    oldboard[rany, ranx] = 255 if random.random()<weight else 0
for y in range(0, height):
    for x in range(0, width):
        randCell(y, x)
addframe(oldboard)
for i in range(0, frames-1, 1):   
    oldboard = setframe(oldboard)
    addframe(oldboard)
images[0].save('Game Of Life Simulation.gif', 
               save_all = True, append_images = images[1:],  
               optimize = False,compress_level=9, duration = 10, loop = 0)
print("{"+str(width)+"x"+str(height)+", "+str(frames)+", "+str(weight)+", \""+seed+"\"}")