from PIL import Image, ImageColor, ImageDraw, ImageEnhance
import sys

def checkEntry(filename):
    x = 0
    y = 0    
    maze = Image.open(filename)
    maze = maze.convert('RGBA')
    maze = ImageEnhance.Brightness(maze).enhance(50.0)
    maze = maze.convert('P')
    width, height = maze.size
    draw = ImageDraw.Draw(maze)

    ###Global vars
    whitecount = 0
    temp = 0
    maxwidth = int(height/5)
    minwidth = 1
    fullline = 0


    ###Get startpnt, pathwidth
    #Right = 0, Left = 1, Up = 2, Down = 3 ? recheck

    #top
    for i in range(width-1):
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
        for i in range(height-1):
            r = maze.getpixel((width-1,i))
            #print ("get pixel, a: ", a, maze.getpixel((0,a)))
            if r > 0:
                whitecount += 1
                temp = i
                #print("width-1,i+1",width-1,i+1)
                r = maze.getpixel((width-1,i+1))
                if r == 0:
                    #print("broken")
                    break
        #print("---------------------")
        if whitecount == 0:
            #print ("check next side")
            #bottom
            for i in range(width-1):
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
                for i in range(height-1):
                    r = maze.getpixel((0,i))
                    #print ("get pixel, a: ", a, maze.getpixel((0,a)))
                    if r > 0:
                        whitecount += 1
                        temp = i
                        #print(r)
                        r = maze.getpixel((0,i+1))
                        if r == 0:
                            #print("broken")
                            startDir = 0
                            startpnt = temp - (whitecount/2)
                            y = startpnt
                            break
                if whitecount == 0:
                    startDir = 4
            else:
                startDir = 2
                startpnt = temp - (whitecount/2)
                x = startpnt
                y = height - 1
        else:
            startDir = 1
            startpnt = temp - (whitecount/2)
            x = width - 1
            y = startpnt
    else:
        startDir = 3
        startpnt = temp - (whitecount/2)
        x = startpnt

    if (x % 2) is not 0:
        x = x+0.5
    if (y % 2) is not 0:
        y = y+0.5
    return whitecount, startDir, temp, x, y

