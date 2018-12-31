from PIL import Image, ImageColor, ImageDraw
#from mazebase import pathFind
#from checkentry import checkEntry
import sys


def checkFile(filename):
    return filename
    print('FILENAME',filename)

#filename = checkFile(filename)

filename = 'line.png'

maze = Image.open(filename)
maze = maze.convert('P')
width, height = maze.size
draw = ImageDraw.Draw(maze)

def getValues(whitecount,halfspace):
    return whitecount, halfspace

#whitecount, halfspace = getValues(whitecount,halfspace)
whitecount, halfspace, pathwidth = 19,9,19

#draw.line((1, 20) + (100,217),fill=10)
#print("gotem")

def pathFind(x,y,nextDir):

    #Right = 0, Left = 1, Up = 2, Down = 3
    #DrawRight = 0, DrawLeft = 1, DrawUp = 2, DrawDown = 3
    xcheck = 1
    ycheck = 1
    ###Main loop
    while (xcheck is not 0) and (xcheck is not (width-1)) and (ycheck is not 0) and (ycheck is not (height-1)):
    #for i in range(38):
        #if not ((xcheck < width or xcheck >= 1)):
        #    print ("BROKEN")
        #if not ((ycheck >= 1)):
        #    print ("BROKEN")
        #print("range new------")
        if nextDir == 0:
            rightSequence(x,y)
            nextDir = rightSequence(x,y)
            x,y = drawRight(x, y)
            #print ("coordinates: ", x,y)
            
            #print("x: ", x)
            xcheck = x
        elif nextDir == 1:
            leftSequence(x,y)
            nextDir = leftSequence(x,y)
            x,y = drawLeft(x, y)
            xcheck = x
            #print ("coordinates: ", x,y)
            #print ("nextDir: ", nextDir)
        elif nextDir == 2:
            upSequence(x,y)
            nextDir = upSequence(x,y)
            x,y = drawUp(x, y)
            ycheck = y
            #print ("coordinates: ", x,y)
            #print ("nextDir: ", nextDir)
            #print(x, y, xcheck,"ycheck: ",ycheck)
        elif nextDir == 3:
            nextDir = downSequence(x,y)
            x,y = drawDown(x, y)
            ycheck = y
            #print ("y",y)
            #print ("coordinates: ", x,y)
            #print ("nextDir: ", nextDir)
        else:
            print ("Error")
            #print (xcheck, ycheck)
            #print ("startDir: ", startDir)

def leftPathDiverge(x,y,newx):
    width = 0
    distance = x - newx
    i = 1
    divpoint = 0
    listdivs = []
    print(distance)
    if (maze.getpixel((x-1,y - halfspace - 2)) > 0):
        distance -= halfspace
        x -= halfspace
    print("i",i)
    while((distance - i + 1) > 0):
    #for i in range(distance):
        r = maze.getpixel((x - i,y - halfspace - 2))
        if r > 0:
            print("diverge,", "i:",i, i+pathwidth, x)
            divpoint = x - i + 1 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
            print('divpoint',divpoint)
            print(x - i)
        i += 1
    print(listdivs)
    for i in range(len(listdivs)):
        pathFind(listdivs[i],y,2)
        print('listdiv[i]:',listdivs[i])

def rightPathDiverge(x,y,newx):
    width = 0
    distance = newx - x
    i = 1
    divpoint = 0
    listdivs = []
    print(distance)
    if (maze.getpixel((x+1,y - halfspace - 2)) > 0):
        distance -= halfspace
        x -= halfspace
        print("halfspace-----", distance,x,halfspace)
    print("i",i)
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x + i,y - halfspace - 2))
        if r > 0:
            print("diverge,", "i:",i, i+pathwidth, x)
            divpoint = x + i - 1 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
            print('divpoint',divpoint)
            print(x + i)
        i += 1
    print(listdivs)
    for i in range(len(listdivs)):
        pathFind(listdivs[i],y,2)
        print('listdiv[i]:',listdivs[i])
def downPathDiverge(x,y,newy):
    width = 0
    distance = newy - y
    i = 1
    divpoint = 0
    listdivs = []
    print(distance)
    if (maze.getpixel((x - halfspace - 2,y + i)) > 0):
        distance -= halfspace
        y -= halfspace
        print("halfspace-----", distance,y,halfspace)
    print("i",i)
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x - halfspace - 2,y + i))
        if r > 0:
            print("diverge,", "i:",i, i+pathwidth, y)
            divpoint = y + i - 1 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
            print('divpoint',divpoint)
            print(y + i)
        i += 1
    print(listdivs)
    for i in range(len(listdivs)):
        pathFind(x,listdivs[i],1)
        print('listdiv[i]:',listdivs[i])
def upPathDiverge(x,y,newy):
    width = 0
    distance = y - newy
    i = 1
    divpoint = 0
    listdivs = []
    print(distance)
    if (maze.getpixel((x - halfspace - 2,y - i)) > 0):
        distance -= halfspace
        y -= halfspace
        print("halfspace-----", distance,y,halfspace)
    print("i",i)
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x - halfspace - 2,y - i))
        if r > 0:
            print("diverge,", "i:",i, i+pathwidth, y)
            divpoint = y - i - 1 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
            print('divpoint',divpoint)
            print(y - i)
        i += 1
    print(listdivs)
    for i in range(len(listdivs)):
        pathFind(x,listdivs[i],1)
        print('listdiv[i]:',listdivs[i])

maze.save('linemazefunctioncheck.png', 'PNG')
