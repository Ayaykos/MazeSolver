from PIL import Image, ImageColor, ImageDraw
from checkentry import checkEntry
import sys

filename = 'maze3.png'
maze = Image.open(filename)
pix = maze.load()
width, height = maze.size


whitecount = 0
temp = 0
maxwidth = int(height/5)
minwidth = 1
fullline = 0

checkEntry(filename)

whitecount = checkEntry(filename)[0]
startDir = checkEntry(filename)[1]
temp = checkEntry(filename)[2]

startpnt = temp - (whitecount/2)
pathwidth = (whitecount)
halfspace = (whitecount/2)

print("halfspace:", halfspace, "whitecount:",whitecount, "temp:",temp, "startpnt:",startpnt, "startDir:",startDir)
"""
for i in range(217):
    r = maze.getpixel((40,i))
    print(r)
"""
r = maze.getpixel((472, 420.5))
print(r)
