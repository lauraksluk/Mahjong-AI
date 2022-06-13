# This file, cp.py, controls the 3 AI's playing the game. The functions are
# for the AI's to determine while tile to discard every turn. It also draws
# the message designating which AI is playing at the given moment.
# Additionally, it draws each AI player's pong/chi tiles, if they do pong
# or chi.

##############################################################################

from tkinter import *
import copy
import math
import random
import string
from player import *
from pong import *
from chi import *
from win import *

def markChiSets(L,done):
    wanT,tongT,bamT,wordT = groupSets(L)
    wanT.sort()
    for i in range(len(wanT)-2):
        n = getNumberFromTile(wanT[i])
        if wanT[i] in L and ('wan'+str(n+1)) in L and ('wan'+str(n+2)) in L:
            done += [wanT[i],'wan'+str(n+1),'wan'+str(n+2)]
            L.remove(wanT[i])
            L.remove('wan'+str(n+1))
            L.remove('wan'+str(n+2))
    tongT.sort()
    for j in range(len(tongT)-2):
        m = getNumberFromTile(tongT[j])
        if tongT[j] in L and ('tong'+str(m+1)) in L and ('tong'+str(m+2)) in L:
            done += [tongT[j],'tong'+str(m+1),'tong'+str(m+2)]
            L.remove(tongT[j])
            L.remove('tong'+str(m+1))
            L.remove('tong'+str(m+2))
    bamT.sort()
    for k in range(len(bamT)-2):
        p = getNumberFromTile(bamT[k])
        if bamT[k] in L and ('bam'+str(p+1)) in L and ('bam'+str(p+2)) in L:
            done += [bamT[k],'bam'+str(p+1),'bam'+str(p+2)]
            L.remove(bamT[k])
            L.remove('bam'+str(p+1))
            L.remove('bam'+str(p+2))
    return done,L

def markPongSets(done,copyL):
    temp = copy.deepcopy(copyL)
    for t in temp:
        if temp.count(t) >= 3:
            if copyL.count(t) >= 3:
                done += [t,t,t]
                index = copyL.index(t)
                copyL.pop(index)
                copyL.pop(index)
                copyL.pop(index)
    return done,copyL

def markAlmostSets(L):
    almost = []
    wanS, tongS, bamS, wordS = groupSets(L)
    wanS.sort()
    for i in range(len(wanS)-1):
        n = getNumberFromTile(wanS[i])
        if wanS[i] in L and ('wan'+str(n+1)) in L:
            almost += [wanS[i],'wan'+str(n+1)]
            L.remove(wanS[i])
            L.remove('wan'+str(n+1))
        elif L.count(wanS[i]) == 2:
            almost += [wanS[i],wanS[i]]
            L.remove(wanS[i])
            L.remove(wanS[i])
    tongS.sort()
    for j in range(len(tongS)-1):
        m = getNumberFromTile(tongS[j])
        if tongS[j] in L and ('tong'+str(m+1)) in L:
            almost += [tongS[j],'tong'+str(m+1)]
            L.remove(tongS[j])
            L.remove('tong'+str(m+1))
        elif L.count(tongS[j]) == 2:
            almost += [tongS[j],tongS[j]]
            L.remove(tongS[j])
            L.remove(tongS[j])
    bamS.sort()
    for k in range(len(bamS)-1):
        p = getNumberFromTile(bamS[k])
        if bamS[k] in L and ('bam'+str(p+1)) in L:
            almost += [bamS[k],('bam'+str(p+1))]
            L.remove(bamS[k])
            L.remove('bam'+str(p+1))
        elif L.count(bamS[k]) == 2:
            almost +=[bamS[k],bamS[k]]
            L.remove(bamS[k])
            L.remove(bamS[k])
    wordS.sort()
    for l in range(len(wordS)):
        if L.count(wordS[l]) == 2:
            almost += [wordS[l],wordS[l]]
            L.remove(wordS[l])
            L.remove(wordS[l])
    return almost,L


def compIncSets(L):
    done,lst = markChiSets(copy.deepcopy(L),[])
    complete,non = markPongSets(done,lst)
    almost,non = markAlmostSets(non)
    return complete,non,almost

def hasConsecutiveTiles(L):
    for i in range(len(L)-2):
        n = getNumberFromTile(L[i])
        if n + 1 == int(L[i+1][-1]) and n + 2 == int(L[i+2][-1]):
            return True
    return False

