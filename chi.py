# This file, chi.py, defines the functions needed to determine if a player
# can chi. It also draws the chi messages for the user and the AI's.

##############################################################################

from pong import *

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
    return wanGroup,tongGroup,bambooGroup,wordGroup

def getNumberFromTile(s):
    return int(s[-1])

def getChiTiles(L,givenTile):
    n = getNumberFromTile(givenTile)
    if 'wan' in givenTile:
        return getPossibleChiTiles(L,n,'wan')
    elif 'tong' in givenTile:
        return getPossibleChiTiles(L,n,'tong')
    elif 'bam' in givenTile:
        return getPossibleChiTiles(L,n,'bam')

def getPossibleChiTiles(L,n,s):
    if (s + str(n+1)) in L and (s + str(n-1)) in L:
        elem1 = s + str(n+1)
        elem2 = s + str(n-1)
        return elem1,elem2
    elif (s + str(n-1)) in L and (s + str(n-2)) in L:
        elem1 = s + str(n-1)
        elem2 = s + str(n-2)
        return elem1,elem2
    elif (s + str(n+1)) in L and (s + str(n+2)) in L:
        elem1 = s + str(n+1)
        elem2 = s + str(n+2)
        return elem1,elem2

def getHandChiTiles(L,n,s):
    if (s + str(n+1)) in L and (s + str(n+2)) in L:
        return True
    if (s + str(n-1)) in L and (s + str(n-2)) in L:
        return True
    if (s + str(n+1)) in L and (s + str(n-1)) in L:
        return True
    else:
        return False

def isChi(L,givenTile):
    if 'wan' in givenTile:
        n = getNumberFromTile(givenTile)
        return getHandChiTiles(L,n,'wan')
    elif 'tong' in givenTile:
        m = getNumberFromTile(givenTile)
        return getHandChiTiles(L,m,'tong')
    elif 'bam' in givenTile:
        p = getNumberFromTile(givenTile)
        return getHandChiTiles(L,p,'bam')
    else:
        return False

def isPlayerChi(data):
    if data.nextPlayer == 'player' and isChi(data.playerHand,data.throw) == True \
    and data.playerDec == False and data.alreadyP == False:
        data.p1Chi = True
        return True
    else:
        return False

def isCp1Chi(data):
    if data.nextPlayer == 'cp1' and isChi(data.cp1Inc,data.throw) == True \
    and data.already1 == False:
        data.pong1 = False
        data.chi1 = True
        return True
    else:
        return False

def isCp2Chi(data):
    if data.nextPlayer == 'cp2' and isChi(data.cp2Inc,data.throw) == True \
    and data.already2 == False:
        data.pong2 = False
        data.chi2 = True
        return True
    else:
        return False

def isCp3Chi(data):
    if data.nextPlayer == 'cp3' and isChi(data.cp3Inc,data.throw) == True \
    and data.already3 == False:
        data.pong3 = False
        data.chi3 = True
        return True
    else:
        return False

def chiRedrawAll(canvas,data):
    if data.p1Chi == True and data.playerDec == False:
        canvas.create_text(data.width//2,data.height//2, text="Chi?", \
        font = "BrushScriptMT 20", fill = "white")
        canvas.create_text(data.width//2, data.height//2 + 50, \
        text = "Click tiles to Chi!", font = "BrushScriptMT 20", fill = "white")
    if data.chi1:
        canvas.create_rectangle(550,200,550+25,200+25,fill='grey')
        canvas.create_text((550+575)//2,(200+225)//2,text="CHI!",fill='white')
    elif data.chi2:
        canvas.create_rectangle(200,75,200+25,75+25,fill='grey')
        canvas.create_text((200+225)//2,(75+100)//2,text="CHI!",fill='white')
    elif data.chi3:
        canvas.create_rectangle(100,100,100+25,100+25,fill='grey')
        canvas.create_text((100+125)//2,(100+125)//2,text="CHI!",fill='white')
