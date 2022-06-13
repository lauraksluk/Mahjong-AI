# This file, startScreen.py, draws the start screen of the game. It also
# controls the user's mouse presses to naviagate through the start and
# help screen.

###################################################################

def startScreenMousePressed(event,data):
    if 100<event.x<250 and 350<event.y<450:
        data.mode = 'play game'
    elif 350<event.x<500 and 350<event.y<450:
        data.mode = 'help screen'

def startScreenRedrawAll(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill='PeachPuff4')
    canvas.create_text(data.width//2,data.height//8,text='WELCOME TO MAHJONG!',\
    font='Monaco 37 bold',fill='white')
    canvas.create_image(data.width//2,data.height/2.5,image=data.mahjong)
    canvas.create_rectangle(100,350,250,450,outline='PeachPuff4',fill='PeachPuff3')
    canvas.create_text((100+250)//2,(350+450)//2,text='PLAY',font='Monaco 30')
    canvas.create_rectangle(350,350,500,450,outline='PeachPuff4',fill='PeachPuff3')
    canvas.create_text((350+500)//2,(350+450)//2,text='HELP',font='Monaco 30')
