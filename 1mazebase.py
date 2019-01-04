from PIL import Image, ImageColor, ImageDraw
from checkentry import checkEntry
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


print("\n\n-------------STARTING MAZE SOLVER-------------\n")
###----------------------------------------
print("                 ...........                 \n")

#mazecolor = Image.new('RGB', (100, 100))


###Global vars
whitecount = 0
temp = 0
maxwidth = int(height/5)
minwidth = 1
fullline = 0
vertexList = []

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
                draw.line((x, y) + (width-1,y),fill=1)
                return (width-1, y)
                break
            else:
                #print("got here 5--------")
                draw.line((x, y) + (x+(fullline - halfspace),y),fill=1)
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
                draw.line((x, y) + (0,y),fill=1)
                return (0, y)
                break
            else:
                draw.line((x, y) + (x-(fullline - halfspace),y),fill=1)
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
                draw.line((x, y) + (x,height-1),fill=1)
                return (x,height-1)
                break
            else:
                #print('RIGHT')
                draw.line((x, y) + (x,y+(fullline - halfspace)),fill=1)
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
                draw.line((x, y) + (x,0),fill=1)
                return (x,0)
                break
            else:
                #print("not broken?")
                draw.line((x, y) + (x,y-(fullline - halfspace)),fill=1)
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
        for i in range(3):
            r = maze.getpixel((x,y+(int(halfspace) + i)))
            if (r == 0):
                z = 1
        if (z == 1):
            #print (r, "Turn Up, coordinates:",x,y)
            return True
            #return ("Turn Up")
        else:
            return (0)
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
    z = 0
    for i in range(3):
        r = maze.getpixel((x-(int(halfspace) + i),y))
        #print('x,y:',((x-(int(halfspace) + i),y)),"r:",r)
        if (r == 0):
            z = 1
            #print("R:", r)
    #print ("GOOD SO FAR")
    if (z == 0):
        for i in range(3):
            r = maze.getpixel((x+(int(halfspace) + i),y))
            print("this is r:",r,x,(x+(int(halfspace) + i),y))
            if (r == 0):
                z = 1
        if (z == 1):
            print (r, "Turn Left, coordinates:",x,y)
            #print("\n------\n")
            return True
            #return ("Turn Left")
        else:
            return (0)
    else:
        for i in range(3):
            r = maze.getpixel((x+(int(halfspace) + i),y))
            print("this is r:",r,x,(x+(int(halfspace) + i),y))
            if (r == 0):
                z = 2
        if (z == 1):
            print (r, "Turn Right, coordinates:",x,y)
            return False
            #return ("Turn Right")
        else:
            return ('Dead end')


def rightSequence(x,y):
    drawRight(x,y)
    #checkIfBothFalse = 0
    print("instide right sequence before any changes: x,y,drawRight(x, y)[0]:", x, y,drawRight(x, y)[0])

    if (rightDivergeDown(x,y,drawRight(x, y)[0])[0]) == True:
        #print ("    rightSequence if rightDivDownCheck is True, x,y:",x,y)
        listdivs = rightDivergeDown(x,y,drawRight(x, y)[0])[1]
        #print("    listdivs:",listdivs)
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],y,3)) == True:
                #print('rDU, listdiv[i]:',listdivs[i])
                return True
            #print('listdiv[i]:',listdivs[i])
    if (rightDivergeUp(x,y,drawRight(x, y)[0])[0]) == True:
        listdivs = rightDivergeUp(x,y,drawRight(x, y)[0])[1]
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],y,2)) == True:
                return True
    x,y = drawRight(x, y)
    if checkVert(x,y) is False:
        nextDir = 3
        return nextDir
    elif checkVert(x,y) is True:
        nextDir = 2
        return nextDir
    elif checkVert(x,y) is 0:
        if pathFind(x,y,3) == True:
            return True
        else:
            nextDir = 2
            return nextDir
    else:
        print("checkVert:",checkVert(x,y))
        nextDir = 4
        return nextDir

