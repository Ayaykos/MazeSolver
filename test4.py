from PIL import Image, ImageColor, ImageDraw
import sys


###Setup
#print(ImageColor.getcolor('red', 'RGBA'))
#basefilename = input('Enter Maze File Name (no extension/suffix): ')
#filename = basefilename + '.png'
filename = 'maze1 backup.png'
maze = Image.open(filename)
maze = maze.convert('1') # conversion
#maze = maze.load()
#maze.save(basefilename + 'solvedbw.png', 'PNG')

draw = ImageDraw.Draw(maze)
pix = maze.load()
#print("Maze size: ", maze.size)

width, height = maze.size
#print("Maze width: ", width)
#print("Maze height: ", height)

print(maze.getbands())
print(maze.getpixel((1,1)))

draw.line((1,1) + (217,217),fill=1)

maze.save('maze1 backup solved.png', 'PNG')
