from PIL import Image, ImageColor, ImageDraw, ImageEnhance
import sys
#from mazefunctions import checkFile


def checkEntry(filename):
    x = 0
    y = 0
    #checkFile(filename)
    
    maze = Image.open(filename)
    maze = maze.convert('P') # conversion to RGB
    #maze = maze.load()
    ###Setup
    #maze = Image.open(filename)
    #print("Maze size: ", maze.size)

    width, height = maze.size
    #print("Maze width: ", width)
    #print("Maze height: ", height)

    draw = ImageDraw.Draw(maze)

    ###Global vars
    whitecount = 0
    temp = 0
    maxwidth = int(height/5)
    minwidth = 1
    fullline = 0

    #r = maze.getpixel((110,0))
    #print ("this is r: ", r)


    ###Get startpnt, pathwidth
    #Right = 0, Left = 1, Up = 2, Down = 3

    #top
    for i in range(width):
        r = maze.getpixel((i,0))
        #print ("get pixel, a: ", a, maze.getpixel((0,a)))
        if r > 0:
            whitecount += 1
            temp = i
            #print(r)
            r = maze.getpixel((i+1,0))
            if r == 0:
                #print("broken")
                break
    #print("---------------------")
    if whitecount == 0:
        #print ("check next side")
        #right
        for i in range(height):
            r = maze.getpixel((width-1,i))
            #print ("get pixel, a: ", a, maze.getpixel((0,a)))
            if r > 0:
                whitecount += 1
                temp = i
                #print(r)
                r = maze.getpixel((width-1,i+1))
                if r == 0:
                    #print("broken")
                    break
        #print("---------------------")
        if whitecount == 0:
            #print ("check next side")
            #bottom
            for i in range(width):
                r = maze.getpixel((i,height-1))
                #print ("get pixel, a: ", a, maze.getpixel((0,a)))
                if r > 0:
                    whitecount += 1
                    temp = i
                    #print(r)
                    r = maze.getpixel((i+1,height-1))
                    if r == 0:
                        #print("broken")
                        break
            if whitecount == 0:
                #print ("check next side")
                #left
                for i in range(height):
                    r = maze.getpixel((0,i))
                    #print ("get pixel, a: ", a, maze.getpixel((0,a)))
                    if r > 0:
                        whitecount += 1
                        temp = i
                        #print(r)
                        r = maze.getpixel((0,i+1))
                        if r == 0:
                            #print("broken")
                            startDir = 1
                            startpnt = temp - (whitecount/2)
                            y = startpnt
                            break
                if whitecount == 0:
                    startDir = 4
            else:
                startDir = 3
                startpnt = temp - (whitecount/2)
                x = startpnt
                y = height - 1
        else:
            startDir = 0
            startpnt = temp - (whitecount/2)
            x = width - 1
            y = startpnt
    else:
        startDir = 2
        startpnt = temp - (whitecount/2)
        x = startpnt

    if (x % 2) is not 0:
        x = x+0.5
    if (y % 2) is not 0:
        y = y+0.5
    return whitecount, startDir, temp, x, y

"""
checkEntry('entry.png')

whitecount = checkEntry('entry.png')[0]
startDir = checkEntry('entry.png')[1]
temp = checkEntry('entry.png')[2]
x = checkEntry('entry.png')[3]
y = checkEntry('entry.png')[4]

startpnt = temp - (whitecount/2)
pathwidth = (whitecount)
halfspace = (whitecount/2)     
print("---------------------", "whitecount: ", whitecount, "startDir: ", startDir, "startpnt: ", startpnt, "x,y: ", x, y)

#right
for i in range(height):
    r = maze.getpixel((width-1,i))
    #print ("get pixel, a: ", a, maze.getpixel((0,a)))
    if r > 0:
        #whitecount += 1
        #temp = a
        print(r)
print("---------------------")
#bottom
for i in range(width):
    r = maze.getpixel((i,height-1))
    #print ("get pixel, a: ", a, maze.getpixel((0,a)))
    if r > 0:
        #whitecount += 1
        #temp = a
        print(r)
print("---------------------")





#print("halfspace: ", halfspace, "whitecount: ",whitecount, "temp: ",temp, "startpnt: ",startpnt, "startDir: ",startDir)


###Main loop
x = 0
y = startpnt
xcheck = 1
ycheck = 1
nextDir = 0
#Right = 0, Left = 1, Up = 2, Down = 3


#maze.save('maze1.png', 'PNG')
"""
