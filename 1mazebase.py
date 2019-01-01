from PIL import Image, ImageColor, ImageDraw
from checkentry import checkEntry
#from mazefunctions import checkFile, getValues, pathFind, rightPathDiverge, leftPathDiverge, downPathDiverge, upPathDiverge
import sys


###Setup
#print(ImageColor.getcolor('red', 'RGBA'))
#basefilename = input('Enter Maze File Name (no extension/suffix): ')
#filename = basefilename + '.png'
filename = 'maze1 backup sharpen.png'
maze = Image.open(filename)
maze = maze.convert('P') # conversion to RGB
#maze = maze.load()
#maze.save(basefilename + 'solvedbw.png', 'PNG')

draw = ImageDraw.Draw(maze)
pix = maze.load()
#print("Maze size: ", maze.size)

width, height = maze.size
#print("Maze width: ", width)
#print("Maze height: ", height)

#maze = ImageEnhance.Brightness(maze).enhance(50.0)


print("\n-------------STARTING MAZE SOLVER-------------")
###----------------------------------------
print("                 ...........                 \n")

#mazecolor = Image.new('RGB', (100, 100))


###Global vars
whitecount = 0
temp = 0
maxwidth = int(height/5)
minwidth = 1
fullline = 0


###Get startpnt, pathwidth
#Right = 0, Up = 1

checkEntry(filename)

whitecount = checkEntry(filename)[0]
startDir = checkEntry(filename)[1]
temp = checkEntry(filename)[2]

startpnt = temp - (whitecount/2)
pathwidth = (whitecount)
halfspace = (whitecount/2)

if (halfspace % 2) is not 0:
    halfspace = halfspace-0.5
if (startpnt % 2) is not 0:
    startpnt = startpnt+0.5
divpoints = [[]]

#getValues(whitecount,halfspace)


#print("halfspace: ", halfspace, "whitecount: ",whitecount, "temp: ",temp, "startpnt: ",startpnt, "startDir: ",startDir)
#print(maze.getpixel((0, startpnt)))
#print(maxwidth)
###----------------------------------------


###Direction Functions
def drawRight(x,y):
    fullline = 0
    for i in range(width):
        #print("got here 1--------", startpnt)
        if (i+x) <= (width-1):
            r = maze.getpixel((i+x,y))
        else:
            r = 0
        if (r > 0) and (i + x <= (width - 1)):
            fullline = i
            #print("got here 2--------")
        else:
            #print("got here 3--------")
            if (i + x > (width - 1)):
                #print("got here 4--------", fullline)
                draw.line((x, y) + (width-1,y),fill=10)
                return (width-1, y)
                break
            else:
                #print("got here 5--------")
                draw.line((x, y) + (x+(fullline - halfspace),y),fill=10)
                return (x+(fullline - halfspace),y)
                break
def drawLeft(x,y):
    fullline = 0
    for i in range(width):
        if (x - i >= 1):
            r = maze.getpixel((x-i,y))
        else:
            r = 0
        if (r > 0) and (x - i >= 1):
            fullline = i
        else:
            if (x - i < 1):
                draw.line((x, y) + (0,y),fill=10)
                return (0, y)
                break
            else:
                draw.line((x, y) + (x-(fullline - halfspace),y),fill=10)
                return (x-(fullline - halfspace),y)
                break

def drawDown(x,y):
    fullline = 0
    #print("drawDown")
    for i in range(width):
        if (i + y <= height - 1):
            r = maze.getpixel((x,i+y))
        else:
            r = 0
        #print("enter loop", x, i+y)
        if (r > 0) and (i + y <= height - 1):
            fullline = i
        else:
            if (y + i > height - 1):
                #print('WRONG')
                #print (x,y+i)
                draw.line((x, y) + (x,height-1),fill=10)
                return (x,height-1)
                break
            else:
                #print('RIGHT')
                draw.line((x, y) + (x,y+(fullline - halfspace)),fill=10)
                #print('coor, right:',x,y+(fullline - halfspace))
                return (x,y+(fullline - halfspace))
                break
    
def drawUp(x,y):
    fullline = 0
    for i in range(width):
        if (y - i >= 1):
            r = maze.getpixel((x,y-i))
        else:
            r = 0
        if (r > 0) and (y - i >= 1):
            fullline = i
            #print ("x,y-i : ", x,y-i)
        else:
            if(y - i < 1):
                #print ("BROKE BOUNDARY, x,y-i : ", x,y-i)
                draw.line((x, y) + (x,0),fill=10)
                return (x,0)
                break
            else:
                #print("not broken?")
                draw.line((x, y) + (x,y-(fullline - halfspace)),fill=10)
                return (x,y-(fullline - halfspace))
                break