def leftSequence(x,y):
    drawLeft(x,y)

    print("Entered left sequence")
    if (leftDivergeDown(x,y,drawLeft(x, y)[0])[0]) == True:
        listdivs = leftDivergeDown(x,y,drawLeft(x, y)[0])[1]
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],y,3)) == True:
                #print('rDU, listdiv[i]:',listdivs[i])
                return True
    if (leftDivergeUp(x,y,drawLeft(x, y)[0])[0]) == True:
        listdivs = leftDivergeUp(x,y,drawLeft(x, y)[0])[1]
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],y,2)) == True:
                return True

    x,y = drawLeft(x, y)

    if checkVert(x,y) is False:
        #print ("nextDir = Down")
        nextDir = 3
        return nextDir
    elif checkVert(x,y) is True:
        #print ("nextDir = Up")
        nextDir = 2
        return nextDir
    elif checkVert(x,y) is 0:
        if pathFind(x,y,3) == True:
            return True
        else:
            nextDir = 2
            return nextDir
    else:
        nextDir = 4
        return nextDir
def downSequence(x,y):
    #print('x,y downSeq',x,y)
    drawDown(x,y)
    if (downDivergeRight(x,y,drawDown(x, y)[1])[0]) == True:
        #print ("    downSequence if downDivRightCheck is True, x,y:",x,y)
        listdivs = downDivergeRight(x,y,drawDown(x, y)[1])[1]
        for i in range(len(listdivs)):
            if (pathFind(x,listdivs[i],0)) == True:
                return True
            #print('listdiv[i]:',listdivs[i])
    #else:
        #print ("    downSequence if downDivRightCheck is False, x,y:",x,y)
    if (downDivergeLeft(x,y,drawDown(x, y)[1])[0]) == True:
        #print ("    downSequence if downDivLeftCheck is True, x,y:",x,y)
        listdivs = downDivergeLeft(x,y,drawDown(x, y)[1])[1]
        for i in range(len(listdivs)):
            if (pathFind(x,listdivs[i],1)) == True:
                return True
    x,y = drawDown(x, y)
    if checkHor(x,y) is False:
        #print ("nextDir = Right")
        nextDir = 0
        return nextDir
    elif checkHor(x,y) is True:
        #print ("nextDir = Left")
        nextDir = 1
        return nextDir
    elif checkHor(x,y) is 0:
        if pathFind(x,y,0) == True:
            return True
        else:
            nextDir = 1
            return nextDir
    else:
        nextDir = 4
        return nextDir
def upSequence(x,y):
    drawUp(x,y)
    if (upDivergeRight(x,y,drawUp(x, y)[1])[0]) == True:
        #print ("    downSequence if downDivRightCheck is True, x,y:",x,y)
        listdivs = upDivergeRight(x,y,drawUp(x, y)[1])[1]
        for i in range(len(listdivs)):
            if (pathFind(x,listdivs[i],0)) == True:
                return True
    if (upDivergeLeft(x,y,drawUp(x, y)[1])[0]) == True:
        #print ("    downSequence if downDivLeftCheck is True, x,y:",x,y)
        listdivs = upDivergeLeft(x,y,drawUp(x, y)[1])[1]
        for i in range(len(listdivs)):
            if (pathFind(x,listdivs[i],1)) == True:
                return True

    x,y = drawUp(x, y)
    #print ("HEREREREREREERE", x,y)
    if checkHor(x,y) is False:
        #print ("nextDir = Right")
        nextDir = 0
        return nextDir
    elif checkHor(x,y) is True:
        #print ("nextDir = Left")
        nextDir = 1
        return nextDir
    elif checkHor(x,y) is 0:
        if pathFind(x,y,0) == True:
            return True
        else:
            nextDir = 1
            return nextDir
    else:
        print("dead end")
        nextDir = 4
        return nextDir

