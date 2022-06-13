# The main file, __init__.py
# This file runs the entire game

# In this directory, we have a file called player.py, a file called cp.py,
# a file called pong.py, a file called chi.py, a file called win.py,
# and 2 files startScreen.py and helpScreen.py which are the graphics for
# the start and instruction page. There are also 2 folders,
# tiles and tilesSmall, which have the images for the UI.

##############################################################################

from tkinter import *
import copy
import math
import random
import string
from startScreen import *
from helpScreen import *
from pong import *
from chi import *
from win import *
from player import *
from cp import *

def init(data):
    data.mode = "start screen"
    data.mahjong = PhotoImage(file='start.gif')
    data.help1 = PhotoImage(file='helpScreen1.gif')
    data.help2 = PhotoImage(file='helpScreen2.gif')
    data.tileWidth,data.tileHeight = 35,50
    data.tiles = ['wan1','wan2','wan3','wan4','wan5','wan6','wan7','wan8','wan9',\
    'tong1','tong2','tong3','tong4','tong5','tong6','tong7','tong8','tong9',\
    'bam1','bam2','bam3','bam4','bam5','bam6','bam7','bam8','bam9',\
    'east','south','west','north','red','green','blank']
    data.tileImages = loadTileImages(data)
    data.smallTileImages = loadSmall(data)

    data.playerHand = getTiles(data)[0]
    data.player = True
    data.playerPong,data.playerChi = [],[]
    data.p1Pong,data.p1Chi = False,False
    data.playerDec = False

    data.cp1,data.cp2,data.cp3 = False,False,False
    data.cp1Hand = getTiles(data)[1]
    data.cp2Hand = getTiles(data)[2]
    data.cp3Hand = getTiles(data)[3]

    data.cp1Complete = compIncSets(data.cp1Hand)[0]
    data.cp1Inc = compIncSets(data.cp1Hand)[1]
    data.cp1Almost = compIncSets(data.cp1Hand)[2]
    data.cp2Almost = compIncSets(data.cp2Hand)[2]
    data.cp3Almost = compIncSets(data.cp3Hand)[2]
    data.cp2Complete = compIncSets(data.cp2Hand)[0]
    data.cp2Inc = compIncSets(data.cp2Hand)[1]
    data.cp3Complete = compIncSets(data.cp3Hand)[0]
    data.cp3Inc = compIncSets(data.cp3Hand)[1]

    data.pong1,data.chi1 = False,False
    data.pong2,data.chi2 = False,False
    data.pong3,data.chi3 = False,False
    data.cp1Pong,data.cp1Chi = [],[]
    data.cp2Pong,data.cp2Chi = [],[]
    data.cp3Pong,data.cp3Chi = [],[]
    data.discarded = []
    data.throw = 'None'
    data.alreadyP = False
    data.already1 = False
    data.already2 = False
    data.already3 = False
    data.nextPlayer = None

    data.time = 0
    data.draw = False
    data.winP,data.win1,data.win2,data.win3 = False,False,False,False
    data.winPHand,data.win1Hand,data.win2Hand,data.win3Hand = [],[],[],[]

def loadTileImages(data):
    images = []
    for tile in data.tiles:
        filename = 'tiles/' + tile + '.gif'
        images.append(PhotoImage(file=filename))
    return images

def loadSmall(data):
    pics = []
    for tile in data.tiles:
        filename = 'tilesSmall/' + tile + '.gif'
        pics.append(PhotoImage(file=filename))
    return pics

def mousePressed(event,data):
    if data.mode == 'start screen':
        startScreenMousePressed(event,data)
    elif data.mode == 'help screen':
        helpScreenMousePressed(event,data)
    elif data.mode == 'play game':
        if data.draw == False:
            if len(data.allTiles) > 0:
                playerMousePressed(event,data)
            else:
                data.draw = True

def keyPressed(event,data):
    if data.mode == 'play game':
        if data.draw == False:
            if data.winP == False and data.win1 == False and data.win2 == False \
            and data.win3 == False:
                if len(data.allTiles) > 0:
                    playerKeyPressed(event,data)
                else:
                    data.draw = True
        if event.keysym == 'r':
            init(data)

def timerFired(data):
    if data.mode == 'play game':
        data.time += 1
        if data.draw == False:
            if data.winP == False and data.win1 == False and data.win2 == False \
            and data.win3 == False:
                if data.p1Pong == False and data.p1Chi == False:
                    playerOnTimerFired(data)
                    if (data.time) % 20 == 0:
                        cp1OnTimerFired(data)
                    elif (data.time) % 25 == 0:
                        cp2OnTimerFired(data)
                    elif (data.time) % 30 == 0:
                        cp3OnTimerFired(data)
                    if playerWin(data,data.throw):
                        data.winPHand = data.playerHand+data.playerPong+data.playerChi+[data.throw]
                        data.winP = True
                elif data.p1Chi == False or data.p1Pong == False:
                    cp1OnTimerFired(data)
                    cp2OnTimerFired(data)
                    cp3OnTimerFired(data)
        if len(data.allTiles) == 0:
            data.draw = True