def addChiToComplete(complete,left,L):
    for i in range(len(L)-2):
        n = getNumberFromTile(L[i])
        if n + 1 == int(L[i+1][-1]) and n + 2 == int(L[i+2][-1]):
            if L[i] in left and L[i+1] in left and L[i+2] in left:
                left.remove(L[i])
                left.remove(L[i+1])
                left.remove(L[i+2])
                complete += [L[i],L[i+1],L[i+2]]
    return complete,left

def addPongToComplete(complete,left,L):
    for t in L:
        if L.count(t) >= 3:
            if left.count(t) >= 3:
                complete += [t,t,t]
                indInLeft = left.index(t)
                left.pop(indInLeft)
                left.pop(indInLeft)
                left.pop(indInLeft)
    return complete,left

def cpThrow(data,complete,leftover,newTile):
    data.playerDec = False
    leftover.append(newTile)
    if '' in leftover:
        leftover.remove('')
    wanTemp,tongTemp,bamTemp,wordTemp = groupSets(leftover)
    wanTemp.sort(),tongTemp.sort(),bamTemp.sort(),wordTemp.sort()
    for c in wordTemp:
        if wordTemp.count(c) == 1:
            throw = c
    if hasConsecutiveTiles(wanTemp):
        addChiToComplete(complete,leftover,wanTemp)
        throw = random.choice(leftover)
    if hasConsecutiveTiles(tongTemp):
        addChiToComplete(complete,leftover,tongTemp)
        throw = random.choice(leftover)
    if hasConsecutiveTiles(bamTemp):
        addChiToComplete(complete,leftover,bamTemp)
        throw = random.choice(leftover)
    elif leftover.count(newTile) >= 3:
        addPongToComplete(complete,leftover,wanTemp)
        addPongToComplete(complete,leftover,tongTemp)
        addPongToComplete(complete,leftover,bamTemp)
        addPongToComplete(complete,leftover,wordTemp)
        throw = random.choice(leftover)
    else:
        throw = random.choice(leftover)
    return throw

def cp1Throw(data,new=''):
    if isCp1Chi(data) == False and isCp1Pong(data) == False:
        data.throw = cpThrow(data,data.cp1Complete,data.cp1Inc,new)
    else:
        data.throw = random.choice(data.cp1Inc)
    data.discarded.append(data.throw)
    data.cp1Hand.remove(data.throw)
    data.cp1Inc.remove(data.throw)
    data.nextPlayer = 'cp2'
    data.player,data.cp1,data.cp3 = False,False,False
    data.pong1,data.chi1 = False,False
    data.alreadyP = False
    if isPlayerPong(data):
        data.p1Pong = True
        if data.playerDec:
            data.p1Pong = False
            data.cp2 = True
    data.cp2 = True

def cp2Throw(data,new=''):
    if isCp2Chi(data) == False and isCp2Pong(data) == False:
        data.throw = cpThrow(data,data.cp2Complete,data.cp2Inc,new)
    else:
        data.throw = random.choice(data.cp2Inc)
    data.discarded.append(data.throw)
    data.cp2Hand.remove(data.throw)
    data.cp2Inc.remove(data.throw)
    data.nextPlayer = 'cp3'
    data.player,data.cp1,data.cp2 = False,False,False
    data.pong2,data.chi2 = False,False
    data.already1 = False
    if isPlayerPong(data):
        data.p1Pong = True
        if data.playerDec:
            data.p1Pong = False
            data.cp3 = True
    data.cp3 = True

def cp3Throw(data,new=''):
    if isCp2Chi(data) == False and isCp2Pong(data) == False:
        data.throw = cpThrow(data,data.cp3Complete,data.cp3Inc,new)
    else:
        data.throw = random.choice(data.cp3Inc)
    data.discarded.append(data.throw)
    data.cp3Hand.remove(data.throw)
    data.cp3Inc.remove(data.throw)
    data.nextPlayer = 'player'
    data.cp1,data.cp2,data.cp3 = False,False,False
    data.pong3,data.chi3 = False,False
    data.already2 = False
    if isPlayerPong(data):
        data.p1Pong = True
        if data.playerDec:
            data.p1Pong = False
            data.player = True
    elif isPlayerChi(data):
        data.p1Chi = True
        if data.playerDec:
            data.p1Chi = False
            data.player = True
    data.player = True

def cp1Win(data,newTile):
    hand = data.cp1Hand + data.cp1Pong + data.cp1Chi
    return isWin(hand,newTile)

def cp2Win(data,newTile):
    hand = data.cp2Hand + data.cp2Pong + data.cp2Chi
    return isWin(hand,newTile)

def cp3Win(data,newTile):
    hand = data.cp3Hand + data.cp3Pong + data.cp3Chi
    return isWin(hand,newTile)