###Check Functions
    #Down/Right = False
def checkVert(x,y):
    z = 0
    for i in range(3):
        r = maze.getpixel((x,y-(int(halfspace) + i)))
        if (r == 0):
            z = 1
    if (z == 0):
        #print (r, "Turn Up, coordinates:",x,y)
        return True
        #return ("Turn Up")
    else:
        z = 0
        for i in range(3):
            r = maze.getpixel((x,y+(int(halfspace) + i)))
            if (r == 0):
                z = 1
        if (z == 0):
            #print (r, "Turn Down, coordinates:",x,y)
            return False
            #return ("Turn Down")
        else:
            print('dead end',z)
            return ('Dead end')

def checkHor(x,y):
    #print ("GOOD SO FAR", x,y)
    #print(int(halfspace))
    #print("x,y original:",x,y)
    #print((x-(int(halfspace) + 3)))
    z = 0
    for i in range(3):
        r = maze.getpixel((x-(int(halfspace) + i),y))
        #print('x,y:',((x-(int(halfspace) + i),y)),"r:",r)
        if (r == 0):
            z = 1
            #print("R:", r)
    #print ("GOOD SO FAR")
    if (z == 0):
        #print (r, "Turn Left, coordinates:",x,y)
        #print("\n------\n")
        return True
        #return ("Turn Left")
    else:
        for i in range(3):
            r = maze.getpixel((x+(int(halfspace) + i),y))
            if (r == 0):
                z = 2
        if (z == 1):
            #print (r, "Turn Right, coordinates:",x,y)
            return False
            #return ("Turn Right")
        else:
            return ('Dead end')


def rightSequence(x,y):
    drawRight(x,y)
    print("RIGHT BEFORE TRUETURETUEREURUERUEURUEURERUEURUERUEUUER", x, y,drawRight(x, y)[0])
    
    if (rightDivergeDown(x,y,drawRight(x, y)[0])) == True:
        print ("rightSequence if rDD is True, x,y:",x,y)
        return 5
    elif (rightDivergeUp(x,y,drawRight(x, y)[0])) == True:
        print("rightSequence if rDD is False, else, x,y:",x,y)
        return 5
        #print("ok")
    #rightDiverge(x,y,drawRight(x, y)[0])
    #rightDivergeDown(x,y,drawRight(x, y)[0])
    #print("rightSequence Loop")
    #rightDivergeUp(x,y,drawRight(x, y)[0])
    #divpoints.append(rightDivergeDown(x,y,drawRight(x, y)[0]))
    #rightDiverge(x,y,drawRight(x, y)[0])
    x,y = drawRight(x, y)
    #print("->entered right seq")
    if checkVert(x,y) == False:
        nextDir = 3
        return nextDir
    elif checkVert(x,y) == True:
        nextDir = 2
        return nextDir
    else:
        print("checkVert:",checkVert(x,y))
        nextDir = 4
        return nextDir

def leftSequence(x,y):
    drawLeft(x,y)

    #leftPathDiverge(x,y,drawLeft(x,y)[0])
    #leftDivergeUp(x,y,drawLeft(x,y)[0])
    #leftDivergeDown(x,y,drawLeft(x,y)[0])
    x,y = drawLeft(x, y)

    if checkVert(x,y) == False:
        #print ("nextDir = Down")
        nextDir = 3
        return nextDir
    elif checkVert(x,y) == True:
        #print ("nextDir = Up")
        nextDir = 2
        return nextDir
    else:
        nextDir = 4
        return nextDir
def downSequence(x,y):
    #print('x,y downSeq',x,y)
    drawDown(x,y)
    #downDivergeLeft(x,y,drawDown(x,y)[1])
    #downDivergeRight(x,y,drawDown(x,y)[1])
    x,y = drawDown(x, y)
    #print('x,y afterdownSeq',x,y)
    #print ("HEREREREREREERE", x,y)
    if checkHor(x,y) == False:
        #print ("nextDir = Right")
        nextDir = 0
        return nextDir
    elif checkHor(x,y) == True:
        #print ("nextDir = Left")
        nextDir = 1
        return nextDir
    else:
        nextDir = 4
        return nextDir
