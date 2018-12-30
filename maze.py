from PIL import Image, ImageColor, ImageDraw
import sys

#def checkUp(x,y):
    

#print(ImageColor.getcolor('red', 'RGBA'))
maze = Image.open('maze1.png')
print(maze.size)

width, height = maze.size
print(width)
print(height)

draw = ImageDraw.Draw(maze)

#mazecolor = Image.new('RGB', (100, 100))
print(maze.getpixel((0, 0)))
print("----")
#print(maze.getpixel((0, 0)))

b = 0
temp = 0
maxwidth = int(height/5)
minwidth = 1

for a in range(height):
    if (maze.getpixel((0, a))) > 0:
        b += 1
        temp = a
startpnt = int(temp - (b/2))
actualwidth = int(b)
halfspace = (b/2)
#print(maze.getpixel((0, startpnt)))
#print(maxwidth)

draw.line((0, startpnt) + ((minwidth),startpnt),fill=10)

fullline = 0

for i in range(width):
    if (maze.getpixel((i+minwidth, startpnt)) > 0):
        fullline = i
    else:
        draw.line((minwidth, startpnt) + ((fullline - halfspace),startpnt),fill=10)
        break


draw = ImageDraw.Draw(maze)
#draw.line((0, 0) + (200,200), fill='yellow')
#draw.line((0, maze.size[1], maze.size[0], 0), fill=128)
#for a in range(150):
    #draw.line((0, a) + (218,a), fill=10)



maze.save('maze1.png', 'PNG')