def cp1OnTimerFired(data):
    if isCp1Chi(data) == True or isCp1Pong(data) == True:
        if cp1Win(data,data.throw):
            data.win1Hand = data.cp1Hand+data.cp1Pong+data.cp1Chi+[data.throw]
            data.win1 = True
        elif isCp1Chi(data):
            data.chi1 = True
        elif isCp1Pong(data):
            data.pong1 = True
    if data.p1Pong == False and data.p1Chi == False:
        if data.cp1 == True and data.pong1 == False and data.chi1 == False:
            if len(data.cp1Hand) == 13-len(data.cp1Pong)-len(data.cp1Chi):
                new1 = getNewTile(data)
                if cp1Win(data,new1):
                    data.win1Hand = data.cp1Hand+data.cp1Pong+data.cp1Chi+[new1]
                    data.win1 = True
                else:
                    data.cp1Hand.append(new1)
                    data.allTiles.remove(new1)
                    cp1Throw(data,new1)
        elif data.pong1:
            data.cp1Hand.remove(data.throw)
            data.cp1Pong.append(data.throw)
            data.cp1Inc.remove(data.throw)
            data.cp1Hand.remove(data.throw)
            data.cp1Pong.append(data.throw)
            data.cp1Inc.remove(data.throw)
            data.cp1Pong.append(data.discarded.pop())
            data.already1 = True
            data.cp1 = True
            cp1Throw(data)
        elif data.chi1:
            elem1,elem2 = getChiTiles(data.cp1Inc,data.throw)
            data.cp1Hand.remove(elem1)
            data.cp1Chi.append(elem1)
            data.cp1Inc.remove(elem1)
            data.cp1Hand.remove(elem2)
            data.cp1Chi.append(elem2)
            data.cp1Inc.remove(elem2)
            data.cp1Chi.append(data.discarded.pop())
            data.cp1Chi = orderHand(data.cp1Chi)
            data.already1 = True
            data.cp1 = True
            cp1Throw(data)

def cp2OnTimerFired(data):
    if isCp2Chi(data) == True or isCp2Pong(data) == True:
        if cp2Win(data,data.throw):
            data.win2Hand = data.cp2Hand+data.cp2Pong+data.cp2Chi+[data.throw]
            data.win2 = True
        elif isCp2Chi(data):
            data.chi2 = True
        elif isCp2Pong(data):
            data.pong2 = True
    if data.p1Pong == False and data.p1Chi == False:
        if data.cp2 == True and data.pong2 == False and data.chi2 == False:
            if(len(data.cp2Hand) == 13-len(data.cp2Pong)-len(data.cp2Chi)):
                new2 = getNewTile(data)
                if cp2Win(data,new2):
                    data.win2Hand = data.cp2Hand+data.cp2Pong+data.cp2Chi+[new2]
                    data.win2 = True
                else:
                    data.cp2Hand.append(new2)
                    data.allTiles.remove(new2)
                    cp2Throw(data,new2)
        elif data.pong2:
            data.cp2Hand.remove(data.throw)
            data.cp2Pong.append(data.throw)
            data.cp2Inc.remove(data.throw)
            data.cp2Hand.remove(data.throw)
            data.cp2Pong.append(data.throw)
            data.cp2Inc.remove(data.throw)
            data.cp2Pong.append(data.discarded.pop())
            data.already2 = True
            data.cp2 = True
            cp2Throw(data)
        elif data.chi2:
            elem1,elem2 = getChiTiles(data.cp2Inc,data.throw)
            data.cp2Hand.remove(elem1)
            data.cp2Chi.append(elem1)
            data.cp2Inc.remove(elem1)
            data.cp2Hand.remove(elem2)
            data.cp2Chi.append(elem2)
            data.cp2Inc.remove(elem2)
            data.cp2Chi.append(data.discarded.pop())
            data.cp2Chi = orderHand(data.cp2Chi)
            data.already2 = True
            data.cp2 = True
            cp2Throw(data)