def upSequence(x,y):
    drawUp(x,y)
    #upDivergeLeft(x,y,drawUp(x,y)[1])
    #upDivergeRight(x,y,drawUp(x,y)[1])
    x,y = drawUp(x, y)
    #print ("HEREREREREREERE", x,y)
    if checkHor(x,y) == False:
        print ("nextDir = Right")
        nextDir = 0
        return nextDir
    elif checkHor(x,y) == True:
        print ("nextDir = Left")
        nextDir = 1
        return nextDir
    else:
        print("dead end")
        nextDir = 4
        return nextDir

def pathFind(x,y,nextDir):

    #Right = 0, Left = 1, Up = 2, Down = 3
    #DrawRight = 0, DrawLeft = 1, DrawUp = 2, DrawDown = 3
    origx = x
    origy = y
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
            print("------------------->TURN RIGHT<-------------------")
            currentDir = nextDir
            nextDir = rightSequence(x,y)
            print("got here",x, y)
            #rightDiverge(x,y,drawRight(x, y)[0])
            x,y = drawRight(x, y)
            print("got here1", x, y)
            #print("x: ", x)
            xcheck = x
            print("got here2", nextDir, xcheck)
            if xcheck == 0 or xcheck == (width-1):
                nextDir = 5
                xcheck = 1
                print ('xcheck', xcheck,nextDir)
        elif nextDir == 1:
            print("------------------->TURN LEFT<-------------------")
            currentDir = nextDir
            leftSequence(x,y)
            nextDir = leftSequence(x,y)
            print ("mid full left seq",x,y)
            x,y = drawLeft(x, y)
            xcheck = x
            if xcheck == 0 or xcheck == (width-1):
                #nextDir = 5
                xcheck = 1
                print ('xcheck', xcheck,nextDir, x, y)
            #print ("nextDir: ", nextDir)
        elif nextDir == 2:
            print("------------------->TURN UP<-------------------")
            currentDir = nextDir
            upSequence(x,y)
            nextDir = upSequence(x,y)
            x,y = drawUp(x, y)
            ycheck = y
            if ycheck == 0 or ycheck == (height-1):
                #nextDir = 5
                ycheck = 1
                print ('ycheck', ycheck,nextDir)
            #print ("coordinates: ", x,y)
            #print ("nextDir: ", nextDir)
            #print(x, y, xcheck,"ycheck: ",ycheck)
        elif nextDir == 3:
            print("------------------->TURN DOWN<-------------------")
            currentDir = nextDir
            nextDir = downSequence(x,y)
            x,y = drawDown(x, y)
            ycheck = y
            if ycheck == 0 or ycheck == (height-1):
                #nextDir = 5
                ycheck = 1
                print ('ycheck', ycheck,nextDir)
            #print ("y",y)
            #print ("coordinates: ", x,y)
            #print ("nextDir: ", nextDir)
        elif nextDir == 4:
            print("dead end")
            break
        elif nextDir == 5:
            print ("PATHWAY FOUND")
            return True
            break
        else:
            print ("Error: ", nextDir)
            #print (xcheck, ycheck)
            #print ("startDir: ", startDir)
    if nextDir == 4:
        print('final',origx,origy,x,y)
        return False,currentDir,origx,origy,x,y
    else:
        return True

###Check entry point
x = checkEntry(filename)[3] 
y = checkEntry(filename)[4]

"""
#print ("startDir: ", startDir)
if startDir == 0:
    #print("X,Y" , x,y)
    leftSequence(x,y)
    #print("X,Y" , x,y)
    nextDir = leftSequence(x,y)
    x,y = drawLeft(x, y)

elif startDir == 1:
    rightSequence(x,y)
    nextDir = rightSequence(x,y)
    x,y = drawRight(x, y)
elif startDir == 2:
    #print("X,Y" , x,y)
    downSequence(x,y)
    nextDir = downSequence(x,y)
    x,y = drawDown(x, y)
    #print ("nextDir: ", nextDir)
elif startDir == 3:
    upSequence(x,y)
    nextDir = leftUp(x,y)
    x,y = drawUp(x, y)

pathFind(x,y,nextDir)

maze.save(basefilename + 'solved.png', 'PNG')
"""

##################################

def leftDivergeUp(x,y,newx):
    width = 0
    distance = x - newx
    i = 1
    divpoint = 0
    listdivs = []
    print("LdU",distance)
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
def leftDivergeDown(x,y,newx):
    width = 0
    distance = x - newx
    i = 1
    divpoint = 0
    listdivs = []
    print("LdD",distance)
    if (maze.getpixel((x-1,y + halfspace + 2)) > 0):
        distance -= halfspace
        x -= halfspace
    print("i",i)
    while((distance - i + 1) > 0):
    #for i in range(distance):
        r = maze.getpixel((x - i,y + halfspace + 2))
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
        pathFind(listdivs[i],y,3)
        print('listdiv[i]:',listdivs[i])

        
