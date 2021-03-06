from PIL import Image, ImageColor, ImageDraw, ImageEnhance
from checkentry import checkEntry
import os
import time
from decimal import Decimal

###Global vars
temp = 0
fullline = 0
vertexList = []
checkWhenTrue = 0
countRecurse = 0
whitecount = 0
startDir = 0
temp = 0
startpnt = 0
pathwidth = 0
halfspace = 0
count = 0

def resetGlobVars():
    global fullline
    fullline = 0
    global vertexList
    vertexList = []
    global checkWhenTrue
    checkWhenTrue = 0
    global countRecurse
    countRecurse = 0
    global whitecount
    whitecount = 0
    global startDir
    startDir = 0
    global temp
    temp = 0
    global startpnt
    startpnt = 0
    global pathwidth
    pathwidth = 0
    global halfspace
    halfspace = 0

###Rounding Functions
def roundUp(x):
    y = str(float(x))
    if y[-1] != '0':
        x = int(x)+1
    return x
def roundDown(x):
    y = str(float(x))
    if y[-1] != '0':
        x = int(x)
    return x

#############################################################################################
    
###Direction Draw Functions

def drawRight(x,y):
    global count
    count += 1
    fullline = 0
    for i in range(width):
        if i == 0:
            continue
        if (i+x) <= (width-1):
            r = maze.getpixel((i+x,y))
        else:
            r = 0
        if (r > 0) and (i + x <= (width - 1)):
            fullline = i
        else:
            if (i + x > (width - 1)):
                draw.line((x, y) + (width-1,y),fill=1)
                return (width-1, y)
                break
            else:
                draw.line((x, y) + (x+(fullline - halfspace),y),fill=1)
                return (x+(fullline - halfspace),y)
                break
def drawLeft(x,y):
    global count
    count += 1
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
                draw.line((x, y) + (0,y),fill=1)
                return (0, y)
                break
            else:
                draw.line((x, y) + (x-(fullline - halfspace),y),fill=1)
                return (x-(fullline - halfspace),y)
                break

def drawDown(x,y):
    global count
    count += 1
    fullline = 0
    for i in range(width):
        if i == 0:
            continue
        if (i + y <= height - 1):
            r = maze.getpixel((x,i+y))
        else:
            r = 0
        if (r > 0) and (i + y <= height - 1):
            fullline = i
        else:
            if (y + i > height - 1):
                draw.line((x, y) + (x,height-1),fill=1)
                return (x,height-1)
                break
            else:
                draw.line((x, y) + (x,y+(fullline - halfspace)),fill=1)
                return (x,y+(fullline - halfspace))
                break
    
def drawUp(x,y):
    global count
    count += 1
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
        else:
            if(y - i < 1):
                draw.line((x, y) + (x,0),fill=1)
                return (x,0)
                break
            else:
                draw.line((x, y) + (x,y-(fullline - halfspace)),fill=1)
                return (x,y-(fullline - halfspace))
                break

###Check next Direction Functions
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
            return True
            #Turn Up
        else:
            return (0)
    else:
        z = 0
        for i in range(3):
            r = maze.getpixel((x,y+(int(halfspace) + i)))
            if (r == 0):
                z = 1
        if (z == 0):
            return False
            #Turn Down
        else:
            return ('Dead end')

def checkHor(x,y):
    z = 0
    for i in range(3):
        r = maze.getpixel((x-(int(halfspace) + i),y))
        if (r == 0):
            z = 1
    if (z == 0):
        for i in range(3):
            r = maze.getpixel((x+(int(halfspace) + i),y))
            if (r == 0):
                z = 1
        if (z == 1):
            return True
            #Turn Left
        else:
            return 0
    else:
        for i in range(3):
            r = maze.getpixel((x+(int(halfspace) + i),y))
            if (r == 0):
                z = 2
        if (z == 1):
            return False
            #Turn Right
        else:
            return ('Dead end')
        
#############################################################################################

