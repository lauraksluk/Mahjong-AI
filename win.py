# This file, win.py, defines the functions to determine if each player's
# current hand is a winning one. It draws the game over/winning message and
# the winning hand's tiles.
# A winning hand is defined to be 1 pair of 2 identical tiles and
# 4 sets of 3 (pong's or chi's).

##############################################################################

import copy

def groupSets(L):
    wanGroup, tongGroup, bambooGroup, wordGroup = [],[],[],[]
    for tile in L:
        if 'wan' in tile:
            wanGroup.append(tile)
        elif 'tong' in tile:
            tongGroup.append(tile)
        elif 'bam' in tile:
            bambooGroup.append(tile)
        else:
            wordGroup.append(tile)
    wanGroup.sort(),tongGroup.sort(),bambooGroup.sort(),wordGroup.sort()
    return wanGroup,tongGroup,bambooGroup,wordGroup

def isWin(L,tile):
    tempL = copy.deepcopy(L)
    tempL.append(tile)
    wanHand,tongHand,bambooHand,wordHand = groupSets(tempL)
    currHand = wanHand + tongHand + bambooHand + wordHand
    return winBacktracking(currHand)

def isComplete(currHand):
    if len(currHand) == 2:
        if currHand[0] == currHand[1]:
            return True
        else:
            return False
    else:
        return False

def winBacktracking(L):
    if isComplete(L):
        return True
    else:
        for i in range(len(L)):
            currTile = L[i]
            if currTile[-1].isdigit() and (currTile[:-1]+str(int(currTile[-1])+1)) \
            in L and (currTile[:-1]+str(int(currTile[-1])+2)) in L:
                consecInd = L.index(currTile[:-1]+str(int(currTile[-1])+1))
                nextConsecInd = L.index(currTile[:-1]+str(int(currTile[-1])+2))
                L.pop(i)
                L.pop(consecInd-1)
                L.pop(nextConsecInd-2)
                tmpSol = winBacktracking(L)
                if tmpSol:
                    return tmpSol
                L.insert(i,currTile)
                L.insert(consecInd,(currTile[:-1]+str(int(currTile[-1])+1)))
                L.insert(nextConsecInd,(currTile[:-1]+str(int(currTile[-1])+2)))
            elif i <= (len(L)-3) and currTile == L[i+1] and currTile == L[i+2]:
                L.pop(i)
                L.pop(i)
                L.pop(i)
                tmpSol = winBacktracking(L)
                if tmpSol:
                    return tmpSol
                L.insert(i,currTile)
                L.insert(i+1,currTile)
                L.insert(i+2,currTile)
        return False

def getSmallTile(data,i):
    return data.smallTileImages[i]

def winRedrawAll(canvas,data):
    smallW = 15
    smallH = 25
    if data.win3:
        canvas.create_rectangle(180,200,420,300,fill='black')
        canvas.create_text(300,225,text="CP3 WON!",font = "BrushScriptMT 20", fill = "white")
        L1,L2,L3,L4 = groupSets(data.win3Hand)
        data.win3Hand = L1 + L2 + L3 + L4
        for i in range(len(data.win3Hand)):
            ind0 = data.tiles.index(data.win3Hand[i])
            img0 = getSmallTile(data,ind0)
            x0 = 195 + smallW*i
            y0 = 265
            x1 = x0 + smallW
            y1 = y0 + smallH
            xw3,yw3 = (x0+x1)//2,(y0+y1)//2
            canvas.create_image(xw3,yw3,image=img0)
    elif data.winP:
        canvas.create_rectangle(180,200,420,300,fill='black')
        canvas.create_text(300,225,text="YOU WON!", font = "BrushScriptMT 20", fill = "white")
        L5,L6,L7,L8 = groupSets(data.winPHand)
        data.winPHand = L5 + L6 + L7 + L8
        for j in range(len(data.winPHand)):
            ind1 = data.tiles.index(data.winPHand[j])
            img1 = getSmallTile(data,ind1)
            x2 = 195 + smallW*j
            y2 = 265
            x3 = x2 + smallW
            y3 = y2 + smallH
            xwp,ywp = (x2+x3)//2,(y2+y3)//2
            canvas.create_image(xwp,ywp,image=img1)
    elif data.win2:
        canvas.create_rectangle(180,200,420,300,fill='black')
        canvas.create_text(300,225,text="CP2 WON!", font = "BrushScriptMT 20", fill = "white")
        L9,L10,L11,L12 = groupSets(data.win2Hand)
        data.win2Hand = L9 + L10 + L11 + L12
        for k in range(len(data.win2Hand)):
            ind2 = data.tiles.index(data.win2Hand[k])
            img2 = getSmallTile(data,ind2)
            x4 = 195 + smallW*k
            y4 = 265
            x5 = x4 + smallW
            y5 = y4 + smallH
            xw2,yw2 = (x4+x5)//2,(y4+y5)//2
            canvas.create_image(xw2,yw2,image=img2)
    elif data.win1:
        canvas.create_rectangle(180,200,420,300,fill='black')
        canvas.create_text(300,225,text="CP1 WON!", font = "BrushScriptMT 20", fill = "white")
        L13,L14,L15,L16 = groupSets(data.win1Hand)
        data.win1Hand = L13 + L14 + L15 + L16
        for l in range(len(data.win1Hand)):
            ind3 = data.tiles.index(data.win1Hand[l])
            img3 = getSmallTile(data,ind3)
            x6 = 195 + smallW*l
            y6 = 265
            x7 = x6 + smallW
            y7 = y6 + smallH
            xw1,yw1 = (x6+x7)//2,(y6+y7)//2
            canvas.create_image(xw1,yw1,image=img3)

##############################################################################
# Citation for inspiration behind "backtracking" method:
# https://stackoverflow.com/questions/4937771/mahjong-winning-hand-algorithm#
# Also huge help from Abhi!