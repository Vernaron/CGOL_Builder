from PIL import Image, ImageDraw 
import numpy as np
import random
from collections import deque
from math import floor
#Example Stats: Width:50, Height:60, Sizeinc: 15, Frames:120, Weight: 0.5, Seed: Sometext
class dimensions:
    height = 0
    width = 0
    sizeinc = 0
conway_dict = np.array([
0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,1,1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,1,1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,])
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
def recheck_neighbors(recheck_queue, y, x, dims):
    for yn, xn in [(-1, -1),(-1,0),(-1,1),(0, -1),(0,0),(0, 1),(1, -1),(1, 0),(1, 1)]:
            pointy = y+yn
            pointx = x+xn
            if(pointy<0):
                pointy=dims.height-1
            elif(pointy>=dims.height):
                pointy=0
            if(pointx<0):
                pointx=dims.width-1
            elif(pointx>=dims.width):
                pointx=0
            recheck_queue.add((pointy, pointx))
def check_board(y, x,change_queue, dims, recheck_queue, main_board):
    
    neighbors = 0
    for yn, xn in [(-1, -1),(-1,0),(-1,1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1)]:
            pointy = y+yn
            pointx = x+xn
            
            if(pointy<0):
                pointy+=dims.height
            elif(pointy>=dims.height):
                pointy=0
            if(pointx<0):
                pointx+=dims.width
            elif(pointx>=dims.width):
                pointx=0
            if(main_board[pointy][pointx]&1):
                neighbors=neighbors+1

    if(neighbors ==3 and main_board[y][x]==0):
        change_queue.append((y, x, 255))
        recheck_neighbors(recheck_queue, y, x, dims)

    elif((neighbors < 2 or neighbors > 3) and main_board[y][x]>1):
        change_queue.append((y, x, 0))
        recheck_neighbors(recheck_queue, y, x, dims)    

    elif(main_board[y][x]>65):
        change_queue.append((y, x, max(int(main_board[y][x]*0.85)|1, 65)))
        recheck_queue.add((y, x))
    
def change_board(val, main_board):
    main_board[val[0]][val[1]] = val[2]
def setframe(check_set, main_board, change_queue, recheck_queued):
    for n in check_set:
        check_board(n[0],n[1], change_queue, dims, recheck_queue, main_board)
    check_set.clear()
    print('')
    check_set.update(recheck_queue)
    recheck_queue.clear()
    while len(change_queue)!=0:
        change_board(change_queue.pop(), main_board)
    
def upscale(old, dims):
    if dims.sizeinc<1.0:
        return old
    temp = np.zeros((dims.height*dims.sizeinc, dims.width*dims.sizeinc))
    def inner(y, x):
        def inner2(yn, xn): temp[y*dims.sizeinc+yn, x*dims.sizeinc+xn]=old[y, x]
        iter2D(inner2, dims.sizeinc, dims.sizeinc)
    iter2D(inner, dims.height, dims.width)
    return temp
def addframe(obj, index, dims, images):
    images[index]=Image.fromarray(upscale(obj,dims))
def randDummy(rany, ranx, totalPlaced):
    totalPlaced[0]=5
    if(ranx==2 and (rany==0 or rany==1 or rany == 2)):
       main_board[rany][ranx] = 255
    elif(ranx==1 and rany==2):
        main_board[rany][ranx] = 255
    elif(ranx==0 and rany==1):
        main_board[rany][ranx] = 255
    else:
         main_board[rany][ranx] = 0
def randCell(rany, ranx, totalPlaced):
    smallerVal = random.random()
    largerVal = random.random()
    totalNeighbors = 0
    doBias = False
    if smallerVal > largerVal:
        tempVal = smallerVal
        smallerVal = largerVal
        largerVal = tempVal
    if rany>0:
        if main_board[rany-1][ranx] > 100:
            totalNeighbors+=1
        if ranx > 0 and main_board[rany-1][ranx-1] >100:
            totalNeighbors+=1
        if ranx < dims.width-1 and main_board[rany-1][ranx+1] >100:
            totalNeighbors+=1
    if ranx > 0 and main_board[rany][ranx-1] > 100:
         totalNeighbors+=1
    if weight >= 0.4 and totalNeighbors >=1 and totalNeighbors <=2:
        doBias = True
    if weight < 0.4 and totalNeighbors >=1 and totalNeighbors <=3:
        doBias = True
 
    if doBias == True:
        main_board[rany][ranx] = 255 if smallerVal<weight else 0
    else:
         main_board[rany][ranx] = 255 if largerVal<weight else 0
    if  main_board[rany][ranx] ==255:
        totalPlaced[0]+=1

dims = dimensions()
images = [] 
finalFrames = []

totalPlaced = [0]
dims.width = forceint("Width:")
dims.height = forceint("Height:")
dims.sizeinc = max(int(1000/max(dims.width, dims.height)), 1) 
frames = forceint("Frame Number: ")
weight = forcedec("Initial Density: ")
seed = input("Seed: ")
main_board =np.zeros((dims.height,dims.width),dtype=int)
change_queue = deque()
recheck_queue = set({})
check_set = set({})

numseed=0
for i in range(0, len(seed)):
    numseed+=ord(seed[i])*3**i
    
random.seed(numseed)
for y in range(0, dims.height):
    for x in range(0, dims.width):
        randCell(y, x, totalPlaced)
        check_set.add((y, x))
totalPlaced=totalPlaced[0]/(dims.width*dims.height)
print(str(totalPlaced*100)+ "% Filled")
for i in range(0, frames, 1):
    images.append(Image.fromarray(np.zeros((1,1))))

images[0]=Image.fromarray(upscale(main_board, dims))
finalFrames.append((np.reshape(main_board, (dims.width, dims.height), copy=True), 0, dims))
for i in range(1, frames, 1): 
    print('Frame:',i)
    setframe(check_set, main_board, change_queue, recheck_queue)
    print("Processing")
    images[i]=Image.fromarray(upscale(main_board, dims))
print("out here")
print("escaped")
print("Saving...")
images[0].save('Game Of Life Simulation.gif', 
               save_all = True, append_images = images[1:],  
               optimize = True,compress_level=9, duration = 10, fps = 1/10,loop = 0)
               
print("{"+str(dims.width)+"x"+str(dims.height)+", "+str(frames)+", "+str(weight)+", \""+seed+"\"}")