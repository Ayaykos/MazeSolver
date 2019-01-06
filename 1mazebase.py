from PIL import Image, ImageColor, ImageDraw
from checkentry import checkEntry
import sys


###Setup
#print(ImageColor.getcolor('red', 'RGBA'))
#basefilename = input('Enter Maze File Name (no extension/suffix): ')
#filename = basefilename + '.png'
filename = 'maze1 backup.png'
maze = Image.open(filename)
maze2 = maze
maze = maze.convert('P') # conversion
#maze = maze.load()
#maze.save(basefilename + 'solvedbw.png', 'PNG')

draw = ImageDraw.Draw(maze)
draw2 = ImageDraw.Draw(maze2)
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
checkWhenTrue = 0
countRecurse = 0


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

print("RCHECK AT 108,28:",maze.getpixel((108,28)))

#getValues(whitecount,halfspace)


#print("halfspace: ", halfspace, "whitecount: ",whitecount, "temp: ",temp, "startpnt: ",startpnt, "startDir: ",startDir)
#print(maze.getpixel((0, startpnt)))
#print(maxwidth)
###----------------------------------------


###Direction Functions
def drawRight(x,y):
    fullline = 0
    print("drawRight,x,y,i:",x,y)
    for i in range(width):
        #print("i:",i)
        if i == 0:
            print("i:",i)
            continue
        #print("got here 1--------", startpnt)
        if (i+x) <= (width-1):
            r = maze.getpixel((i+x,y))
            #print("r at i+x,y:",r,"at",i+x,y)
        else:
            r = 0
        if (r > 0) and (i + x <= (width - 1)):
            fullline = i
            print("got here 2--------")
        else:
            print("got here 3--------,r,x,i+x,y:",r,x,i+x,y)
            if (i + x > (width - 1)):
                #print("got here 4--------", fullline)
                draw.line((x, y) + (width-1,y),fill="black")
                return (width-1, y)
                break
            else:
                print("got here 5--------",x+(fullline - halfspace),y,"fulline,halfspace:",fullline,halfspace)
                draw.line((x, y) + (x+(fullline - halfspace),y),fill="black")
                return (x+(fullline - halfspace),y)
                break
def drawLeft(x,y):
    fullline = 0
    for i in range(width):
        if i == 0:
            continue
        if (x - i >= 1):
            r = maze.getpixel((x-i,y))
        else:
            r = 0
        if (r > 0) and (x - i >= 1):
            fullline = i
        else:
            if (x - i < 1):
                draw.line((x, y) + (0,y),fill="black")
                return (0, y)
                break
            else:
                draw.line((x, y) + (x-(fullline - halfspace),y),fill="black")
                return (x-(fullline - halfspace),y)
                break

def drawDown(x,y):
    fullline = 0
    print("drawDown",x,y)
    for i in range(width):
        if i == 0:
            continue
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
                print (x,y+i)
                draw.line((x, y) + (x,height-1),fill="black")
                return (x,height-1)
                break
            else:
                #print('RIGHT')
                draw.line((x, y) + (x,y+(fullline - halfspace)),fill="black")
                print('coor, right:',x,y+(fullline - halfspace),fullline)
                return (x,y+(fullline - halfspace))
                print("wtf")
                break
    
def drawUp(x,y):
    fullline = 0
    for i in range(width):
        if i == 0:
            continue
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
                draw.line((x, y) + (x,0),fill="black")
                return (x,0)
                break
            else:
                #print("not broken?")
                draw.line((x, y) + (x,y-(fullline - halfspace)),fill="black")
                return (x,y-(fullline - halfspace))
                break

###Check Functions
    #Down/Right = False