def getSmallTile(data,i):
    return data.smallTileImages[i]

def drawDiscarded(canvas,data):
    discardTileW = 15
    discardTileH = 25
    for i in range(len(data.discarded)):
        x0 = 165 + discardTileW*(i%18)
        y0 = 125 + discardTileH*(i//18)
        x1 = x0 + discardTileW
        y1 = y0 + discardTileH
        index = data.tiles.index(data.discarded[i])
        image = getSmallTile(data,index)
        canvas.create_image((x0+x1)//2,(y0+y1)//2,image=image)

def drawCenterTiles(canvas,data):
    tileWidth = 15
    tileHeight = 25
    for i in range(18):
        x0 = data.width/3.6 + tileWidth*i
        y0 = data.height*3//20 + tileHeight
        x1 = x0 + tileWidth
        y1 = y0 + tileHeight
        canvas.create_rectangle(x0,y0,x1,y1,fill='darkgreen')
    for j in range(18):
        x2 = data.width/3.6 - tileHeight
        y2 = data.height*3//20 + tileHeight + tileWidth*j
        x3 = x2 + tileHeight
        y3 = y2 + tileWidth
        canvas.create_rectangle(x2,y2,x3,y3,fill='darkgreen')
    for k in range(18):
        x4 = data.width/3.6 + tileWidth*k
        y4 = data.height*3//20 + 18*tileWidth
        x5 = x4 + tileWidth
        y5 = y4 + tileHeight
        canvas.create_rectangle(x4,y4,x5,y5,fill='darkgreen')
    for l in range(18):
        x6 = data.width/3.6 + 18*tileWidth
        y6 = data.height*3//20 + tileHeight + tileWidth*l
        x7 = x6 + tileHeight
        y7 = y6 + tileWidth
        canvas.create_rectangle(x6,y6,x7,y7,fill='darkgreen')

def drawCPTiles(canvas,data):
    tileWidth = 15
    tileHeight = 25
    for i in range(len(data.cp2Hand)):
        x0 = data.width/3.6 + 2.5*tileWidth + tileWidth*i
        y0 = data.height//10
        x1 = x0 + tileWidth
        y1 = y0 + tileHeight
        canvas.create_rectangle(x0,y0,x1,y1,fill='darkgreen')
    for j in range(len(data.cp3Hand)):
        x2 = data.width/3.6 - 3*tileHeight
        y2 = data.height*3//20 + 2.5*tileHeight + tileWidth*j
        x3 = x2 + tileHeight
        y3 = y2 + tileWidth
        canvas.create_rectangle(x2,y2,x3,y3,fill='darkgreen')
    for k in range(len(data.cp1Hand)):
        x4 = data.width/3.6 + 18*tileWidth + 2*tileHeight
        y4 = data.height*3//20 + 2.5*tileHeight + tileWidth*k
        x5 = x4 + tileHeight
        y5 = y4 + tileWidth
        canvas.create_rectangle(x4,y4,x5,y5,fill='darkgreen')

def redrawAll(canvas,data):
    if data.mode == 'start screen':
        startScreenRedrawAll(canvas,data)
    elif data.mode == 'help screen':
        helpScreenRedrawAll(canvas,data)
    elif data.mode == 'play game':
        if data.draw == False:
            canvas.create_rectangle(0,0,data.width,data.height,fill='lime green')
            drawCenterTiles(canvas,data)
            drawCPTiles(canvas,data)
            drawPlayer(canvas,data)
            drawDiscarded(canvas,data)
            pongRedrawAll(canvas,data)
            chiRedrawAll(canvas,data)
            cpRedrawAll(canvas,data)
            if data.winP == True or data.win1 == True or data.win2 == True \
            or data.win3 == True:
                winRedrawAll(canvas,data)
            elif data.cp1:
                cp1RedrawAll(canvas,data)
            elif data.cp2:
                cp2RedrawAll(canvas,data)
            elif data.cp3:
                cp3RedrawAll(canvas,data)
        elif data.draw == True:
            canvas.create_rectangle(0,0,data.width,data.height,fill='lime green')
            drawCenterTiles(canvas,data)
            drawCPTiles(canvas,data)
            canvas.create_text(data.width//2,data.height//2,text="DRAW",\
            font="BrushScriptMT 20", fill = "white")

################
#Run Function
#Taken from 15-112 Class Notes on Animation - Time Based Animations in Tkinter
################
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

    print("bye!")

run(600,500)

##############################################################################
# Citation for images:
# start screen- http://www.chinese-word.com/data/7241-3.html
# help screen- http://mcgillmahjong.blogspot.com/p/hong-kong-old-style-our-rules.html
# tiles- https://www.istockphoto.com/illustrations/mahjong-tiles?assettype=image&sort=mostpopular&mediatype=illustration&family=creative&phrase=mahjong%20tiles

#Citation for Tkinter colors:
#http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
##############################################################################