def rightDivergeUp(x,y,newx):
    width = 0
    distance = newx - x
    i = 1
    divpoint = 0
    listdivs = []
    print("RdU",distance)
    if (maze.getpixel((x+1,y - halfspace - 2)) > 0):
        distance -= halfspace
        x -= halfspace
        print("halfspace-----", distance,x,halfspace)
    print("i",i)
    #Gives a list of points of diversion
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
    #listdivs.append(2)
    #return listdivs
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False
    """
    print(listdivs)
    if len(listdivs) > 0:
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],y,2)) == True:
                return True
            #print('listdiv[i]:',listdivs[i])
    """
def rightDivergeDown(x,y,newx):
    width = 0
    distance = newx - x
    i = 1
    divpoint = 0
    listdivs = []
    print("RdD",distance)
    if (maze.getpixel((x+1,y + halfspace + 2)) > 0):
        distance -= halfspace
        x -= halfspace
        print("halfspace-----", distance,x,halfspace)
    print("i",i)
    #Gives a list of points of diversion
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x + i,y + halfspace + 2))
        if r > 0:
            print("diverge,", "i:",i, i+pathwidth, x)
            divpoint = x + i - 1 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
            print('divpoint',divpoint)
            print(x + i)
        i += 1
        
    if len(listdivs) > 0:
        return True, listdivs

    """    
    print("listdivs, lengthlist",listdivs, len(listdivs), x, y)
    if len(listdivs) > 0:
        for i in range(len(listdivs)):
            print ("got here, rightDivDown within end for loop",listdivs[i], y)
            if (pathFind(listdivs[i],y,3)) == True:
                print("TRUEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",listdivs[i],y)
                return True
            print('listdiv[i]:',listdivs[i])
    """
    #print("PAST LIST")
    #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", divpoints)
    #if len(listdivs) is not 0:        
        #listdivs.append('down')
    #return listdivs
    

def downDivergeLeft(x,y,newy):
    width = 0
    distance = newy - y
    i = 1
    divpoint = 0
    listdivs = []
    print("DdL",distance)
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

def downDivergeRight(x,y,newy):
    width = 0
    distance = newy - y
    i = 1
    divpoint = 0
    listdivs = []
    print("DdR",distance)
    if (maze.getpixel((x + halfspace + 2,y + i)) > 0):
        distance -= halfspace
        y -= halfspace
        print("halfspace-----", distance,y,halfspace)
    print("i",i)
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x + halfspace + 2,y + i))
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
        pathFind(x,listdivs[i],0)
        print('listdiv[i]:',listdivs[i])


def upDivergeLeft(x,y,newy):
    width = 0
    distance = y - newy
    i = 1
    divpoint = 0
    listdivs = []
    print("UdL",distance)
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
def upDivergeRight(x,y,newy):
    width = 0
    distance = y - newy
    i = 1
    divpoint = 0
    listdivs = []
    print("UdR",distance)
    if (maze.getpixel((x + halfspace + 2,y - i)) > 0):
        distance += halfspace
        y += halfspace
        print("halfspace-----", distance,y,halfspace)
    print("i",i)
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x + halfspace + 2,y - i))
        if r > 0:
            print("diverge,", "i:",i, i+pathwidth, y)
            divpoint = y - i - 1 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
            print('divpoint',divpoint)
            print(y - i)
        i += 1
    #return listdivs
    """
    print(listdivs)
    for i in range(len(listdivs)):
        pathFind(x,listdivs[i],0)
        print('listdiv[i]:',listdivs[i])
    """
def rightDiverge(x,y,newx):
    width = 0
    distance = newx - x
    savedistance = distance
    i = 1
    divpoint = 0
    listdivs = []
    print("RdU",distance)
    if (maze.getpixel((x+1,y + halfspace + 2)) > 0):
        distance -= halfspace
        x -= halfspace
        print("halfspace-----", distance,x,halfspace)
    print("i",i)
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x + i,y + halfspace + 2))
        if r > 0:
            print("diverge,", "i:",i, i+pathwidth, x)
            divpoint = x + i - 1 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
            print('divpoint',divpoint)
            print(x + i)
        i += 1
    if len(listdivs) > 0:
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],y,3)) == True:
                return True
            print('listdiv[i]:',listdivs[i])

    #####
    width = 0
    distance = savedistance
    i = 1
    divpoint = 0
    listdivs = []
    print("RdD",distance)

    """
    print("listdivs, lengthlist",listdivs, len(listdivs))
    if len(listdivs) > 0:
        for i in range(len(listdivs)):
            pathFind(listdivs[i],y,3)
            print('listdiv[i]:',listdivs[i])
    """
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
    if len(listdivs) > 0:
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],y,2)) == True:
                return True
    """
    print(listdivs)
    for i in range(len(listdivs)):
        pathFind(listdivs[i],y,2)
        print('listdiv[i]:',listdivs[i])
    """