def checkVert(x,y):
    print("inside checkvert")
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
    print("began checkHor,x,y:",x,y)
    for i in range(3):
        print(((x-(int(halfspace) + i),y)),x,y)
        r = maze.getpixel((x-(int(halfspace) + i),y))
        print('x,y:',((x-(int(halfspace) + i),y)),"r:",r)
        if (r == 0):
            z = 1
            #print("R:", r)
    #print ("GOOD SO FAR")
    if (z == 0):
        for i in range(3):
            r = maze.getpixel((x+(int(halfspace) + i),y))
            #print("this is r:",r,x,(x+(int(halfspace) + i),y))
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
            print("checkHor else,z=",z)
            return ('Dead end')


def rightSequence(x,y):
    oldx,oldy = x,y
    x,y = drawRight(x, y)
    if x == width - 1:
        return True
    #checkIfBothFalse = 0
    print("instide right sequence before any changes: x,y,drawRight(x, y)[0]:", oldx, oldy,x)

    if (rightDivergeDown(oldx,oldy,x)[0]) == True:
        #print ("    rightSequence if rightDivDownCheck is True, x,y:",x,y)
        listdivs = rightDivergeDown(oldx,oldy,x)[1]
        #print("    listdivs:",listdivs)
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],oldy,3)) == True:
                #print('rDU, listdiv[i]:',listdivs[i])
                return True
            #print('listdiv[i]:',listdivs[i])
    if (rightDivergeUp(oldx,oldy,x)[0]) == True:
        listdivs = rightDivergeUp(oldx,oldy,x)[1]
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],oldy,2)) == True:
                return True
    print("right before checkVert in rightSequence") 
    if checkVert(x,y) is False:
        print("false")
        nextDir = 3
        return nextDir
    elif checkVert(x,y) is True:
        print("truee")
        nextDir = 2
        return nextDir
    elif checkVert(x,y) is 0:
        print("pathFind")
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
    oldx, oldy = x,y
    x,y = drawLeft(x, y)
    if x == 0:
        return True
    print("Entered left sequence")
    if (leftDivergeDown(oldx,oldy,x)[0]) == True:
        listdivs = leftDivergeDown(oldx,oldy,x)[1]
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],oldy,3)) == True:
                #print('rDU, listdiv[i]:',listdivs[i])
                return True
    if (leftDivergeUp(oldx,oldy,x)[0]) == True:
        listdivs = leftDivergeUp(oldx,oldy,x)[1]
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],oldy,2)) == True:
                return True

    #x,y = drawLeft(x, y)

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
    #drawDown(x,y)
    oldx,oldy = x,y
    x,y = drawDown(x, y)
    if y == height - 1:
        return True
    if (downDivergeRight(oldx,oldy,y)[0]) == True:
        print ("    downSequence if downDivRightCheck is True, x,y:",oldx,oldy)
        listdivs = downDivergeRight(oldx,oldy,y)[1]
        for i in range(len(listdivs)):
            if (pathFind(oldx,listdivs[i],0)) == True:
                return True
            #print('listdiv[i]:',listdivs[i])
    else:
        print ("    downSequence if downDivRightCheck is False, x,y:",x,y)
    if (downDivergeLeft(oldx,oldy,y)[0]) == True:
        print ("    downSequence if downDivLeftCheck is True, x,y:",oldx,oldy)
        listdivs = downDivergeLeft(oldx,oldy,y)[1]
        for i in range(len(listdivs)):
            if (pathFind(oldx,listdivs[i],1)) == True:
                return True
    else:
        print ("    downSequence if downDivLeftCheck is False, x,y:",x,y)    
    print("right before checkHor from downseq",x,y)
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
        print("nextDir else,checkHor=",checkHor(x,y))
        nextDir = 4
        return nextDir
