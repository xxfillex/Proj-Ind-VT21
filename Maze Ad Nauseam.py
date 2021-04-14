from tkinter import *
import math

class Window(Frame):
    #I have no idea what this does but google said I needed it
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

def displayhelp():
    #clears all widgets and displays a text
    clearwidgets()
    
    T = Text(root, height=5)
    T.insert(INSERT, "This is a help screen")
    T.pack(padx=5, pady=5)
    B1 = Button(root, command=menuscreen, text ="Back")
    B1.pack(padx=230, side=LEFT)
    
    WidgetList.extend([T, B1]) #extends the list with the added widgets so that they can be removed

def choosedifficulty():
    #clears all widgets and then creates three buttons to choose difficulty from
    clearwidgets()
    
    B1 = Button(root, command=lambda: startgame(10), text ="Easy")
    B1.pack(padx=90, side=LEFT)
    B2 = Button(root, command=lambda: startgame(15), text ="Medium")
    B2.pack(padx=0, side=LEFT)
    B3 = Button(root, command=lambda: startgame(20), text ="Hard")
    B3.pack(padx=90, side=LEFT)
    
    WidgetList.extend([B1, B2, B3]) #extends the list with the added widgets so that they can be removed

def startgame(Difficulty):
    #clears widgets and then creates widgets for game elements
    clearwidgets()
    
    GameOptions = Canvas(root, bg = "gray", height = 100, width = 500)
    GameOptions.pack(side=TOP)    
    GameCanvas = Canvas(root, bg = "gray", height = 500, width = 500)
    GameCanvas.pack(side=TOP)
    Sprite = Canvas(GameCanvas, bg = "green", height = 16, width = 16)
    Sprite.place(x=246, y=480)
    
    WidgetList.extend([GameCanvas, GameOptions]) #extends the list with the added widgets so that they can be removed
    boxlistsetup(Difficulty)
    boxlistgenerate()
    boxlistprint(GameCanvas)
    root.bind("<KeyPress>", keydown)
    root.bind("<KeyRelease>", keyup)    
    
    Sprite.after(33, lambda : physics(4/Difficulty, Sprite, GameCanvas, 0, 0))

def boxlistsetup(Difficulty):
    #fills the boxlist with a number of lists equal to "Difficulty", then fills each of those lists with the same number of lists.
    #in effect, these lists can be used as a grid of X and Y coordinates, where the X coordinate is the placement of the parent lists
    #and the Y coordinate is the placement of the lists nested inside of the parent list
    for Xc in range(0, Difficulty):
        BoxList.append([])
        for Yc in range(0, Difficulty):
            BoxList[Xc].append(0)
            
    
def boxlistgenerate():
    #sets [X][Y] coordinates to 1, meaning a box is there
    BoxList[0][0]=1
    BoxList[2][2]=1
    BoxList[3][3]=1
    BoxList[3][4]=1
    BoxList[9][9]=1

def boxlistprint(GameCanvas):
    #takes the length of the boxlist to figure out how many X and Y coordinates there are
    #then it places a box image on the GameCanvas widget at the coordinates X and Y according to how many X and Y coordinates there are for every element in the boxlist
    G=len(BoxList)
    for Xc in range(0, G):
        for Yc in range(0, G):
            if BoxList[Xc][Yc] == 1:
                placebox(GameCanvas, Xc, Yc, G)

def clearwidgets():
    #clears all widgets that are in the widgetlist
    for Widget in WidgetList:
        Widget.pack_forget()
    WidgetList.clear()

def menuscreen():
    #clears widgets and then creates menu widgets
    clearwidgets()
    
    T = Text(root, height=5)
    T.insert(INSERT, "                        Maze Ad Nauseam")
    T.pack()
    
    B1 = Button(root, command=displayhelp, text ="Help")
    B1.pack(padx=145, side=LEFT)
    B2 = Button(root, command=choosedifficulty, text ="Start")
    B2.pack(side=LEFT)
    
    WidgetList.extend([T, B1, B2]) #extends the list with the added widgets so that they can be removed
    
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
    Xc = Sprite.winfo_rootx() - GameCanvas.winfo_rootx()
    Yc = Sprite.winfo_rooty() - GameCanvas.winfo_rooty()
    if ArrowKeys[0] == 1:
        VelX-=Speed
    if ArrowKeys[1] == 1:
        VelX+=Speed
    if ArrowKeys[2] == 1:
        VelY-=Speed
    if ArrowKeys[3] == 1:
        VelY+=Speed
    NXc=Xc+VelX
    NYc=Yc+VelY
    
    Correction=collision(NXc, NYc, VelX, VelY)
    NXc+=Correction[0]
    NYc+=Correction[1]
    VelX=Correction[2]
    VelY=Correction[3]
    Correction.clear()
    
    Sprite.place(x=NXc, y=NYc)    
    Sprite.after(33, lambda : physics(Speed, Sprite, GameCanvas, VelX, VelY))

def collision(Xc, Yc, VelX, VelY):
    XFault=0
    YFault=0
    G=len(BoxList)
    P=500/G
    Xg=math.floor(Xc/(P))
    Yg=math.floor(Yc/(P))
    if BoxList[Xg][Yg] == 1:
        
        Dist=["","","",""] #down, up, right, left
        Dist[0]= ((Yg+1)*P)-Yc
        Dist[1]= Yc-(Yg*P)
        Dist[2]= ((Xg+1)*P)-Xc
        Dist[3]= Xc-(Xg*P)
        Dist2=Dist[:]
        Dist2.sort()
        
        XFault = ((math.ceil(Xc/(P)))-(Xc/(P)))*P
        YFault = ((math.ceil(Yc/(P)))-(Yc/(P)))*P
    if Xc > 480 or Xc < 0:
        pass
    if Yc > 476 or Yc < 0:
        pass    
    return [XFault, YFault, VelX, VelY]

def placebox(GameCanvas, Xg, Yg, G):
    Size=500/G #establishes how large each box in the grid is in pixels
    Xc=Xg*Size #multiplies its position in the grid with how large each box is to figure out its X coordinate in pixels
    Yc=Yg*Size #same as for Y coordinate in pixels
    C=Xc, Yc, Xc+Size, Yc, Xc+Size, Yc+Size, Xc, Yc+Size #makes a variable with the coordinates in pixels
    Box = GameCanvas.create_polygon(C, fill="black") #creates a box at those coordinates



#setup
#creates the tkinter window and details for it, as well as global lists that are needed later
root = Tk()
app = Window(root)
root.wm_title("Maze Ad Nauseam")
root.geometry("500x600")
WidgetList=[]
BoxList=[]
ArrowKeys=[0, 0, 0, 0]
menuscreen() #creates the menu screen in the tkinter window

root.mainloop() #makes the tkinter window show up and runs a code loop in the background