###Pathway Sequence Functions

def rightSequence(x,y):
    oldx,oldy = x,y
    x,y = drawRight(x, y)
    if x == width - 1:
        return True,x,y

    if (rightDivergeDown(oldx,oldy,x)[0]) == True:
        listdivs = rightDivergeDown(oldx,oldy,x)[1]
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],oldy,3)) == True:
                return True,x,y
    if (rightDivergeUp(oldx,oldy,x)[0]) == True:
        listdivs = rightDivergeUp(oldx,oldy,x)[1]
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],oldy,2)) == True:
                return True,x,y
    if checkVert(x,y) is False:
        #nextDir = Down
        nextDir = 3
        return nextDir,x,y
    elif checkVert(x,y) is True:
        #nextDir = Up
        nextDir = 2
        return nextDir,x,y
    elif checkVert(x,y) is 0:
        #Breakpoint
        if pathFind(x,y,3) == True:
            return True,x,y
        else:
            nextDir = 2
            return nextDir,x,y
    else:
        #Dead end
        nextDir = 4
        return nextDir,x,y

def leftSequence(x,y):
    oldx, oldy = x,y
    x,y = drawLeft(x, y)
    if x == 0:
        return True,x,y
    if (leftDivergeDown(oldx,oldy,x)[0]) == True:
        listdivs = leftDivergeDown(oldx,oldy,x)[1]
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],oldy,3)) == True:
                return True,x,y
    if (leftDivergeUp(oldx,oldy,x)[0]) == True:
        listdivs = leftDivergeUp(oldx,oldy,x)[1]
        for i in range(len(listdivs)):
            if (pathFind(listdivs[i],oldy,2)) == True:
                return True,x,y

    if checkVert(x,y) is False:
        #nextDir = Down
        nextDir = 3
        return nextDir,x,y
    elif checkVert(x,y) is True:
        #nextDir = Up
        nextDir = 2
        return nextDir,x,y
    elif checkVert(x,y) is 0:
        if pathFind(x,y,3) == True:
            return True,x,y
        else:
            nextDir = 2
            return nextDir,x,y
    else:
        #Dead end
        nextDir = 4
        return nextDir,x,y
def downSequence(x,y):
    oldx,oldy = x,y
    x,y = drawDown(x, y)
    if y == height - 1:
        return True,x,y
    if (downDivergeRight(oldx,oldy,y)[0]) == True:
        listdivs = downDivergeRight(oldx,oldy,y)[1]
        for i in range(len(listdivs)):
            if (pathFind(oldx,listdivs[i],0)) == True:
                return True,x,y

    if (downDivergeLeft(oldx,oldy,y)[0]) == True:
        listdivs = downDivergeLeft(oldx,oldy,y)[1]
        for i in range(len(listdivs)):
            if (pathFind(oldx,listdivs[i],1)) == True:
                return True,x,y
            
    if checkHor(x,y) is False:
        #nextDir = Right
        nextDir = 0
        return nextDir,x,y
    elif checkHor(x,y) is True:
        #nextDir = Left
        nextDir = 1
        return nextDir,x,y
    elif checkHor(x,y) is 0:
        #Breakpoint
        if pathFind(x,y,0) == True:
            return True,x,y
        else:
            nextDir = 1
            return nextDir,x,y
    else:
        #Dead end
        nextDir = 4
        return nextDir,x,y