def upSequence(x,y):
    oldx,oldy = x,y
    x,y = drawUp(x, y)
    if y == 0:
        return True
    if (upDivergeRight(oldx,oldy,y)[0]) == True:
        #print ("    downSequence if downDivRightCheck is True, x,y:",x,y)
        listdivs = upDivergeRight(oldx,oldy,y)[1]
        for i in range(len(listdivs)):
            if (pathFind(oldx,listdivs[i],0)) == True:
                return True
    if (upDivergeLeft(oldx,oldy,y)[0]) == True:
        #print ("    downSequence if downDivLeftCheck is True, x,y:",x,y)
        listdivs = upDivergeLeft(oldx,oldy,y)[1]
        for i in range(len(listdivs)):
            if (pathFind(oldx,listdivs[i],1)) == True:
                return True

    
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
    global checkWhenTrue
    global countRecurse
    """
    if countRecurse == 0:
        print("COUNT RECURSE XY:",x,y)
        tempList = []
    else:
        tempList = [[x,y]]
    """
    tempList = [[x,y]]
    origx = x
    origy = y
    xcheck = 1
    ycheck = 1
    ###Main loop
    #while (xcheck is not 0) and (xcheck is not (width-1)) and (ycheck is not 0) and (ycheck is not (height-1)):
    while nextDir is not 5:
    #for i in range(38):
        #if not ((xcheck < width or xcheck >= 1)):
        #    print ("BROKEN")
        #if not ((ycheck >= 1)):
        #    print ("BROKEN")
        print("range new------")
        if nextDir == 0:
            print("------------------->TURN RIGHT<-------------------",x,y)
            currentDir = nextDir
            #oldx,oldy = x,y
            #x,y = drawRight(x, y)
            nextDir = rightSequence(x,y)
            x,y = drawRight(x, y)
            print("got here",x, y)
            #rightDiverge(x,y,drawRight(x, y)[0])
            #print("got here1", x, y)
            #print("x: ", x)
            xcheck = x
            countRecurse += 1
            print("templist append (x,y): ",x,y)
            #tempList.append([x,y])
            #print("got here2", nextDir, xcheck)
            if xcheck == 0 or xcheck == (width-1):
                nextDir = 5
                xcheck = 1
                print ('xcheck', xcheck,nextDir)
            if nextDir is True:
                nextDir = 5
            if checkWhenTrue == 0:
                tempList.append([x,y])
        elif nextDir == 1:
            print("------------------->TURN LEFT<-------------------",x,y)
            currentDir = nextDir
            #print("checkpoint1")
            #leftSequence(x,y)
            #print("checkpoint2")
            #oldx,oldy = x,y
            #x,y = drawLeft(x, y)
            nextDir = leftSequence(x,y)
            #print("checkpoint3")
            #print ("mid full left seq",x,y)
            x,y = drawLeft(x, y)
            #print("checkpoint4")
            xcheck = x
            countRecurse += 1
            print("templist append (x,y): ",x,y)
            
            #print("checkpoint5")
            if xcheck == 0 or xcheck == (width-1):
                nextDir = 5
                xcheck = 1
                print ('xcheck', xcheck,nextDir, x, y)
            print("nextDir:",nextDir)
            if nextDir is True:
                nextDir = 5
            if checkWhenTrue == 0:
                tempList.append([x,y])

            #print ("checkpoint6, nextDir: ", nextDir)
        elif nextDir == 2:
            print("------------------->TURN UP<-------------------",x,y)
            currentDir = nextDir
            #upSequence(x,y)
            nextDir = upSequence(x,y)
            x,y = drawUp(x, y)
            ycheck = y
            countRecurse += 1
            print("templist append (x,y): ",x,y)
            #tempList.append([x,y])
            if ycheck == 0 or ycheck == (height-1):
                nextDir = 5
                ycheck = 1
                print ('ycheck', ycheck,nextDir)
            if nextDir is True:
                nextDir = 5
            if checkWhenTrue == 0:
                tempList.append([x,y])
            #print ("coordinates: ", x,y)
            #print ("nextDir: ", nextDir)
            #print(x, y, xcheck,"ycheck: ",ycheck)
        elif nextDir == 3:
            print("------------------->TURN DOWN<-------------------",x,y)
            currentDir = nextDir
            print("about to find nextDir:", nextDir)
            nextDir = downSequence(x,y)
            print("nextDir:",nextDir)
            x,y = drawDown(x, y)
            #print("nextDir:",nextDir)
            #print("checking x and y after downSeq and drawDown:",x,y)
            ycheck = y
            
            countRecurse += 1
            #tempList.append([x,y])
            print("templist append (x,y): ",x,y,tempList)
            
            if ycheck == 0 or ycheck == (height-1):
                nextDir = 5
                ycheck = 1
                print ('ycheck', ycheck,nextDir)
            #print("nextDir:",nextDir)
            if nextDir is True:
                #print("nextDir:",nextDir)
                nextDir = 5
            if checkWhenTrue == 0:
                tempList.append([x,y])            
            #print ("y",y)
            #print ("coordinates: ", x,y)
            #print ("nextDir: ", nextDir)
        elif nextDir == 4:
            print("dead end, break",x,y,"templist removed:",tempList)
            xcheck = 0
            print("<--------------------------------------------------------------------------------reverserecurse",tempList)
            tempList = []
            countRecurse += 1
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
        #print('final',origx,origy,x,y)
        print("<--------------------------------------------------------------------------------reverserecurse",tempList)
        tempList = []
        countRecurse += 1
        #xcheck = 0
        #return False,currentDir,origx,origy,x,y
        return False
    elif nextDir == 5:
        print("right before vertexList",tempList,x,y)
        print("<--------------------------------------------------------------------------------reverserecurse",tempList)
        for i in tempList:
            vertexList.append(i)
        checkWhenTrue = 1
        countRecurse += 1
        return True
    else:
        print ("uhh what is this")


