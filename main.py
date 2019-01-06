from PIL import Image, ImageColor, ImageDraw, ImageEnhance
from checkentry import checkEntry
from mazefunctions import drawRight,drawLeft,drawDown,drawUp,checkVert,checkHor,rightSequence,leftSequence,downSequence,upSequence,pathFind,leftDivergeUp,leftDivergeDown,rightDivergeUp,rightDivergeDown,downDivergeLeft,downDivergeRight,upDivergeLeft,upDivergeRight
import globvars
import os


def main(filename):
    global maze
    maze = Image.open(filename)
    maze = maze.convert('RGBA')
    maze = ImageEnhance.Brightness(maze).enhance(50.0)
    maze = maze.convert('P')
    global draw
    draw = ImageDraw.Draw(maze)
    global width
    global height
    width, height = maze.size
    
    checkEntry(filename)

    global whitecount
    whitecount = checkEntry(filename)[0]
    global startDir
    startDir = checkEntry(filename)[1]
    global temp
    temp = checkEntry(filename)[2]

    global startpnt
    startpnt = temp - (whitecount/2)
    global pathwidth
    pathwidth = (whitecount)
    global halfspace
    halfspace = (whitecount/2)
    
    x = checkEntry(filename)[3] 
    y = checkEntry(filename)[4]
    
    if (halfspace % 2) is not 0:
        halfspace = halfspace-0.5
    if (startpnt % 2) is not 0:
        startpnt = startpnt+0.5
    
    if (pathFind(x,y,startDir)) == True:
        maze = maze.convert('RGBA')
        draw = ImageDraw.Draw(maze,'RGBA')
        for i in range(len(vertexList)-1):
            draw.line((vertexList[i][0],vertexList[i][1]) + (vertexList[i+1][0],vertexList[i+1][1]),fill="black")
        solvedname = basefilename + ' solved.png'
        maze.save(solvedname, 'PNG')
        print("\nFinal path found.")
        print("-----------------MAZE SOLVED------------------\n")
        print("Check: ",solvedname)
        directory = "C:/Users/User/Documents/Ibrahim/Machine Learning/MazeSolver/" + solvedname
        os.startfile(directory)
    else:
        print("\nError in maze.")

if __name__ == "__main__":  

key = ''
while(key is not 'Q' and key is not 'q'):
    ###Setup
    basefilename = input('Enter Maze File Name (no extension/suffix): ')
    filename = basefilename + '.png'
    print("\n\n-------------STARTING MAZE SOLVER-------------\n")
    print("                 ...........                 \n")
    main(filename)
    key = input("Press Q to exit or any key to continue.")