def upSequence(x,y):
    oldx,oldy = x,y
    x,y = drawUp(x, y)
    if y == 0:
        return True,x,y
    if (upDivergeRight(oldx,oldy,y)[0]) == True:
        listdivs = upDivergeRight(oldx,oldy,y)[1]
        for i in range(len(listdivs)):
            if (pathFind(oldx,listdivs[i],0)) == True:
                return True,x,y
    if (upDivergeLeft(oldx,oldy,y)[0]) == True:
        listdivs = upDivergeLeft(oldx,oldy,y)[1]
        for i in range(len(listdivs)):
            if (pathFind(oldx,listdivs[i],1)) == True:
                return True,x,y

    if checkHor(x,y) is False:
        #nextDir = Right
        nextDir = 0
        return nextDir,x,y
    elif checkHor(x,y) is True:
        #nextDir = Left
        nextDir = 1
        return nextDir,x,y
    elif checkHor(x,y) is 0:
        #Breakpoint
        if pathFind(x,y,0) == True:
            return True,x,y
        else:
            nextDir = 1
            return nextDir,x,y
    else:
        #Dead end
        nextDir = 4
        return nextDir,x,y


#############################################################################################
    
###Path Diversion Functions

def leftDivergeUp(x,y,newx):
    distance = x - newx
    distance -= (halfspace+(halfspace/3))
    i = 1
    divpoint = 0
    listdivs = []
    ifRounded = 0
    if (maze.getpixel((x-1,y - halfspace - 2)) > 0):
        distance -= (halfspace+(halfspace/2))
        x -= (halfspace+(halfspace/3))
    while((distance - i + 1) > 0):
        r = maze.getpixel((x - i - ifRounded,y - halfspace - 3))
        if r > 0:
            divpoint = x - i - ifRounded + 0 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs
def leftDivergeDown(x,y,newx):
    distance = x - newx
    distance -= (halfspace+(halfspace/4))
    i = 1
    divpoint = 0
    listdivs = []
    if (maze.getpixel((x-1,y + halfspace + 2)) > 0):
        distance -= (halfspace+(halfspace/2))
        x -= (halfspace+(halfspace/3))
    while((distance - i + 1) > 0):
        r = maze.getpixel((x - i,y + halfspace + 2))
        if r > 0:
            divpoint = x - i + 0 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs
        
def rightDivergeUp(x,y,newx):
    distance = newx - x
    i = 1
    divpoint = 0
    distance -= (halfspace+(halfspace/4))
    listdivs = []
    if (maze.getpixel((x+1,y - halfspace - 2)) > 0):
        distance -= (halfspace+(halfspace/2))
        x += (halfspace+(halfspace/3))
    while((distance - i - 1) > 0):
        r = maze.getpixel((x + i,y - halfspace - 2))
        if r > 0:
            divpoint = x + i - 0 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs

def rightDivergeDown(x,y,newx):
    distance = newx - x
    distance -= (halfspace+(halfspace/3))
    i = 1
    divpoint = 0
    listdivs = []
    if (maze.getpixel((x+1,y + halfspace + 2)) > 0):
        distance -= (halfspace+(halfspace/2))
        x += (halfspace+(halfspace/3))
    while((distance - i - 1) > 0):
        r = maze.getpixel((x + i,y + halfspace + 2))
        if r > 0:
            divpoint = x + i - 0 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
        i += 1
    
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs

def downDivergeLeft(x,y,newy):
    distance = newy - y
    i = 1
    divpoint = 0
    distance -= (halfspace+(halfspace/3))
    listdivs = []
    if (maze.getpixel((x - halfspace - 2,y + i)) > 0):
        distance -= (halfspace+(halfspace/2))
        y += (halfspace+(halfspace/3))
    while((distance - i - 1) > 0):
        r = maze.getpixel((x - halfspace - 2,y + i))
        if r > 0:
            divpoint = y + i - 0 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs

def downDivergeRight(x,y,newy):
    distance = newy - y
    i = 1
    divpoint = 0
    distance -= (halfspace+(halfspace/3))
    listdivs = []
    if (maze.getpixel((x + halfspace + 2,y + i)) > 0):
        distance -= (halfspace+(halfspace/2))
        y += (halfspace+(halfspace/3))
    while((distance - i - 1) > 0):
        r = maze.getpixel((x + halfspace + 2,y + i))
        if r > 0:
            divpoint = y + i - 0 + halfspace
            i += pathwidth
            listdivs.append(divpoint)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs

def upDivergeLeft(x,y,newy):
    distance = y - newy
    i = 1
    divpoint = 0
    distance -= (halfspace+(halfspace/3))
    listdivs = []
    if (maze.getpixel((x - halfspace - 2,y - i)) > 0):
        distance -= (halfspace+(halfspace/2))
        y -= (halfspace+(halfspace/3))
    while((distance - i - 1) > 0):
        r = maze.getpixel((x - halfspace - 2,y - i))
        if r > 0:
            divpoint = y - i - 0 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs
    while((distance - i - 1) > 0):
        r = maze.getpixel((x + halfspace + 2,y - i))
        if r > 0:
            divpoint = y - i - 0 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs
def upDivergeRight(x,y,newy):
    distance = y - newy
    i = 1
    divpoint = 0
    distance -= (halfspace+(halfspace/3))
    listdivs = []
    if (maze.getpixel((x + halfspace + 2,y - i)) > 0):
        distance -= (halfspace+(halfspace/2))
        y -= (halfspace+(halfspace/3))
    while((distance - i - 1) > 0):
        r = maze.getpixel((x + halfspace + 2,y - i))
        if r > 0:
            divpoint = y - i - 0 - halfspace
            i += pathwidth
            listdivs.append(divpoint)
        i += 1
    if len(listdivs) > 0:
        return True, listdivs
    else:
        return False, listdivs

#############################################################################################

###Main Path Finder Function
def pathFind(x,y,nextDir):
    #DrawRight = 0, DrawLeft = 1, DrawUp = 2, DrawDown = 3
    global vertexList
    global checkWhenTrue
    global countRecurse
    countTurn = 0
    tempList = [[x,y]]
    vertexList.append([x,y])
    xcheck = 1
    ycheck = 1

    while nextDir is not 5:
        if nextDir == 0:
            #Turn Right
            x = roundUp(x)
            countTurn += 1
            currentDir = nextDir
            nextDir,x,y = rightSequence(x,y)
            xcheck = x
            
            if nextDir is not True:
                tempList.append([x,y])
                vertexList.append([x,y])    
            if xcheck == 0 or xcheck == (width-1):
                countRecurse = 1
                vertexList.append([x,y])
                nextDir = 5
                xcheck = 1
            if nextDir is True:
                nextDir = 5
                if ((countRecurse < 1) and (x is not 0) and (x is not (width-1))):
                    tempList.append([x,y])
                    vertexList.append([x,y])
                    
        elif nextDir == 1:
            #Turn Left
            x = roundDown(x)
            countTurn += 1
            currentDir = nextDir
            oldx,oldy = x,y
            nextDir,x,y = leftSequence(x,y)
            xcheck = x
            
            if nextDir is not True:
                tempList.append([x,y])
                vertexList.append([x,y])    
            if xcheck == 0 or xcheck == (width-1):
                countRecurse = 1
                vertexList.append([x,y])
                nextDir = 5
                xcheck = 1
            if nextDir is True:
                nextDir = 5
                if ((countRecurse < 1) and (x is not 0) and (x is not (width-1))):
                    tempList.append([x,y])
                    vertexList.append([x,y]) 
      
        elif nextDir == 2:
            #Turn Up
            y = roundDown(y)
            countTurn += 1
            currentDir = nextDir
            nextDir,x,y = upSequence(x,y)
            ycheck = y
            if nextDir is not True:
                tempList.append([x,y])
                vertexList.append([x,y])    
            if ycheck == 0 or ycheck == (height-1):
                countRecurse = 1
                vertexList.append([x,y])
                nextDir = 5
                ycheck = 1
            if nextDir is True:
                nextDir = 5
                if ((countRecurse < 1) and (y is not 0) and (y is not (height-1))):
                    tempList.append([x,y])
                    vertexList.append([x,y]) 

        elif nextDir == 3:
            #Turn Down
            y = roundUp(y)
            countTurn += 1
            currentDir = nextDir
            nextDir,x,y = downSequence(x,y)
            ycheck = y
            
            if nextDir is not True:
                tempList.append([x,y])
                vertexList.append([x,y])            
            if ycheck == 0 or ycheck == (height-1):
                countRecurse = 1
                vertexList.append([x,y])
                nextDir = 5
                ycheck = 1
            if nextDir is True:
                nextDir = 5
                if ((countRecurse < 1) and (y is not 0) and (y is not (height-1))):
                    tempList.append([x,y])
                    vertexList.append([x,y]) 
         
        elif nextDir == 4:
            #Dead end
            break
        elif nextDir == 5:
            #Pathway found
            break
        else:
            #Error
            print ("Error.")
    if nextDir == 4:
        #Dead end
        a = 0
        for i in reversed (vertexList):
            if a < len(tempList):
                vertexList.remove(i)
            a += 1
        return False
    elif nextDir == 5:
        #Pathway found
        checkWhenTrue = 1
        return True
    else:
        print ("Error.")