#pathFind(x,y,nextDir)

#maze.save(basefilename + 'solved.png', 'PNG')

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
###Check entry point
x = checkEntry(filename)[3] 
y = checkEntry(filename)[4]
print("-----------------------------------------------------x,y:",x,y,startDir)
vertexList.append([x,y])
"""
#print ("startDir: ", startDir)
if startDir == 1:
    print("X,Y" , x,y)
    leftSequence(x,y)
    vertexList.append([x,y])
    print("X,Y" , x,y)
    nextDir = leftSequence(x,y)
    print("nextDirleft",nextDir)
    #vertexList.append([x,y])
    x,y = drawLeft(x, y)
    
    print("------------------------------------------------------",[x,y])
elif startDir == 0:
    rightSequence(x,y)
    nextDir = rightSequence(x,y)
    print("nextDirRight",nextDir)
    #vertexList.append([x,y])
    x,y = drawRight(x, y)
    vertexList.append([x,y])
    print("------------------------------------------------------",x,y)
elif startDir == 2:
    #print("X,Y" , x,y)
    downSequence(x,y)
    nextDir = downSequence(x,y)
    #vertexList.append([x,y])
    x,y = drawDown(x, y)
    vertexList.append([x,y])
    print("------------------------------------------------------",x,y)
    #print ("nextDir: ", nextDir)
elif startDir == 3:
    upSequence(x,y)
    nextDir = upSequence(x,y)
    #vertexList.append([x,y])
    x,y = drawUp(x, y)
    vertexList.append([x,y])
    print("------------------------------------------------------",x,y)
"""
r = maze.getpixel((109,1))
r2 = maze.getpixel((217,1))
print(r,r2)
#print("nextDir", nextDir)
#vertexList.append([1,109])
#mainFunction(1,109,0,False)

if (pathFind(x,y,startDir)) == True:
    print("\nFinal path found.")
else:
    print("\nError in maze.")

print("\n",vertexList)    
"""
for i in range(len(vertexList)-1):
    draw.line((vertexList[i][0],vertexList[i][1]) + (vertexList[i+1][0],vertexList[i+1][1]),fill="black")
"""


#draw.line((1,1) + (217,217),fill="black")
##################################
#maze.save('maze1 backup sharpen fill.png', 'PNG')
maze.save('maze1 backup solved.png', 'PNG')

print("-----------------MAZE SOLVED------------------\n")
#print("Check file:",basefilename + ' solved.png')
