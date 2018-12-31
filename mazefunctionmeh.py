from PIL import Image, ImageColor, ImageDraw
from checkentry import checkEntry
from mazebase import pathFind
import sys


###Setup
#print(ImageColor.getcolor('red', 'RGBA'))
#basefilename = input('Enter Maze File Name (no extension/suffix): ')
filename = 'line.png'
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

print("pathwidth:", pathwidth, "halfspace:", halfspace, "whitecount:",whitecount, "temp:",temp, "startpnt:",startpnt, "startDir:",startDir)

x = 218
y = 109
newx = 130


def leftPathDiverge(x,y,newx):
    width = 0
    distance = x - newx
    i = 1
    divpoint = 0
    listdivs = []
    print(distance)
    while((218 - i + 1) is not 0):
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
        #pathFind(listdivs[i],y,2)
        print('listdiv[i]:',listdivs[i])
        
leftPathDiverge(x,y,newx)
"""
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
"""