#############################################################################################

def main(filename):
    start_time = time.clock()
    global maze
    try:
        maze = Image.open(filename)
    except FileNotFoundError:
        print("File not found.\n")
        return False
    maze = maze.convert('RGBA')
    maze = ImageEnhance.Brightness(maze).enhance(50.0)
    maze = maze.convert('P')
    global draw
    draw = ImageDraw.Draw(maze)
    global width
    global height
    global count
    width, height = maze.size
    

    checkOutput = checkEntry(filename)

    global whitecount
    whitecount = checkOutput[0]
    if whitecount == 2:
        print("Maze path width size (2px) incompatible.")
        return False

    global startDir
    startDir = checkOutput[1]
    global temp
    temp = checkOutput[2]

    global startpnt
    startpnt = temp - (whitecount/2)
    global pathwidth
    pathwidth = (whitecount)
    global halfspace
    halfspace = (whitecount/2)

    print("\n\n-------------STARTING MAZE SOLVER-------------\n")
    print("                 ...........                 \n")
    
    x = checkOutput[3] 
    y = checkOutput[4]
    
    if (halfspace % 2) is not 0:
        halfspace = halfspace-0.5
    if (startpnt % 2) is not 0:
        startpnt = startpnt+0.5
        
    if (pathFind(x,y,startDir)) == True:
        maze = maze.convert('RGBA')
        draw = ImageDraw.Draw(maze,'RGBA')
        if pathwidth > 4:
            linewidth = pathwidth*0.7
            linewidth = roundUp(linewidth)
        elif pathwidth > 1:
            linewidth = pathwidth/2
            linewidth = roundDown(linewidth)
        else:
            linewidth = 1
        linewidth = int(linewidth)
        for i in range(len(vertexList)-1):
            draw.line((vertexList[i][0],vertexList[i][1]) + (vertexList[i+1][0],vertexList[i+1][1]),fill="firebrick",width=linewidth)
        solvedname = basefilename + ' solved.png'
        maze.save(solvedname, 'PNG')
        print("              Final path found.\n")
        print("-----------------MAZE SOLVED------------------\n")
        x = Decimal(time.clock() - start_time)
        elapsedtime = round(x,2)
        print ("Time elapsed:",elapsedtime,"seconds")
        #print("NCount:",count)
        count = 0
        print("Check file:",solvedname)
        directory = os.path.dirname(os.path.realpath(solvedname))
        directory = directory + "\\" + solvedname
        openfile = input("Open file? (yes = 1/no = 0) ")
        if openfile == '1':
            os.startfile(directory)
    else:
        print("\nError in maze.")


###Main Loop
key = ''
while(key is not 'Q' and key is not 'q'):
    basefilename = input('Enter Maze File Name (no extension/suffix): ')
    filename = basefilename + '.png'
    main(filename)
    resetGlobVars()
    key = input("\nPress any key to enter new file or Q to exit: ")