def pathFind(x,y,nextDir):
    print("entered pathFind <----->",x,y,nextDir)
    #Right = 0, Left = 1, Up = 2, Down = 3
    #DrawRight = 0, DrawLeft = 1, DrawUp = 2, DrawDown = 3
    global vertexList
    tempList = []
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
        print("range new------")
        if nextDir == 0:
            print("------------------->TURN RIGHT<-------------------",x,y)
            currentDir = nextDir
            nextDir = rightSequence(x,y)
            #print("got here",x, y)
            #rightDiverge(x,y,drawRight(x, y)[0])
            x,y = drawRight(x, y)
            #print("got here1", x, y)
            #print("x: ", x)
            xcheck = x
            print("templist append (x,y): ",x,y)
            tempList.append([x,y])
            #print("got here2", nextDir, xcheck)
            if xcheck == 0 or xcheck == (width-1):
                nextDir = 5
                xcheck = 1
                print ('xcheck', xcheck,nextDir)
            if nextDir is True:
                nextDir = 5
        elif nextDir == 1:
            print("------------------->TURN LEFT<-------------------",x,y)
            currentDir = nextDir
            #print("checkpoint1")
            #leftSequence(x,y)
            #print("checkpoint2")
            nextDir = leftSequence(x,y)
            #print("checkpoint3")
            #print ("mid full left seq",x,y)
            x,y = drawLeft(x, y)
            #print("checkpoint4")
            xcheck = x
            print("templist append (x,y): ",x,y)
            tempList.append([x,y])
            #print("checkpoint5")
            if xcheck == 0 or xcheck == (width-1):
                nextDir = 5
                xcheck = 1
                print ('xcheck', xcheck,nextDir, x, y)
            print("nextDir:",nextDir)
            if nextDir is True:
                nextDir = 5
                
            #print ("checkpoint6, nextDir: ", nextDir)
        elif nextDir == 2:
            print("------------------->TURN UP<-------------------",x,y)
            currentDir = nextDir
            #upSequence(x,y)
            nextDir = upSequence(x,y)
            x,y = drawUp(x, y)
            ycheck = y
            print("templist append (x,y): ",x,y)
            tempList.append([x,y])
            if ycheck == 0 or ycheck == (height-1):
                nextDir = 5
                ycheck = 1
                print ('ycheck', ycheck,nextDir)
            if nextDir is True:
                nextDir = 5
            #print ("coordinates: ", x,y)
            #print ("nextDir: ", nextDir)
            #print(x, y, xcheck,"ycheck: ",ycheck)
        elif nextDir == 3:
            print("------------------->TURN DOWN<-------------------",x,y)
            currentDir = nextDir
            #print("about to find nextDir:", nextDir)
            nextDir = downSequence(x,y)
            #print("nextDir:",nextDir)
            x,y = drawDown(x, y)
            #print("nextDir:",nextDir)
            #print("checking x and y after downSeq and drawDown:",x,y)
            ycheck = y
            tempList.append([x,y])
            print("templist append (x,y): ",x,y,tempList)
            
            if ycheck == 0 or ycheck == (height-1):
                nextDir = 5
                ycheck = 1
                print ('ycheck', ycheck,nextDir)
            #print("nextDir:",nextDir)
            if nextDir is True:
                #print("nextDir:",nextDir)
                nextDir = 5
            
            #print ("y",y)
            #print ("coordinates: ", x,y)
            #print ("nextDir: ", nextDir)
        elif nextDir == 4:
            print("dead end, break",x,y,"templist removed:",tempList)
            xcheck = 0
            return False
            break
        elif nextDir == 5:
            print ("PATHWAY FOUND")
            break
        else:
            print ("Error: ", nextDir)
            #print (xcheck, ycheck)
            #print ("startDir: ", startDir)
    if nextDir == 4:
        print('final',origx,origy,x,y)
        #xcheck = 0
        #return False,currentDir,origx,origy,x,y
        return False
    elif nextDir == 5:
        print("right before vertexList",tempList)
        for i in tempList:
            vertexList.append(i)
        return True
    else:
        print ("uhh what is this")

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
    print("leftDivergeUp entered")
    width = 0
    distance = x - newx
    #print("prepreprehalfspace-----", distance,newx,x,halfspace,halfspace+(halfspace/4))
    distance -= (halfspace+(halfspace/3))
    #print("preprehalfspace-----", distance,newx,x,halfspace)
    i = 1
    divpoint = 0
    listdivs = []
    #print("LdU",distance)
    if (maze.getpixel((x-1,y - halfspace - 2)) > 0):
        distance -= (halfspace+(halfspace/3))
        x -= (halfspace+(halfspace/4))
        #print("prehalfspace-----", distance,newx,x,halfspace)
    #print("i",i)
    while((distance - i + 1) > 0):
    #for i in range(distance):
        r = maze.getpixel((x - i,y - halfspace - 2))
        if r > 0:
            #print("diverge,", "i:",i, i+pathwidth, x)
            divpoint = x - i + 1 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
            #print('divpoint',divpoint)
            #print(x - i)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs
