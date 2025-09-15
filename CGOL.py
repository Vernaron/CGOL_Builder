from PIL import Image, ImageDraw 
import numpy as np
import random
from multiprocessing import Process,  Pipe, Array, Value, Pool, Manager
import threading
from math import floor
#Example Stats: Width:50, Height:60, Sizeinc: 15, Frames:120, Weight: 0.5, Seed: Sometext
class dimensions:
    height = 0
    width = 0
    sizeinc = 0
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
    for yn in [0, 1, 2]:
      for xn in [0, 1, 2]:
            if(yn==1 and xn==1):
                 continue
            pointy = y+yn-1
            pointx = x+xn-1
            if(pointy<0):
                pointy=dims.height-1
            elif(pointy>=dims.height):
                pointy=0
            if(pointx<0):
                pointx=dims.width-1
            elif(pointx>=dims.width):
                pointx=0
            recheck_queue.put(convertXY(pointy, pointx, dims))
    recheck_queue.put(convertXY(y, x, dims))
def check_board(check_queue,change_queue, dims, recheck_queue, main_board):
    curr = check_queue.get()
    y=floor(curr/dims.width)
    x=curr%dims.width
    changed = False
    neighbors = 0
    for yn in [0, 1, 2]:
        for xn in [0, 1, 2]:
            if(yn==1 and xn==1):
                continue
            pointy = y+yn-1
            pointx = x+xn-1
            
            if(pointy<0):
                pointy=dims.height-1
            elif(pointy>=dims.height):
                pointy=0
            if(pointx<0):
                pointx=dims.width-1
            elif(pointx>=dims.width):
                pointx=0
            if(getXY(pointy, pointx, dims, main_board)>1):
                neighbors=neighbors+1

    if(neighbors ==3 and getXY(y, x, dims,main_board)==0):
        change_queue.put((convertXY(y, x, dims), 255))
        recheck_neighbors(recheck_queue, y, x, dims)
        changed = True

    elif((neighbors < 2 or neighbors > 3) and getXY(y, x, dims, main_board)>1):
        change_queue.put((convertXY(y, x, dims), 0))
        recheck_neighbors(recheck_queue, y, x, dims)    
        changed = True
    if(getXY(y, x, dims, main_board)>64 and changed==False):
        change_queue.put((convertXY(y, x, dims), max(int(getXY(y, x, dims, main_board)*0.85), 64)))
        recheck_queue.put(convertXY(y, x, dims))
    check_queue.task_done()
    
def change_board(change_queue, main_board):
    val = change_queue
    main_board[val[0]] = val[1]
def setframe(workers, check_set, check_queue, main_board, change_queue, recheck_queued):
    for n in check_set:
        check_queue.put(n)
    #workers.starmap(check_board,(check_queue,change_queue,dims, recheck_queue, main_board))
    while not check_queue.empty():
        check_board(check_queue, change_queue, dims, recheck_queue, main_board)
    check_set.clear()
    print('')
    check_queue.join()
    while(not recheck_queue.empty()):
        if(not recheck_queue.empty()):
            check_set.add(recheck_queue.get())
    while not change_queue.empty():
        change_board(change_queue.get(), main_board)
    
def upscale(old, dims):
    temp = np.zeros((dims.height*dims.sizeinc, dims.width*dims.sizeinc))
    def inner(y, x):
        def inner2(yn, xn): temp[y*dims.sizeinc+yn, x*dims.sizeinc+xn]=old[y, x]
        iter2D(inner2, dims.sizeinc, dims.sizeinc)
    iter2D(inner, dims.height, dims.width)
    return temp
def addframe(obj, index, dims, pipeback):
    pipeback.send((Image.fromarray(upscale(obj,dims)), index))
    pipeback.close()
def getXY(y, x, dims, arr):
    return arr[y*dims.width+x]
def convertXY(y, x, dims):
    return y*dims.width+x    
def setXY(y, x, dims, arr, val):
    arr[y*dims.width+x] = val
