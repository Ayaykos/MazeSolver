from PIL import Image, ImageColor, ImageDraw, ImageEnhance
import sys


###Setup
maze = Image.open('test1.png')
draw = ImageDraw.Draw(maze)
"""
if maze.mode == 'RGBA':
    r, g, b = maze.getpixel((200,1))
    print (r)
else:
    r = maze.getpixel((200,1))
    print(r)

#maze = maze.convert('1') # convert image to black and white
#scale_value = scale1.get()
#maze = ImageEnhance.Brightness(maze).enhance(50.0)
"""
r, g, b = maze.getpixel((1,0))
print (r,g,b)
#maze = ImageEnhance.Brightness(maze).enhance(50.0)
maze = maze.convert('1')
r = maze.getpixel((1,0))
print(r)
r, g, b = maze.getpixel((1,0))

maze.save('result.png')
#r, g, b, = maze.getpixel((200,1))
#print(r,g,b)

"""
im = Image.open("sample1.png")
enhancer = ImageEnhance.Contrast(im)
enhanced_im = enhancer.enhance(50.0)
enhanced_im = enhanced_im.convert('1')
enhanced_im = ImageEnhance.Contrast(enhanced_im).enhance(50.0)
enhanced_im.save("enhanced.sample1.png")
"""