def leftDivergeDown(x,y,newx):
    width = 0
    distance = x - newx
    #print("prepreprehalfspace-----", distance,newx,x,halfspace)
    distance -= (halfspace+(halfspace/4))
    #print("preprehalfspace-----", distance,newx,x,halfspace,halfspace+(halfspace/4))
    i = 1
    divpoint = 0
    listdivs = []
    #print("LdD",distance)
    if (maze.getpixel((x-1,y + halfspace + 2)) > 0):
        distance -= (halfspace+(halfspace/4))
        x -= (halfspace+(halfspace/4))
        #print("prehalfspace-----", distance,newx,x,halfspace)
    #print("i",i)
    while((distance - i + 1) > 0):
    #for i in range(distance):
        r = maze.getpixel((x - i,y + halfspace + 2))
        if r > 0:
            #print("diverge,", "i:",i, i+pathwidth, x)
            divpoint = x - i + 1 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
            #print('divpoint',divpoint)
            #print(x - i)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs
        
def rightDivergeUp(x,y,newx):
    width = 0
    distance = newx - x
    i = 1
    divpoint = 0
    distance -= (halfspace+(halfspace/4))
    listdivs = []
    #print("RdU",distance)
    if (maze.getpixel((x+1,y - halfspace - 2)) > 0):
        distance -= (halfspace+(halfspace/3))
        x += (halfspace+(halfspace/4))
        #print("halfspace-----", distance,x,halfspace)
    #print("i",i)
    #Gives a list of points of diversion
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x + i,y - halfspace - 2))
        if r > 0:
            #print("diverge,", "i:",i, i+pathwidth, x)
            divpoint = x + i - 1 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
            #print('divpoint',divpoint)
            #print(x + i)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs

def rightDivergeDown(x,y,newx):
    width = 0
    distance = newx - x
    #print("preprehalfspace-----", distance,newx,x,halfspace,(halfspace/3),halfspace+(halfspace/3))
    distance -= (halfspace+(halfspace/3))
    #print("prehalfspace-----", distance,x,halfspace)
    i = 1
    divpoint = 0
    listdivs = []
    #print("RdD",distance)
    if (maze.getpixel((x+1,y + halfspace + 2)) > 0):
        distance -= (halfspace+(halfspace/3))
        x += (halfspace+(halfspace/4))
        #print("halfspace-----", distance,x,halfspace)
    #print("i",i)
    #Gives a list of points of diversion
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x + i,y + halfspace + 2))
        if r > 0:
            #print("diverge,", "i:",i, i+pathwidth, x)
            divpoint = x + i - 1 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
            #print('divpoint',divpoint)
            #print(x + i)
        i += 1
    
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs

def downDivergeLeft(x,y,newy):
    width = 0
    distance = newy - y
    #print("preprehalfspace-----", distance,newy,y,halfspace,(halfspace/3),halfspace+(halfspace/3))
    i = 1
    divpoint = 0
    distance -= (halfspace+(halfspace/3))
    #print("preprehalfspace-----", distance,newy,y,halfspace)
    listdivs = []
    #print("DdL",distance)
    if (maze.getpixel((x - halfspace - 2,y + i)) > 0):
        distance -= (halfspace+(halfspace/3))
        y += (halfspace+(halfspace/4))
        #print("halfspace-----", distance,y,halfspace)
    #print("i",i)
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x - halfspace - 2,y + i))
        if r > 0:
            #print("diverge,", "i:",i, i+pathwidth, y)
            divpoint = y + i - 1 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
            #print('divpoint',divpoint)
            #print(y + i)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        print("len(listdivs) = 0:",listdivs)
        return False, listdivs

