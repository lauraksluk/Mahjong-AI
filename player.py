# This file, player.py initializes all the players' tiles and controls the
# user's mouse/key presses. It also draws the user's tiles and pongs/chis.

##############################################################################

from tkinter import *
import random
from pong import *
from chi import *
from win import *

def init(data):
    data.tileWidth = 35
    data.tileHeight = 50

def getTiles(data):
    data.allTiles = ['wan1','wan2','wan3','wan4','wan5','wan6','wan7','wan8','wan9',\
    'tong1','tong2','tong3','tong4','tong5','tong6','tong7','tong8','tong9',\
    'bam1','bam2','bam3','bam4','bam5','bam6','bam7','bam8','bam9',\
    'east','south','west','north','red','green','blank',\
    'wan1','wan2','wan3','wan4','wan5','wan6','wan7','wan8','wan9',\
    'tong1','tong2','tong3','tong4','tong5','tong6','tong7','tong8','tong9',\
    'bam1','bam2','bam3','bam4','bam5','bam6','bam7','bam8','bam9',\
    'east','south','west','north','red','green','blank',\
    'wan1','wan2','wan3','wan4','wan5','wan6','wan7','wan8','wan9',\
    'tong1','tong2','tong3','tong4','tong5','tong6','tong7','tong8','tong9',\
    'bam1','bam2','bam3','bam4','bam5','bam6','bam7','bam8','bam9',\
    'east','south','west','north','red','green','blank',\
    'wan1','wan2','wan3','wan4','wan5','wan6','wan7','wan8','wan9',\
    'tong1','tong2','tong3','tong4','tong5','tong6','tong7','tong8','tong9',\
    'bam1','bam2','bam3','bam4','bam5','bam6','bam7','bam8','bam9',\
    'east','south','west','north','red','green','blank']
    player = []
    for i in range(14):
        cardP = random.choice(data.allTiles)
        player.append(cardP)
        data.allTiles.remove(cardP)
    player = orderHand(player)
    if None in player:
        player.remove(None)
    cp1 = []
    for j in range(13):
        card1 = random.choice(data.allTiles)
        cp1.append(card1)
        data.allTiles.remove(card1)
    cp1 = orderHand(cp1)
    if None in cp1:
        cp1.remove(None)
    cp2 = []
    for k in range(13):
        card2 = random.choice(data.allTiles)
        cp2.append(card2)
        data.allTiles.remove(card2)
    cp2 = orderHand(cp2)
    if None in cp2:
        cp2.remove(None)
    cp3 = []
    for l in range(13):
        card3 = random.choice(data.allTiles)
        cp3.append(card3)
        data.allTiles.remove(card3)
    cp3 = orderHand(cp3)
    if None in cp3:
        cp3.remove(None)
    return [player,cp1,cp2,cp3]

def orderHand(L):
    L1,L2,L3,L4 = [],[],[],[]
    for tile in L:
        if 'wan' in tile:
            L1.append(tile)
            L1.sort()
        elif 'bam' in tile:
            L2.append(tile)
            L2.sort()
        elif 'tong' in tile:
            L3.append(tile)
            L3.sort()
        else:
            L4.append(tile)
            L4.sort()
    result = L1+L2+L3+L4
    return result

def getNewTile(data):
    tile = random.choice(data.allTiles)
    return tile

def playerThrow(event,data):
    if 425 < event.y < 425 + data.tileHeight:
        data.p1Pong = False
        data.p1Chi = False
        data.tileNum = (event.x - 60) // data.tileWidth
        data.throw = data.playerHand.pop(data.tileNum)
        data.discarded.append(data.throw)
        data.nextPlayer = "cp1"
        data.playerDec = False
        data.player = False
        data.cp1 = True
        data.already3 = False

def playerMousePressed(event, data):
    if data.p1Pong == True and data.playerDec == False:
        data.p1Pong = False
        data.cp1,data.cp2,data.cp3 = False,False,False
        TileNum1 = (event.x - 60) // data.tileWidth
        data.playerPong.append(data.playerHand.pop(TileNum1))
        data.playerPong.append(data.discarded.pop())
        data.playerPong.append(data.playerHand.pop(TileNum1))
        data.pong1,data.pong2,data.pong3 = False,False,False
        data.chi1,data.chi2,data.chi3 = False,False,False
        data.alreadyP = True
        data.player = True
    elif data.p1Chi == True and data.playerDec == False:
        data.p1Chi = False
        data.cp1,data.cp2,data.cp3 = False,False,False
        TileNum1 = (event.x - 60) // data.tileWidth
        data.playerChi.append(data.playerHand.pop(TileNum1))
        data.playerChi.append(data.discarded.pop())
        data.playerChi.append(data.playerHand.pop(TileNum1))
        data.playerChi = orderHand(data.playerChi)
        data.pong1,data.pong2,data.pong3 = False,False,False
        data.chi1,data.chi2,data.chi3 = False,False,False
        data.alreadyP = True
        data.player = True
    elif data.player:
        playerThrow(event,data)

def playerKeyPressed(event, data):
    if data.p1Pong:
        if event.keysym == 'space':
            data.playerDec = True
            data.p1Pong = False
    elif data.p1Chi:
        if event.keysym == 'space':
            data.playerDec = True
            data.p1Chi = False

def playerOnTimerFired(data):
    if data.player == True and data.pong1 == False and data.chi1 == False \
    and data.pong2 == False and data.chi2 == False and data.pong3 == False \
    and data.chi3 == False:
        if len(data.playerHand) == 13-len(data.playerPong)-len(data.playerChi):
            newTile = getNewTile(data)
            if playerWin(data,newTile):
                data.winPHand = data.playerHand+data.playerPong+data.playerChi+[newTile]
                data.winP = True
            data.playerHand.append(newTile)
            data.allTiles.remove(newTile)
            data.playerHand = orderHand(data.playerHand)

def playerWin(data,tile):
    hand = data.playerHand + data.playerPong + data.playerChi
    return isWin(hand,tile)

def getTileImage(data,i):
    return data.tileImages[i]

def getSmallTile(data,i):
    return data.smallTileImages[i]

def drawPlayer(canvas,data):
    tileWidth = 35
    tileHeight = 50
    for i in range(len(data.playerHand)):
        ind0 = data.tiles.index(data.playerHand[i])
        image = getTileImage(data,ind0)
        x0 = 60 + tileWidth*i
        y0 = 440
        x1 = x0 + tileWidth
        y1 = y0 + tileHeight
        x,y = (x0+x1)//2,(y0+y1)//2
        canvas.create_image(x,y,image=image)
    smallW = 15
    smallH = 25
    for j in range(len(data.playerPong)):
        ind1 = data.tiles.index(data.playerPong[j])
        img = getSmallTile(data,ind1)
        px0 = 170 + smallW*j
        py0 = 375
        px1 = px0 + smallW
        py1 = py0 + smallH
        px,py = (px0+px1)//2,(py0+py1)//2
        canvas.create_image(px,py,image=img)
    for k in range(len(data.playerChi)):
        ind2 = data.tiles.index(data.playerChi[k])
        img1 = getSmallTile(data,ind2)
        cx0 = 170 + smallW*k
        cy0 = 400
        cx1 = cx0 + smallW
        cy1 = cy0 + smallH
        cx,cy = (cx0+cx1)//2,(cy0+cy1)//2
        canvas.create_image(cx,cy,image=img1)

