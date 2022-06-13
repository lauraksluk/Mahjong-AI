# This file, helpScreen.py, draws the instruction/help page of the game.
# It also controls the user's mouse presses to navigate through the
# start and help screen.

########################################################

def helpScreenMousePressed(event,data):
    if 0<event.x<75 and 465<event.y<500:
        data.mode = 'start screen'

def helpScreenRedrawAll(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill='tan4')
    canvas.create_text(data.width//2,50,text='INSTRUCTIONS',font='Monaco 50',fill='white')
    canvas.create_image(375,160,image=data.help1)
    canvas.create_image(100,185,image=data.help2)
    canvas.create_text(375,250,\
    text= 'The game starts off with you as the dealer!',font='Monaco 10',fill='white')
    canvas.create_text(380,265,\
    text=' You start with 14 tiles. The others start with 13.',font='Monaco 10',\
    fill='white')
    canvas.create_text(250,297,text='The goal is to create a legal hand in the shortest time.'\
    ,font='Monaco 10',fill='white')
    canvas.create_text(240,315,text='A legal hand consists of 1 pair and 4 sets of threes:',\
    font='Monaco 10',fill='white')
    canvas.create_text(260,330,text='- A set of three can be any 3 consecutive',\
    font='Monaco 10',fill='white')
    canvas.create_text(291,345,text='suits of the same kind or 3 of the same tile.',\
    font='Monaco 10',fill='white')
    canvas.create_text(236,360,text='- A pair is any 2 of the same tile.',font='Monaco 10',\
    fill='white')
    canvas.create_text(data.width//2,390,text='GAME CONTROLS',font='Monaco 15 underline',\
    fill='white')
    canvas.create_text(320,410,text='Click on a tile to discard it or select it and the tile to',\
    font='Monaco 10',fill='white')
    canvas.create_text(320,425,text='its right to pong/chi.',font='Monaco 10',fill='white')
    canvas.create_text(310,440,text='Press the spacebar to decline a pong/chi.',
    font='Monaco 10',fill='white')
    canvas.create_text(300,455,text='Press r to restart the game.',\
    font='Monaco 10',fill='white')
    canvas.create_rectangle(0,465,75,500,fill='PeachPuff3')
    canvas.create_text(75//2,(465+500)//2,text='BACK',font='Monaco 15 underline')