def downDivergeRight(x,y,newy):
    width = 0
    distance = newy - y
    i = 1
    divpoint = 0
    distance -= (halfspace+(halfspace/3))
    listdivs = []
    #print("DdR",distance)
    if (maze.getpixel((x + halfspace + 2,y + i)) > 0):
        distance -= (halfspace+(halfspace/3))
        y += (halfspace+(halfspace/4))
        #print("halfspace-----", distance,y,halfspace)
    #print("i",i)
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x + halfspace + 2,y + i))
        if r > 0:
            #print("diverge,", "i:",i, i+pathwidth, y)
            divpoint = y + i - 1 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
            #print('divpoint',divpoint)
            #print(y + i)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs

def upDivergeLeft(x,y,newy):
    width = 0
    distance = y - newy
    i = 1
    divpoint = 0
    distance -= (halfspace+(halfspace/3))
    listdivs = []
    #print("UdL",distance)
    if (maze.getpixel((x - halfspace - 2,y - i)) > 0):
        distance -= (halfspace+(halfspace/3))
        y -= (halfspace+(halfspace/4))
        #print("halfspace-----", distance,y,halfspace)
    #print("i",i)
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x - halfspace - 2,y - i))
        if r > 0:
            #print("diverge,", "i:",i, i+pathwidth, y)
            divpoint = y - i - 1 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
            #print('divpoint',divpoint)
            #print(y - i)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs
    #print("i",i)
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x + halfspace + 2,y - i))
        if r > 0:
            #print("diverge,", "i:",i, i+pathwidth, y)
            divpoint = y - i - 1 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
            #print('divpoint',divpoint)
            #print(y - i)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs
def upDivergeRight(x,y,newy):
    width = 0
    distance = y - newy
    i = 1
    divpoint = 0
    distance -= (halfspace+(halfspace/3))
    listdivs = []
    #print("UdR",distance)
    if (maze.getpixel((x + halfspace + 2,y - i)) > 0):
        distance -= (halfspace+(halfspace/3))
        y -= (halfspace+(halfspace/4))
        #print("halfspace-----", distance,y,halfspace)
    #print("i",i)
    #print("i",i)
    while((distance - i - 1) > 0):
    #for i in range(distance):
        #print('CALCTEST:',distance - i - 1)
        r = maze.getpixel((x + halfspace + 2,y - i))
        if r > 0:
            #print("diverge,", "i:",i, i+pathwidth, y)
            #print("diverge,", "i:",i, i+pathwidth, y)
            divpoint = y - i - 1 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
            #print('divpoint',divpoint)
            #print(y - i)
            #print('divpoint',divpoint)
            #print(y - i)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs

#CHECK 218 FOR ALL

##################################


"""
#pathFind(1,109,0,True)
#print(rightDivergeDown(1,109,69),"---------------------------------------------")
#print("---------------------------------------------",pathFind(27,109,3))
#print("final coordinates",x,y)
#rightDiverge(1,109,69)

"""
vertexList.append([1,109])
#mainFunction(1,109,0,False)
if (pathFind(1,109,0)) == True:
    print("\nFinal path found.",vertexList)
else:
    print("\nError in maze.",vertexList)

countList = 0

print(vertexList)
"""
for i in vertexList:
    for j in range((len(i))-1):
        #draw.line((i[j][0], i[j][1]) + (x,0),fill=2)
        #print(i[j][0],i[j][1],"|",i[j+1][0],i[j+1][1])
        print (j)
        print(i[j-1][0],i[j][1])

print("\n\n")
for i in vertexList:
    for j in i:
        #draw.line((i[j][0], i[j][1]) + (x,0),fill=2)
        #print(i[j][0],i[j][1],"|",i[j+1][0],i[j+1][1])
        if countList == len(i):
            break
        else:
            #print(j[0],j[1],len(i),i[countList])
            print(i[countList][0],i[countList][1],len(i))
            countList += 1
        #print("count:",countList)
"""
for i in range(len(vertexList)-1):
    #print(vertexList[i][0],vertexList[i][1], "|",vertexList[i+1][0],vertexList[i+1][1])
    draw.line((vertexList[i][0],vertexList[i][1]) + (vertexList[i+1][0],vertexList[i+1][1]),fill=2)

    
##################################
maze.save('maze1 backup sharpen fill.png', 'PNG')

print("-----------------MAZE SOLVED------------------\n")