#x = 150
#y = 109
#newx = 126
#leftPathDiverge(x,y,newx)
#rightPathDiverge(x,y,newx)
#pathFind(1,109,0)
#downPathDiverge(x,y,newy)
#upPathDiverge(x,y,newy)
#upDivergeRight(x,y,newy)
#downDivergeRight(x,y,newy)
#rightDivergeDown(1,109,69)
#leftDivergeDown(x,y,newx)

#CHECK 218 FOR ALL

##################################

###Instructions


def manualFind(x,y,nextDir):

    if nextDir == 0:
        rightSequence(x,y)
        nextDir = rightSequence(x,y)
        x,y = drawRight(x, y)
    elif nextDir == 1:
        leftSequence(x,y)
        nextDir = leftSequence(x,y)
        x,y = drawLeft(x, y)
    elif nextDir == 2:
        upSequence(x,y)
        nextDir = upSequence(x,y)
        x,y = drawUp(x, y)
    elif nextDir == 3:
        downSequence(x,y)
        nextDir = downSequence(x,y)
        x,y = drawDown(x, y)

    upSequence(x,y)
    x,y = drawUp(x, y)
    print("checking hor from down: ", x,y)
    print(checkHor(x,y))
    leftSequence(x,y)
    x,y = drawLeft(x, y)
    print("checking vert from left: ", x,y)
    print(checkVert(x,y))
    upSequence(x,y)
    x,y = drawUp(x, y)
    print("checking hor from down: ", x,y)
    print(checkHor(x,y))
    rightSequence(x,y)
    x,y = drawRight(x, y)
    print("checking vert from right: ", x,y)
    print(checkVert(x,y))
    downSequence(x,y)
    #nextDir, x, y = upSequence(x,y)
    x,y = drawDown(x, y)

"""
if (pathFind(1,109,0)) == True:
    print("Found pathway!")
else:
    print("Dead End Confirmed.")
    x = pathFind(1,109,0)[2]
    y = pathFind(1,109,0)[3]
    newx = pathFind(1,109,0)[4]
    print (x,y,newx)
"""
pathFind(1,109,0)
#print(rightDivergeDown(1,109,69),"---------------------------------------------")
#print("---------------------------------------------",pathFind(27,109,3))
#print("final coordinates",x,y)
#rightDiverge(1,109,69)

"""

def mainFunction(1,109,0):
    if pathFind(1,109,0) == True:
        return functionComplete
    elif pathFind(1,109,0) == False:
        if any checkDivs:
            mainFunction(Div1)
        else:
            return False
                
        pathFind(1,109,0)
            rightSequence
                if checkDivergeUp == True:
                    pathFind(new):
                        pathway found
                elif checkDivergeDown == True:
                    pathway found
                
def mainFunction(1,109,0):
    while(pathFind(1,109,0) is not False):
        return functionComplete

    if pathFind(1,109,0) == False:
        checkDivergePoints == True:
            pathFind(newPoints)
        
    else:
        pathFind(1,109,0)
            rightSequence
                if checkDivergeUp == True:
                    pathFind(new):
                        pathway found
                elif checkDivergeDown == True:
                    pathway found

def checkIfFalse(1,109,0):
    if checkDiv(x,y,Dir)== True:
        pathFind
        checkIfFalse(newPoint)
    else:
        return (1,109,0)
    

keep checking for divpoints/dead ends until you cant find anymore
    when you run into 0 divpoints/dead end, return previous start point and start from there

print("----------------------------------------------------------")
print (divpoints)
for lists in range(len(divpoints)):
    if (len(divpoints[lists])) == 0:
        continue
    else:
        for element in range(len(divpoints[lists])):
            print(divpoints[lists][element])




drawRight(0, startpnt)
x,y = drawRight(0, startpnt)
#x = int(x)
#y = int(y)
print("checking vert from right: ", x,y)
print(checkVert(x,y))
"""
##################################
maze.save('maze1 backup sharpen fill.png', 'PNG')

print("-----------------MAZE SOLVED------------------")