def randDummy(rany, ranx, totalPlaced):
    totalPlaced[0]=5
    if(ranx==2 and (rany==0 or rany==1 or rany == 2)):
        setXY(rany,ranx, dims,main_board, 255)
    elif(ranx==1 and rany==2):
        setXY(rany,ranx, dims,main_board, 255)
    elif(ranx==0 and rany==1):
        setXY(rany,ranx, dims,main_board, 255)
    else:
         setXY(rany,ranx, dims,main_board, 0)
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
        if getXY(rany-1,ranx, dims,main_board) > 100:
            totalNeighbors+=1
        if ranx > 0 and getXY(rany-1,ranx-1, dims,main_board) >100:
            totalNeighbors+=1
        if ranx < dims.width-1 and getXY(rany-1,ranx+1, dims,main_board) >100:
            totalNeighbors+=1
    if ranx > 0 and getXY(rany,ranx-1, dims,main_board) > 100:
         totalNeighbors+=1
    if weight >= 0.4 and totalNeighbors >=1 and totalNeighbors <=2:
        doBias = True
    if weight < 0.4 and totalNeighbors >=1 and totalNeighbors <=3:
        doBias = True
 
    if doBias == True:
        setXY(rany,ranx, dims,main_board, 255) if smallerVal<weight else 0
    else:
         setXY(rany,ranx, dims,main_board, 255) if largerVal<weight else 0
    if  getXY(rany,ranx, dims,main_board) ==255:
        totalPlaced[0]+=1
if __name__ == '__main__':
    with Manager() as manager:
        dims = dimensions()
        images = [] 
        finalFrames = []
        processCount = Value('i', 0);
        imagePipes = []
        
        totalPlaced = [0]
        dims.width = forceint("Width:")
        dims.height = forceint("Height:")
        dims.sizeinc = max(int(1000/max(dims.width, dims.height)), 1) 
        frames = forceint("Frame Number: ")
        weight = forcedec("Initial Density: ")
        seed = input("Seed: ")
        main_board = manager.Array('f',np.zeros((dims.height*dims.width)))
        change_queue = manager.Queue()
        check_queue = manager.Queue()
        recheck_queue = manager.Queue()
        check_set = set({})
        workers = Pool()

        numseed=0
        for i in range(0, len(seed)):
            numseed+=ord(seed[i])*3**i
            
        random.seed(numseed)
        for y in range(0, dims.height):
            for x in range(0, dims.width):
                randCell(y, x, totalPlaced)
                check_set.add(convertXY(y, x, dims))
        totalPlaced=totalPlaced[0]/(dims.width*dims.height)
        print(str(totalPlaced*100)+ "% Filled")
        #addframe(oldboard)
        for i in range(0, frames, 1):
            images.append(Image.fromarray(np.zeros((1,1))))
        temprec, tempsend = Pipe()
        imagePipes.append(temprec)
        finalFrames.append((np.reshape(main_board, (dims.width, dims.height), copy=True), 0, dims, tempsend))
        for i in range(1, frames, 1): 
            print('Frame:',i)
            setframe(workers, check_set, check_queue, main_board, change_queue, recheck_queue)
            print("Processing")
            temprec2, tempsend2 = Pipe()
            imagePipes.append(temprec2)
            finalFrames.append((np.reshape(main_board, (dims.width, dims.height), copy=True),i, dims, tempsend2))
        print("out here")
        workers.starmap_async(addframe,finalFrames)
        print("escaped")
        for n in imagePipes:

            result = n.recv()
            images[result[1]] = result[0]
        workers.close()
        workers.join()
        print("Saving...")
        images[0].save('Game Of Life Simulation.gif', 
                       save_all = True, append_images = images[1:],  
                       optimize = False,compress_level=9, duration = 10, fps = 1/10,loop = 0)
                       
        print("{"+str(dims.width)+"x"+str(dims.height)+", "+str(frames)+", "+str(weight)+", \""+seed+"\"}")