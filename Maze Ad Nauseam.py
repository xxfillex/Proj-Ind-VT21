from tkinter import *
import math

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

def displayhelp():
    clearwidgets()
    T = Text(root, height=5)
    T.insert(INSERT, "This is a help screen")
    T.pack(padx=5, pady=5)
    B1 = Button(root, command=menuscreen, text ="Back")
    B1.pack(padx=230, side=LEFT)
    WidgetList.extend([T, B1])

def choosedifficulty():
    clearwidgets()
    B1 = Button(root, command=lambda: startgame(10), text ="Easy")
    B1.pack(padx=90, side=LEFT)
    B2 = Button(root, command=lambda: startgame(15), text ="Medium")
    B2.pack(padx=0, side=LEFT)
    B3 = Button(root, command=lambda: startgame(20), text ="Hard")
    B3.pack(padx=90, side=LEFT)
    WidgetList.extend([B1, B2, B3])

def startgame(Difficulty):
    clearwidgets()
    
    GameOptions = Canvas(root, bg = "gray", height = 100, width = 500)
    GameOptions.pack(side=TOP)    
    GameCanvas = Canvas(root, bg = "gray", height = 500, width = 500)
    GameCanvas.pack(side=TOP)
    Sprite = Canvas(GameCanvas, bg = "green", height = 16, width = 16)
    Sprite.place(x=246, y=480)
    
    WidgetList.extend([GameCanvas, GameOptions])
    boxlistsetup(Difficulty)
    boxlistgenerate()
    boxlistprint(GameCanvas)
    root.bind("<KeyPress>", keydown)
    root.bind("<KeyRelease>", keyup)    
    
    Sprite.after(33, lambda : physics(4/Difficulty, Sprite, GameCanvas, 0, 0))

def boxlistsetup(Difficulty):
    for Xc in range(0, Difficulty):
        BoxList.append([])
        for Yc in range(0, Difficulty):
            BoxList[Xc].append(0)
            
    
def boxlistgenerate():
    BoxList[0][0]=1
    BoxList[2][2]=1
    BoxList[3][3]=1
    BoxList[3][4]=1
    BoxList[9][9]=1

def boxlistprint(GameCanvas):
    G=len(BoxList)
    for Xc in range(0, G):
        for Yc in range(0, G):
            if BoxList[Xc][Yc] == 1:
                placebox(GameCanvas, Xc, Yc, G)

def clearwidgets():
    for Widget in WidgetList:
        Widget.pack_forget()
    WidgetList.clear()

def menuscreen():
    clearwidgets()
    T = Text(root, height=5)
    T.insert(INSERT, "                        Maze Ad Nauseam")
    T.pack()
    
    B1 = Button(root, command=displayhelp, text ="Help")
    B1.pack(padx=145, side=LEFT)
    B2 = Button(root, command=choosedifficulty, text ="Start")
    B2.pack(side=LEFT)
    WidgetList.extend([T, B1, B2])
    
def keydown(event):
    if event.keysym == 'Left':
        ArrowKeys[0]=1
    elif event.keysym == 'Right':
        ArrowKeys[1]=1
    elif event.keysym == 'Up':
        ArrowKeys[2]=1
    elif event.keysym == 'Down':
        ArrowKeys[3]=1
        
def keyup(event):
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
    NXc=Xc
    NYc=Yc
    if ArrowKeys[0] == 1:
        VelX-=Speed
    if ArrowKeys[1] == 1:
        VelX+=Speed
    if ArrowKeys[2] == 1:
        VelY-=Speed
    if ArrowKeys[3] == 1:
        VelY+=Speed
    Fault=collision(NXc, NYc)
    NXc+=Fault[0]
    NYc+=Fault[1]
    Fault.clear()
    if NXc > 480 or NXc < 0:
        NXc=Xc
    if NYc > 476 or NYc < 0:
        NYc=Yc
    Sprite.place(x=NXc, y=NYc)    
    Sprite.after(33, lambda : physics(Speed, Sprite, GameCanvas, Velocity, Angle))

def collision(Xc, Yc):
    XFault=0
    YFault=0
    G=len(BoxList)
    P=500/G
    Xg=math.floor(Xc/(P))
    Yg=math.floor(Yc/(P))
    Xg2=math.floor((Xc+16)/(P))
    Yg2=math.floor((Yc+16)/(P))
    if BoxList[Xg][Yg] == 1:
        XFault = ((math.ceil(Xc/(P)))-(Xc/(P)))*P
        YFault = ((math.ceil(Yc/(P)))-(Yc/(P)))*P
    return [XFault, YFault]

def placebox(GameCanvas, Xg, Yg, G):
    Size=500/G
    Xc=Xg*Size
    Yc=Yg*Size
    C=Xc, Yc, Xc+Size, Yc, Xc+Size, Yc+Size, Xc, Yc+Size
    Box = GameCanvas.create_polygon(C, fill="black")


root = Tk()
app = Window(root)
root.wm_title("Maze Ad Nauseam")
root.geometry("500x600")
WidgetList=[]
BoxList=[]
ArrowKeys=[0, 0, 0, 0]
menuscreen()

root.mainloop()