def cp3OnTimerFired(data):
    if isCp3Chi(data) == True or isCp3Pong(data) == True:
        if cp3Win(data,data.throw):
            data.win3Hand = data.cp3Hand+data.cp3Pong+data.cp3Chi+[data.throw]
            data.win3 = True
        elif isCp3Chi(data):
            data.chi3 = True
        elif isCp3Pong(data):
            data.pong3 = True
    if data.p1Pong == False and data.p1Chi == False:
        if data.cp3 == True and data.pong3 == False and data.chi3 == False:
            if (len(data.cp3Hand) == 13-len(data.cp3Pong)-len(data.cp3Chi)):
                new3 = getNewTile(data)
                if cp3Win(data,new3):
                    data.win3Hand = data.cp3Hand+data.cp3Pong+data.cp3Chi+[new3]
                    data.win3 = True
                else:
                    data.cp3Hand.append(new3)
                    data.allTiles.remove(new3)
                    cp3Throw(data,new3)
        elif data.pong3:
            data.cp3Hand.remove(data.throw)
            data.cp3Pong.append(data.throw)
            data.cp3Inc.remove(data.throw)
            data.cp3Hand.remove(data.throw)
            data.cp3Pong.append(data.throw)
            data.cp3Inc.remove(data.throw)
            data.cp3Pong.append(data.discarded.pop())
            data.already3 = True
            data.cp3 = True
            cp3Throw(data)
        elif data.chi3:
            elem1,elem2 = getChiTiles(data.cp3Inc,data.throw)
            data.cp3Hand.remove(elem1)
            data.cp3Chi.append(elem1)
            data.cp3Inc.remove(elem1)
            data.cp3Hand.remove(elem2)
            data.cp3Chi.append(elem2)
            data.cp3Inc.remove(elem2)
            data.cp3Chi.append(data.discarded.pop())
            data.cp3Chi = orderHand(data.cp3Chi)
            data.already3 = True
            data.cp3 = True
            cp3Throw(data)

def cp1RedrawAll(canvas,data):
    canvas.create_rectangle(500,75,500+25,75+25,fill='grey')
    canvas.create_text((500+525)//2,(75+100)//2,text="CP1",fill='white')

def cp2RedrawAll(canvas,data):
    canvas.create_rectangle(120,50,120+25,50+25,fill='grey')
    canvas.create_text((120+145)//2,(50+75)//2,text="CP2",fill='white')

def cp3RedrawAll(canvas,data):
    canvas.create_rectangle(75,100,75+25,100+25,fill='grey')
    canvas.create_text((75+100)//2,(100+125)//2,text="CP3",fill='white')

def cpRedrawAll(canvas,data):
    tileW,tileH = 15,25
    for i in range(len(data.cp1Pong)):
        index0 = data.tiles.index(data.cp1Pong[i])
        img0 = getSmallTile(data,index0)
        x0 = 580
        y0 = 200 + i*tileH
        x1 = x0 + tileW
        y1 = y0 + tileH
        x1p,y1p = (x0+x1)//2,(y0+y1)//2
        canvas.create_image(x1p,y1p,image=img0)
    for j in range(len(data.cp1Chi)):
        index1 = data.tiles.index(data.cp1Chi[j])
        img1 = getSmallTile(data,index1)
        x2 = 560
        y2 = 200 + j*tileH
        x3 = x2 + tileW
        y3 = y2 + tileH
        x1c,y1c = (x2+x3)//2,(y2+y3)//2
        canvas.create_image(x1c,y1c,image=img1)
    for k in range(len(data.cp2Pong)):
        index2 = data.tiles.index(data.cp2Pong[k])
        img2 = getSmallTile(data,index2)
        x4 = 180 + k*tileW
        y4 = 10
        x5 = x4 + tileW
        y5 = y4 + tileH
        x2p,y2p = (x4+x5)//2,(y4+y5)//2
        canvas.create_image(x2p,y2p,image=img2)
    for l in range(len(data.cp2Chi)):
        index3 = data.tiles.index(data.cp2Chi[l])
        img3 = getSmallTile(data,index3)
        x6 = 350 + l*tileW
        y6 = 10
        x7 = x6 + tileW
        y7 = y6 + tileH
        x2c,y2c = (x6+x7)//2,(y6+y7)//2
        canvas.create_image(x2c,y2c,image=img3)
    for m in range(len(data.cp3Pong)):
        index4 = data.tiles.index(data.cp3Pong[m])
        img4 = getSmallTile(data,index4)
        x8 = 0
        y8 = 200 + m*tileH
        x9 = x8 + tileW
        y9 = y8 + tileH
        x3p,y3p = (x8+x9)//2,(y8+y9)//2
        canvas.create_image(x3p,y3p,image=img4)
    for n in range(len(data.cp3Chi)):
        index5 = data.tiles.index(data.cp3Chi[n])
        img5 = getSmallTile(data,index5)
        x10 = 20
        y10 = 160 + n*tileH
        x11 = x10 + tileW
        y11 = y10 + tileH
        x3c,y3c = (x10+x11)//2,(y10+y11)//2
        canvas.create_image(x3c,y3c,image=img5)
