# This file, pong.py, defines the functions needed to determine if a player
# can pong. It also draws the pong messages for the user along for the AI's.

##############################################################################

def isPong(L,givenTile):
    if L.count(givenTile) >= 2:
        return True

def isPlayerPong(data):
    if data.nextPlayer != 'cp1' and isPong(data.playerHand,data.throw) == True \
    and data.playerDec == False and data.alreadyP == False:
        data.p1Chi = False
        data.p1Pong = True
        return True
    else:
        return False

def isCp1Pong(data):
    if data.cp1 == False and data.nextPlayer != 'cp2' and \
    isPong(data.cp1Inc,data.throw) == True and data.already1 == False:
        data.pong1 = True
        return True
    else:
        return False

def isCp2Pong(data):
    if data.cp2 == False and data.nextPlayer != 'cp3' and \
    isPong(data.cp2Inc,data.throw) == True and data.already2 == False:
        data.pong2 = True
        return True
    else:
        return False

def isCp3Pong(data):
    if data.cp3 == False and data.nextPlayer != 'player' and \
    isPong(data.cp3Inc,data.throw) == True and data.already3 == False:
        data.pong3 = True
        return True
    else:
        return False

def pongRedrawAll(canvas,data):
    if data.p1Pong and data.playerDec == False:
        canvas.create_text(data.width//2,data.height//2, text="Pong?",\
        font = "BrushScriptMT 20", fill = "white")
        canvas.create_text(data.width//2, data.height//2 + 50, \
        text = "Click tiles to pong!", font = "BrushScriptMT 20", fill = "white")
    if data.pong1:
        canvas.create_rectangle(550,200,550+20,200+20,fill='grey')
        canvas.create_text((550+570)//2,(200+220)//2,text="PONG!",fill='white')
    if data.pong2:
        canvas.create_rectangle(200,75,200+20,75+20,fill='grey')
        canvas.create_text((200+220)//2,(75+95)//2,text="PONG!",fill='white')
    if data.pong3:
        canvas.create_rectangle(100,100,100+20,100+20,fill='grey')
        canvas.create_text((100+120)//2,(100+120)//2,text="PONG!",fill='white')
