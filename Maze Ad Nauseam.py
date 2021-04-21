from tkinter import *
import math

class Window(Frame):
    #I have no idea what this does but google said I needed it
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        
def createlists():
    #creates global lists which will be used for various purposes
    global WidgetList
    global BoxList
    global ArrowKeys
    WidgetList=[]
    BoxList=[]
    ArrowKeys=[0, 0, 0, 0]  
def menuscreen():
    #clears widgets
    clearwidgets()
    
    #these global variables are set to false as exiting the game leads to here, and these being false stops game functions from running
    global RunTimer
    global GameWon
    global RunPhysics
    RunTimer=False
    GameWon=False
    RunPhysics=False
    
    #creates a text widget containing the title
    T = Text(root, height=5)
    T.insert(INSERT, "                        Maze Ad Nauseam")
    T.pack()
    
    #creates buttons which run the functions displayhelp and choosedifficulty when clicked
    B1 = Button(root, command=displayhelp, text ="Help")
    B1.pack(padx=145, side=LEFT)
    B2 = Button(root, command=choosedifficulty, text ="Start")
    B2.pack(side=LEFT)
    
    #extends the list with the added widgets so that they can be removed
    WidgetList.extend([T, B1, B2]) 

def displayhelp():
    #clears all widgets and displays a text, as well as creating a button leading back to the menuscreen
    
    clearwidgets()
    
    T = Text(root, height=8, wrap=WORD)
    T.insert(INSERT, "Welcome to Maze Ad Nauseam, the goal is to complete the maze as fast as possible. ")
    T.insert(INSERT, "You can move the dark green box through the mazes using the 4 arrow keys, ")
    T.insert(INSERT, "but you cannot move through the black areas. In addition, black areas slows you down. ")
    T.insert(INSERT, "You complete a maze by making the dark green box touch a light green box. ")
    T.insert(INSERT, "Start the game by selecting one of the three difficulties: easy, medium, or hard. ")
    T.insert(INSERT, "Easy presents you with a maze of size 10x10, medium 15x15, and hard 20x20. ")    
    T.pack()
    
    B1 = Button(root, command=menuscreen, text ="Back")
    B1.pack(padx=230, side=LEFT)
    
    #extends the list with the added widgets so that they can be removed
    WidgetList.extend([T, B1]) 

def choosedifficulty():
    #clears all widgets
    clearwidgets()
    
    #doing "lambda:" is necessary because otherwise you cannot use any parameters in the function
    #the number parameter decides how large the grid for the maze is (currently hardcoded as no system for randomizing mazes exist)
    B1 = Button(root, command=lambda: startgame(10), text ="Easy")
    B1.pack(padx=90, side=LEFT)
    B2 = Button(root, command=lambda: startgame(15), text ="Medium")
    B2.pack(padx=0, side=LEFT)
    B3 = Button(root, command=lambda: startgame(20), text ="Hard")
    B3.pack(padx=90, side=LEFT)
    
    #extends the list with the added widgets so that they can be removed
    WidgetList.extend([B1, B2, B3]) 

def startgame(Difficulty):
    #clears widgets and then creates widgets for game elements
    clearwidgets()
    
    #creates a canvas containing a timer as well as a button for exiting the game
    GameOptions = Canvas(root, bg = "gray", height = 100, width = 500)
    GameOptions.pack(side=TOP)  
    B1 = Button(GameOptions, command=menuscreen, text ="Quit")
    B1.place(x=50, y=44)
    Timer = Label(GameOptions, font=("Courier", 30, 'bold'), bg="dark green", fg="white", bd =30)
    Timer.place(x=100, y=0)  
    
    #creates a canvas containing the player sprite as well as space for boxes to be drawn as obstacles
    GameCanvas = Canvas(root, bg = "gray", height = 500, width = 500)
    GameCanvas.pack(side=TOP)
    Sprite = Canvas(GameCanvas, bg = "green", height = 16, width = 16)
    Sprite.place(x=246, y=480)
    
    #extends the list with the added widgets so that they can be removed
    WidgetList.extend([GameCanvas, GameOptions, Sprite, B1, Timer]) 
    
    #setup creates a list containing lists containing 0s to make possible for a coordinate system according to Difficulty
    #generate fills the created list with coordinates for a maze according to Difficulty
    #print draws the maze on the GameCanvas
    boxlistsetup(Difficulty)
    boxlistgenerate(Difficulty)
    boxlistprint(GameCanvas)
    
    #tracks keypresses and releases, to know when arrow keys are pressed during gameplay
    root.bind("<KeyPress>", keydown)
    root.bind("<KeyRelease>", keyup)    
    
    #creates global variables for the timer and then starts the timer
    global RunTimer
    global RunPhysics
    global Sec
    global Min
    global Hour
    Sec = -1
    Min = 0
    Hour = 0    
    RunTimer=True   
    RunPhysics=True
    gametimer(Timer)
    
    #starts the physics engine
    Sprite.after(33, lambda : physics(4/Difficulty, Sprite, GameCanvas, 0, 0))

