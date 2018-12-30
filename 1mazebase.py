from PIL import Image, ImageColor, ImageDraw
from checkentry import checkEntry
import sys


###Setup
#print(ImageColor.getcolor('red', 'RGBA'))
basefilename = input('Enter Maze File Name (no extension/suffix): ')
filename = basefilename + '.png'
#filename = 'test1.png'
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


print("-------------STARTING MAZE SOLVER-------------")
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
"""
for a in range(height):
    r, = maze.getpixel((0,a))
    #print ("get pixel, a: ", a, maze.getpixel((0,a)))
    if (r) > 0:
        whitecount += 1
        temp = a
        startDir = 0

        r, = maze.getpixel((0,a+1))
        if r == 0:
            #print ("BROKEN LOOP")
            break
if (whitecount == 0):
    for i in range(width):
        r, = maze.getpixel((i,0))
        #print ("get pixel, a: ", a, maze.getpixel((0,a)))
        if (r) > 0:
            whitecount += 1
            temp = a
            startDir = 1
            r, = maze.getpixel((i+1,0))
            if r == 0:
                #print ("BROKEN LOOP")
                break

"""
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
    if (z == 1):
        #print (r, "Turn Down")
        return False
        #return ("Turn Down")
    else:
        #print(x,y)
        #print(r, "Turn Up")
        return True
        #return ("Turn Up")

def checkHor(x,y):
    #print ("GOOD SO FAR")
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
    if (z == 1):
        #print (r, "Turn Right")
        #print("\n------\n")
        return False
        #return ("Turn Right")
    else:
        #print (r, "Turn Left")
        return True
        #return ("Turn Left")

"""
###Instructions
drawRight(0, startpnt)
x,y = drawRight(0, startpnt)
#x = int(x)
#y = int(y)
print("checking vert from right: ", x,y)
print(checkVert(x,y))
drawDown(x,y)
x,y = drawDown(x, y)
print("checking hor from down: ", x,y)
print(checkHor(x,y))
drawLeft(x,y)
x,y = drawLeft(x, y)
print("checking vert from left: ", x,y)
print(checkVert(x,y))
drawDown(x,y)
x,y = drawDown(x, y)
print("checking hor from down: ", x,y)
print(checkHor(x,y))
drawRight(x,y)
x,y = drawRight(x, y)
print("checking vert from right: ", x,y)
print(checkVert(x,y))
drawUp(x,y)
x,y = drawUp(x, y)
print("checking hor from up: ", x,y)
#print(checkHor(x,y))
drawRight(x,y)
print("checking vert from right: ", x,y)
print(checkVert(x,y))
"""
def rightSequence(x,y):
    drawRight(x,y)
    x,y = drawRight(x, y)
    #print("->entered right seq")
    if checkVert(x,y) == False:
        nextDir = 3
        return nextDir
    else:
        nextDir = 2
        return nextDir
def leftSequence(x,y):
    drawLeft(x,y)
    x,y = drawLeft(x, y)
    if checkVert(x,y) == False:
        #print ("nextDir = Down")
        nextDir = 3
        return nextDir
    else:
        #print ("nextDir = Up")
        nextDir = 2
        return nextDir
def downSequence(x,y):
    #print('x,y downSeq',x,y)
    drawDown(x,y)
    x,y = drawDown(x, y)
    #print('x,y afterdownSeq',x,y)
    #print ("HEREREREREREERE", x,y)
    if checkHor(x,y) == False:
        #print ("nextDir = Right")
        nextDir = 0
        return nextDir
    else:
        #print ("nextDir = Left")
        nextDir = 1
        return nextDir
def upSequence(x,y):
    drawUp(x,y)
    x,y = drawUp(x, y)
    #print ("HEREREREREREERE", x,y)
    if checkHor(x,y) == False:
        #print ("nextDir = Right")
        nextDir = 0
        return nextDir
    else:
        #print ("nextDir = Left")
        nextDir = 1
        return nextDir

###Check entry point
x = checkEntry(filename)[3]
y = checkEntry(filename)[4]
xcheck = 1
ycheck = 1

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
    



#Right = 0, Left = 1, Up = 2, Down = 3
#DrawRight = 0, DrawLeft = 1, DrawUp = 2, DrawDown = 3

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


maze.save(basefilename + 'solved.png', 'PNG')

print("-----------------MAZE SOLVED------------------")