def boxlistsetup(Difficulty):
    #fills the boxlist with a number of lists equal to "Difficulty", then fills each of those lists with the same number of lists.
    #in effect, these lists can be used as a grid of X and Y coordinates, where the X coordinate is the placement of the parent lists
    #and the Y coordinate is the placement of the lists nested inside of the parent list
    BoxList.clear()
    for Xc in range(0, Difficulty):
        BoxList.append([])
        for Yc in range(0, Difficulty):
            BoxList[Xc].append(0)
            
    
def boxlistgenerate(Difficulty):
    if Difficulty == 10:
        BoxListGen=[
            [1, 2, 4, 6],
            [4, 6, 8],
            [0, 1, 2, 4, 8, 9],
            [4, 6],
            [1, 2, 3, 4, 6, 7, 8],
            [1, 3, 8],
            [1, 5, 6, 8],
            [3, 4, 5, 8],
            [1, 2, 3, 7, 8],
            [3, 5]]
        BoxList[3][0]=2 #sets a box to 2, meaning it is a light green box causing you to win
    elif Difficulty == 15:
        BoxListGen=[
            [2, 6, 8, 12, 14],
            [1, 2, 4, 6, 10, 12],
            [4, 6, 7, 8, 9, 10, 12, 13],
            [1, 2, 3, 4, 5, 6, 13],
            [4, 8, 9, 10, 11, 13],
            [1, 2, 4, 5, 6, 8, 11],
            [2, 6, 8, 10, 11, 12, 13, 14],
            [0, 1, 2, 4, 6, 11, 13],
            [0, 4, 6, 7, 8, 10, 11],
            [0, 2, 3, 4, 8, 13, 14],
            [0, 2, 4, 5, 7, 8, 9, 10, 11],
            [5, 6, 7, 11, 12, 13],
            [0, 2, 3, 6, 9, 12],
            [0, 3, 4, 8, 9, 11, 12, 14],
            [0, 1, 4, 5, 6, 8, 14]]
        BoxList[7][0]=2 #sets a box to 2, meaning it is a light green box causing you to win
        BoxList[13][0]=2
    else:
        BoxListGen=[
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            [0, 4, 8, 10, 14],
            [0, 2, 4, 6, 8, 10, 11, 12, 14, 16, 18],
            [0, 2, 6, 8, 12, 16, 18],
            [0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 15, 16, 18],
            [0, 4, 10, 18],
            [0, 2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            [0, 2, 4, 12, 18],
            [0, 2, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18],
            [0, 2, 6, 10, 14, 18],
            [0, 2, 3, 4, 6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            [0, 4, 8, 16],
            [0, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19],
            [0, 2, 4, 8, 10, 14, 18],
            [0, 1, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16, 17, 18],
            [0, 4, 6, 8, 10],
            [0, 2, 3, 4, 6, 8, 10, 11, 12, 14, 15, 16, 18, 19],
            [0, 2, 6, 16],
            [0, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            [0, 4]]
        BoxList[9][0]=2 #sets a box to 2, meaning it is a light green box causing you to win
    for Yc in range(Difficulty):
        for Xc in BoxListGen[Yc]:
            #works through each nested list in the BoxListGen list
            #the index of the nested list is the Y coordinate, and the values in the nested list are X coordinates
            #sets [Xc][Yc] coordinates to 1, meaning a box is there
            BoxList[Xc][Yc]=1 
    
    

def boxlistprint(GameCanvas):
    #takes the length of the boxlist to figure out how many X and Y coordinates there are
    #then it places a box image on the GameCanvas widget at the coordinates X and Y according to how many X and Y coordinates there are for every element in the boxlist
    G=len(BoxList)
    for Xc in range(0, G):
        for Yc in range(0, G):
            if BoxList[Xc][Yc] == 1:
                placebox(GameCanvas, Xc, Yc, G, "black")
            elif BoxList[Xc][Yc] == 2:
                placebox(GameCanvas, Xc, Yc, G, "light green")

def placebox(GameCanvas, Xg, Yg, G, F):
    Size=500/G #establishes how large each box in the grid is in pixels
    Xc=Xg*Size #multiplies its position in the grid with how large each box is to figure out its X coordinate in pixels
    Yc=Yg*Size #same as for Y coordinate in pixels
    C=Xc, Yc, Xc+Size, Yc, Xc+Size, Yc+Size, Xc, Yc+Size #makes a variable with the coordinates in pixels
    Box = GameCanvas.create_polygon(C, fill=F) #creates a box at those coordinates

def clearwidgets():
    #clears all widgets that are in the widgetlist
    for Widget in WidgetList:
        Widget.pack_forget()
    WidgetList.clear()
  
def keydown(event):
    #updates the list of keys pressed whenever a button is pressed to know which arrow keys are currently pressed
    if event.keysym == 'Left':
        ArrowKeys[0]=1
    elif event.keysym == 'Right':
        ArrowKeys[1]=1
    elif event.keysym == 'Up':
        ArrowKeys[2]=1
    elif event.keysym == 'Down':
        ArrowKeys[3]=1
        
def keyup(event):
    #sets the arrow keys in the list to 0 whenever a key is released to not have the arrow keys stuck as pressed
    if event.keysym == 'Left':
        ArrowKeys[0]=0
    elif event.keysym == 'Right':
        ArrowKeys[1]=0
    elif event.keysym == 'Up':
        ArrowKeys[2]=0
    elif event.keysym == 'Down':
        ArrowKeys[3]=0


def physics(Speed, Sprite, GameCanvas, VelX, VelY):
    global RunPhysics
    
    #finds the X and Y coordinate of the sprite
    Xc = Sprite.winfo_rootx() - GameCanvas.winfo_rootx() + 10 
    Yc = Sprite.winfo_rooty() - GameCanvas.winfo_rooty() + 10
    
    #adds the speed variable to the velocity of the sprite according to which arrow key is pressed
    if ArrowKeys[0] == 1:
        VelX-=Speed
    if ArrowKeys[1] == 1:
        VelX+=Speed
    if ArrowKeys[2] == 1:
        VelY-=Speed
    if ArrowKeys[3] == 1:
        VelY+=Speed
    
    #runs physics in 4 steps to prevent clipping
    for L in range(0,4):
        #adds a quarter of the velocity to the coordinate
        Xc+=(VelX/4) 
        Yc+=(VelY/4)    
        Correction=collision(Xc, Yc, VelX, VelY) #returns correction values for coordinates and speed as a list
        
        #corrects the X and Y coordinate if collision happens, and sets velocities to 0
        Xc+=Correction[0]
        Yc+=Correction[1]
        VelX=Correction[2]
        VelY=Correction[3]
        Win=Correction[4]
    
    #decreases the speed by 3% per cycle
    VelX=VelX*0.97
    VelY=VelY*0.97    
    
    #places the sprite in the updated coordinates
    Sprite.place(x=Xc-10, y=Yc-10)    
    if Win == 1:
        gamewin(GameCanvas)
    elif RunPhysics == True:
        Sprite.after(33, lambda : physics(Speed, Sprite, GameCanvas, VelX, VelY)) #reruns physics after 33ms

def collision(Xc, Yc, VelX, VelY):
    XFault=0
    YFault=0
    Win=0
    #finds how large the grid is and then how many pixels wide each grid is
    G=len(BoxList)
    P=500/G
    
    #adjusts coordinates to inbounds if they are out of bounds, and sets velocities to 0
    if Xc > 488:
        XFault-=Xc-488
        Xc=488
        VelX=0
    if Xc < 12:
        XFault-=Xc-12
        Xc=12
        VelX=0
    if Yc > 486:
        YFault-=Yc-486
        Yc=486
        VelY=0
    if Yc < 12:
        YFault-=Yc-12
        Yc=12
        VelY=0
    
    #finds the grid coordinate by dividing the coordinate by how large the grids are in pixels
    Xg=math.floor(Xc/(P))
    Yg=math.floor(Yc/(P))
    if BoxList[Xg][Yg] == 1: #if the grid coordinate contains a box
        
        Dist=["","","",""] #distance to the next grid down, right, up, and left
        Dist[0]= ((Yg+1)*P)-Yc
        Dist[1]= ((Xg+1)*P)-Xc
        Dist[2]= Yc-(Yg*P)
        Dist[3]= Xc-(Xg*P)
        #copies it and sorts it to find the shortest distance to run code according to which one is the shortest
        DistCopy=Dist[:]
        DistCopy.sort()
        if Dist[0] == DistCopy[0]:          #if down is the shortest distance    
            if BoxList[Xg][Yg+1] == 1:      #if the grid down contains a box
                if Dist[3] < Dist[1]:       #push the sprite either right or left according to which distance is smallest
                    XFault-=Dist[3]         #push left according to distance
                else:
                    XFault+=Dist[1]         #push right according to distance
                VelX=0                      #set X velocity to 0 as a corner has been hit
            YFault+=(Dist[0]+1)             #push sprite down according to distance, plus one to prevent faulty rounding
            VelY=0                          #set Y velocity to 0 as a horizontal wall has been hit
            VelX=VelX/2                     #halves X velocity as a penalty to hitting a wall
        elif Dist[1] == DistCopy[0]:
            if BoxList[Xg+1][Yg] == 1:        
                if Dist[0] < Dist[2]:
                    YFault+=Dist[0]
                else:
                    YFault-=Dist[2]
                VelY=0
            XFault+=(Dist[1]+1)
            VelX=0
            VelY=VelY/2
        elif Dist[2] == DistCopy[0]:
            if BoxList[Xg][Yg-1] == 1:        
                if Dist[1] < Dist[3]:
                    XFault+=Dist[1]
                else:
                    XFault-=Dist[3]
                VelX=0
            YFault-=(Dist[2]+1)
            VelY=0
            VelX=VelX/2
        elif Dist[3] == DistCopy[0]:
            if BoxList[Xg-1][Yg] == 1:
                if Dist[2] < Dist[0]:
                    XFault-=Dist[2]
                else:
                    XFault+=Dist[0]
                VelY=0
            XFault-=(Dist[3]+1)
            VelX=0
            VelY=VelY/2
    if BoxList[Xg][Yg] == 2: #a box with the value 2 is the light green box causing you to win
        Win=1
    return [XFault, YFault, VelX, VelY, Win] #returns how far the sprite has been pushed X and Y as well as updated velocities

def gametimer(Timer):
    #every second it increments seconds and if 60 seconds has passed, a minute, and if 60 minutes has passed, an hour
    global Sec
    global Min
    global Hour    
    global RunTimer
    Sec+=1
    if Sec >= 60:
        Sec-=60
        Min+=1
    if Min >= 60:
        Min-=60
        Hour+=1
    St=Sec
    Mt=Min
    if Sec < 10:
        St="0"+str(Sec) #adds a 0 to the seconds so that it's always 2 digits long if the seconds are single digits
    if Min < 10:
        Mt="0"+str(Min) #adds a 0 to the minutes
    T=Hour,":",Mt,":",St #creates the text to display on the timer
    Timer.config(text=T) #changes the timer's text to the updated text
    if RunTimer==True: #makes sure that the timer isn't run several times at once if you return to menu screen
        Timer.after(1000, lambda : gametimer(Timer)) #runs the function after 1s
def gamewin(GameCanvas):
    global Sec
    global Min
    global Hour
    global GameWon
    # returns if GameWon is true so that the rest of the function is only run once
    if GameWon == True:
        return
    GameWon=True
    Tw = '''You win
    it took you {} hours, {} minutes, {} seconds.'''.format(Hour, Min, Sec)
    WinPopup = Label(GameCanvas, font=("Courier", 10, 'bold'), bg="blue", fg="white", bd =30, text=Tw)
    WinPopup.place(x=35, y=200)    
    WidgetList.extend([WinPopup]) #extends the list with the added widget so that they can be removed
  
#setup
#creates the tkinter window and details for it, as well as global lists that are needed later
root = Tk()
app = Window(root)
root.wm_title("Maze Ad Nauseam")
root.geometry("500x600")
createlists()
menuscreen() #creates the menu screen in the tkinter window

root.mainloop() #makes the tkinter window show up and runs a code loop in the background