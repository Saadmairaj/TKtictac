import random as rnd
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter.messagebox import *
from pygame.mixer import init, music
from TkExtra import GuiLoop
from Titlebar import TitleBar


class FrameBody(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self)
        self.py = init()
        self.tb = TitleBar(self, "TicTacToe", False)  # if enabled use self.geometry("500x325+300+200")
        self.tb.dark_mode()
        self.Load = music.load('dummy.wav')
        
        self.Move = True
        self.off = True
        self.Restarting = True
        self._Turn = 'h'
        self.Round = 1
        self.BgBlack = "black"
        self.BgWhite = "white"
        self.difficulty = "unbeatable"

        self.PlScr = 0
        self.CpScr = 0

        self.Effect = True
        self.EffectCount=0
        self.EffectCurrent = None
        self.EffectLoop=0

        self.configure(highlightbackground=self.BgWhite,highlightcolor=self.BgWhite,highlightthickness=3)
        self.title('TicTacToe')
        self.resizable(False,False)
        self.geometry("500x325+300+200")
        self.configure(bg=self.BgBlack)

        self.options = Frame(self, bg=self.BgBlack, width=150)
        self.options.config(highlightbackground=self.BgWhite,highlightcolor=self.BgWhite,highlightthickness=1)
        self.options.grid_propagate(1)
        self.options.pack(side=LEFT, fill=Y)
        self._Grid(root=self.options, row=15, col=3)
        
        self.Score=Label(self.options, text='Score', fg=self.BgWhite, bg=self.BgBlack)
        self.Score.config(font=Font(size=20,underline=True))
        self.Score.grid(row=0, columnspan=4, padx=10)

        self.Player=Label(self.options, text="Player",fg=self.BgWhite, bg=self.BgBlack)
        self.Player.grid(row=1, column=0, padx=10, sticky=SW)
        self.Computer=Label(self.options, text="Computer",fg=self.BgWhite, bg=self.BgBlack)
        self.Computer.grid(row=1, column=3, padx=10, sticky=SE)

        self.PlayerScore=Label(self.options, text='0',fg=self.BgWhite, bg=self.BgBlack)
        self.PlayerScore.grid(row=2, column=0, padx=20, sticky=NSEW)
        self.ComputerScore=Label(self.options, text='0',fg=self.BgWhite, bg=self.BgBlack)
        self.ComputerScore.grid(row=2, column=3, padx=20, sticky=NSEW)

        self.DiffLB1 = Label(self.options,fg=self.BgWhite, bg=self.BgBlack)
        self.DiffLB1.config(text="Difficulty:")
        self.DiffLB1.grid(row=9, columnspan=4,padx=10,sticky=S)

        self.DiffLB2 = Label(self.options,fg=self.BgWhite, bg=self.BgBlack)
        self.DiffLB2.config(text=self.difficulty.capitalize())
        self.DiffLB2.config(font=Font(weight="bold"))
        self.DiffLB2.grid(row=10,columnspan=4,padx=10,sticky=N)

        self.RoundLB=Label(self.options, text=("Round: {}".format(self.Round)),fg=self.BgWhite, bg=self.BgBlack)
        self.RoundLB.grid(row=5,columnspan=4,padx=10)

        self._Data = {0:None, 1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None}

        self.Draw = _drawings(self,background=self.BgBlack)
        self.Draw.pack(side=LEFT)
        self.Ai=Bot(self, difficulty=self.difficulty)
        self.Setting = Settings(self)

        self.bind("<Button-1>", self.Turn)

        self.AniLoop = GuiLoop(self, self.RandomHexCode, speed=100)
        self.Win_ChkLoop = GuiLoop(self, self.win_check, speed=100)

    def Sound_Effect(self, state=True):
        if state and self.off:
            music.play()
        else: return

    def RandomHexCode(self, whatever=None):
        r = lambda: rnd.randint(0,255)
        color = ('#%02X%02X%02X' % (r(),r(),r()))
        self.Score.configure(fg=color)
        for i in (1,2,3,4): self.Draw.itemconfig(i,fill=color)
        self.config(highlightcolor=color)

    def _Grid(self, root, row, col):
        for y in range(col):
            Grid.columnconfigure(root, y, weight=1)
        for x in range(row):
            Grid.rowconfigure(root, x, weight=1)
    
    def Turn(self, evt=None):
        if self.Restarting:
            if self.Draw.Human(evt=evt):
                self.after(615, lambda: self.Ai.Move())

    def Effects(self):
        Stop = False
        self.Move = False
        if self.EffectCount <= 5:
            if self.Effect:
                self.Draw.itemconfig(self.EffectCurrent,state='hidden')
                self.Effect=False
            else:
                self.Draw.itemconfig(self.EffectCurrent,state='normal')
                self.Effect=True
            self.EffectCount+=1
        else:
            self.EffectCount = 0
            self.after_cancel(self.EffectLoop)
            self.Move=True
            Stop = True
        if not Stop: self.EffectLoop=self.after(100,self.Effects)
        
    def win_check(self):
        for i in self.Ai._Combo:
            if self._Data[i[0]]=='X' and self._Data[i[1]]=='X' and self._Data[i[2]]=='X':
                self.CpScr+=1
                self.ComputerScore.configure(text=str(self.CpScr))
                for x,y in self.Draw._LineDic.items():
                    if i == y: self.Draw.itemconfig(x,state='normal')
                self.Move=False
                self.Restarting = False
                self.Win_ChkLoop.Pause()
                self.Restart(win=True)
                return True
            if self._Data[i[0]]=='O' and self._Data[i[1]]=='O' and self._Data[i[2]]=='O':
                self.PlScr+=1
                self.PlayerScore.configure(text=str(self.PlScr))
                for x,y in self.Draw._LineDic.items():
                    if i == y: self.Draw.itemconfig(x,state='normal')
                self.Move=False
                self.Restarting = False
                self.Win_ChkLoop.Pause()
                self.Restart(win=True)
                return True
        if None not in self._Data.values():
            self.Win_ChkLoop.Pause()
            self.Restart()
        return False
        
    def Restart(self, win = False):
        def Reset():
            self.Round+=1
            self.RoundLB.configure(text=("Round: {}".format(self.Round)))
            self.Move=True
            self.Effect = True
            self.Restarting = True
            self.EffectCount=0
            self.EffectCurrent = None
            self.EffectLoop=0
            self._Data = {0:None, 1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None}
            self.Draw.destroy()
            del self.Ai
            # self.update()
            self.Draw = _drawings(self,background=self.BgBlack,
                    highlightbackground=self.BgWhite,highlightcolor=self.BgWhite)
            self.Draw.pack(side=LEFT)
            self.Ai=Bot(self, difficulty=self.difficulty)
            self.DiffLB2.config(text=self.difficulty.capitalize())
            self.Win_ChkLoop.Play()

        if None not in self._Data.values(): self.after(1500, Reset)

        if win: self.after(1500, Reset)


class _drawings(Canvas):
    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, kwargs)
        self.master = master
        self.configure(highlightthickness=1)
        self.config(width=350, height=300)
        self.start = None
        
        # Lines
        self.create_line(125, 40, 125, 260, fill= self.master.BgWhite, width=4)
        self.create_line(215, 40, 215, 260, fill= self.master.BgWhite, width=4)
        self.create_line(50, 105, 290, 105, fill= self.master.BgWhite, width=4)
        self.create_line(50, 185, 290, 185, fill= self.master.BgWhite, width=4)

        self.L012=self.create_line(70,  70, 270,  70, fill= self.master.BgWhite, width=4, state='hidden')
        self.L345=self.create_line(70, 145, 270, 145, fill= self.master.BgWhite, width=4, state='hidden')
        self.L678=self.create_line(70, 220, 270, 220, fill= self.master.BgWhite, width=4, state='hidden')
        self.L147=self.create_line(170, 60, 170, 240, fill= self.master.BgWhite, width=4, state='hidden')
        self.L036=self.create_line( 85, 60,  85, 240, fill= self.master.BgWhite, width=4, state='hidden')
        self.L258=self.create_line(255, 60, 255, 240, fill= self.master.BgWhite, width=4, state='hidden')
        self.L048=self.create_line( 80, 60, 260, 230, fill= self.master.BgWhite, width=4, state='hidden')
        self.L246=self.create_line(260, 60,  80, 230, fill= self.master.BgWhite, width=4, state='hidden')

        self._LineDic={
            self.L012 : [0,1,2],
            self.L345 : [3,4,5],
            self.L678 : [6,7,8],
            self.L147 : [1,4,7],
            self.L036 : [0,3,6],
            self.L258 : [2,5,8],
            self.L048 : [0,4,8],
            self.L246 : [2,4,6],
                }

    def Click(self, x, y):
        if x<120 and y<100 and x> 50 and y> 40: return  50+8,  40-8, 0
        if x<210 and y<100 and x>130 and y> 40: return 135+8,  40-8, 1
        if x<290 and y<100 and x>220 and y> 40: return 220+8,  40-8, 2
        if x<120 and y<190 and x> 50 and y>120: return  50+8, 115-8, 3
        if x<210 and y<190 and x>130 and y>120: return 135+8, 115-8, 4
        if x<290 and y<190 and x>220 and y>120: return 220+8, 115-8, 5
        if x<120 and y<260 and x> 50 and y>192: return  50+8, 192-8, 6
        if x<210 and y<260 and x>130 and y>192: return 135+8, 192-8, 7
        if x<290 and y<260 and x>220 and y>192: return 220+8, 192-8, 8
        return False

    def Human(self, evt=None):
        if self.Click(evt.x, evt.y) and self.master.Move:
            x,y,p=self.Click(evt.x, evt.y)
            if self.master._Data[p] == None:
                L = self.create_text(x,y,text="◯",font=Font(size=60),fill= self.master.BgWhite,anchor=NW)
                self.master.Sound_Effect()
                self.master.EffectCurrent=L
                self.master.Effects()
                self.master._Data.update({p:"O"})
                return True


class Bot(object):
    def __init__(self, master, difficulty=None, *args, **kwargs):
        self.master = master
        self.Goonce = True
        self._Data = master._Data
        self.Draw = master.Draw
        self.diff = difficulty
        self._TryBlock = { (1,6) : 0,
                            (1,8) : 2,
                            (7,2) : 8,
                            (7,0) : 6,
                            (3,8) : 6,
                            (3,2) : 0,
                            (5,0) : 2,
                            (5,6) : 8   }
        
        self._TryBlock2 = { (5,7) : 0,
                            (1,5) : 6,
                            (1,3) : 8,
                            (3,7) : 2   }

        self._AlreadyMoved=False
        self._Combo = ( [0, 1, 2],[0, 3, 6],[0, 4, 8],
                        [1, 4, 7],[2, 5, 8],[2, 4, 6], 
                        [3, 4, 5],[6, 7, 8] )
        
        self._Poisiton = (  ( 50+11,  40-2, 0),
                            (135+11,  40-2, 1),
                            (220+11,  40-2, 2),
                            ( 50+11, 115-2, 3),
                            (135+11, 115-2, 4),
                            (220+11, 115-2, 5),
                            ( 50+11, 192-2, 6),
                            (135+11, 192-2, 7),
                            (220+11, 192-2, 8) )
        
        self._Cornors = (0, 6, 8, 2)
        self._Sides = (1, 3, 5, 7)
        self._Move = 0

    def Move(self):
        if None in self._Data.values() and self.master.Move and self.master.Restarting:
            self.master.Sound_Effect()
            
            if self.diff=="unbeatable" or self.diff=='hard':
                if self.Smart_Move(): 
                    self._AlreadyMoved = True
                    return True

            if self.diff=="unbeatable":
                if self.Block2(): 
                    self._AlreadyMoved = True
                    return True

            if self.diff=="unbeatable" or self.diff=="medium" \
            or self.diff=="hard" or self.diff=="easy":
                if self.Aggressive_Move(): 
                    self._AlreadyMoved = True
                    return True
            
            if self.diff=="unbeatable" or self.diff=="medium" or self.diff=="hard":
                if self.Defensive_Move(): 
                    self._AlreadyMoved = True
                    return True
            
            if self.diff=="unbeatable" or self.diff=="hard" or self.diff=="medium":
                if self.Block(): 
                    self._AlreadyMoved = True
                    return True

            if self.diff=="unbeatable" or self.diff=="medium" \
            or self.diff=="hard" or self.diff=="easy":
                if self.Just_Move(): 
                    self._AlreadyMoved = True
                    return True
        
        else: return False

    def Smart_Move(self):
        if self._Data[4] == None :
            x,y,p = self._Poisiton[4]
            L = self.Draw.create_text(x,y,text="╳",font=Font(size=50),fill= self.master.BgWhite,anchor=NW)
            self.master.EffectCurrent=L
            self.master.Effects()
            self._Data.update({4:"X"})
            return True
        return False

    def Aggressive_Move(self):
        for x in self._Combo:
            if self._Data[x[0]] == "X" and self._Data[x[1]] == "X" and self._Data[x[2]] == None:
                X,Y,p = self._Poisiton[x[2]]
                L = self.Draw.create_text(X,Y,text="╳",font=Font(size=50),fill= self.master.BgWhite,anchor=NW)
                self.master.EffectCurrent=L
                self.master.Effects()
                self._Data.update({p:"X"})
                return True

            elif self._Data[x[1]] == "X" and self._Data[x[2]] == "X" and self._Data[x[0]] == None:
                X,Y,p = self._Poisiton[x[0]]
                L = self.Draw.create_text(X,Y,text="╳",font=Font(size=50),fill= self.master.BgWhite,anchor=NW)
                self.master.EffectCurrent=L
                self.master.Effects()
                self._Data.update({p:"X"})
                return True

            elif self._Data[x[2]] == "X" and self._Data[x[0]] == "X" and self._Data[x[1]] == None:
                X,Y,p = self._Poisiton[x[1]]
                L = self.Draw.create_text(X,Y,text="╳",font=Font(size=50),fill= self.master.BgWhite,anchor=NW)
                self.master.EffectCurrent=L
                self.master.Effects()
                self._Data.update({p:"X"})
                return True
    
    def Defensive_Move(self):
        for x in self._Combo:
            if self._Data[x[0]] == "O" and self._Data[x[1]] == "O" and self._Data[x[2]] == None:
                X,Y,p = self._Poisiton[x[2]]
                L = self.Draw.create_text(X,Y,text="╳",font=Font(size=50),fill= self.master.BgWhite,anchor=NW)
                self.master.EffectCurrent=L
                self.master.Effects()
                self._Data.update({p:"X"})
                return True
        
            elif self._Data[x[1]] == "O" and self._Data[x[2]] == "O" and self._Data[x[0]] == None:
                X,Y,p = self._Poisiton[x[0]]
                L = self.Draw.create_text(X,Y,text="╳",font=Font(size=50),fill= self.master.BgWhite,anchor=NW)
                self.master.EffectCurrent=L
                self.master.Effects()
                self._Data.update({p:"X"})
                return True

            elif self._Data[x[2]] == "O" and self._Data[x[0]] == "O" and self._Data[x[1]] == None:
                X,Y,p = self._Poisiton[x[1]]
                L = self.Draw.create_text(X,Y,text="╳",font=Font(size=50),fill= self.master.BgWhite,anchor=NW)
                self.master.EffectCurrent=L
                self.master.Effects()
                self._Data.update({p:"X"})
                return True

    def Block(self):
        SidTmp = []
        for Con in self._Cornors:
            if self._Data[Con] == "O" and self._Data[4] == "X":
                for x in self._Sides:
                    if self._Data[x] == None: SidTmp.append(x)
                choice = rnd.choice(SidTmp)
                X,Y,p = self._Poisiton[choice]
                L = self.Draw.create_text(X,Y,text="╳",font=Font(size=50),fill= self.master.BgWhite,anchor=NW)
                self.master.EffectCurrent=L
                self.master.Effects()
                self._Data.update({p:"X"})
                return True
    
    def Block2(self):
        tmp=list(self._Data.values())
        tmp = tmp.count(None)
        for i,j in self._TryBlock.items():
            if (self._Data[i[0]]=="O") and (self._Data[i[1]]=="O") and \
            (self.Goonce) and (self._Data[j]==None) and (tmp>=6):
                X,Y,p = self._Poisiton[j]
                L = self.Draw.create_text(X,Y,text="╳",font=Font(size=50),fill= self.master.BgWhite,anchor=NW)
                self.master.EffectCurrent=L
                self.master.Effects()
                self._Data.update({p:"X"})
                self.Goonce=False
                return True

    def Just_Move(self):
        ConTmp = []
        SidTmp = []
        tmp = True
       
        for x in self._Cornors:
            for i,j in self._TryBlock2.items():
                if self._Data[i[0]]=="O" and self._Data[i[1]]=="O" \
                and self._Data[x]==None and x!=j and self.diff=="unbeatable":
                    ConTmp.append(x)
                    tmp=False
                    break
                    
        for x in self._Cornors: 
            if self._Data[x]==None and tmp:
                ConTmp.append(x)
                
        if ConTmp == []:
            for x in self._Sides:
                if self._Data[x]==None:
                    SidTmp.append(x)

            choice = rnd.choice(SidTmp)
            X,Y,p = self._Poisiton[choice]
            L = self.Draw.create_text(X,Y,text="╳",font=Font(size=50),fill= self.master.BgWhite,anchor=NW)
            self.master.EffectCurrent=L
            self.master.Effects()
            self._Data.update({p:"X"})
            SidTmp.clear()
            return True

        else:
            choice = rnd.choice(ConTmp)
            X,Y,p = self._Poisiton[choice]
            L = self.Draw.create_text(X,Y,text="╳",font=Font(size=50),fill= self.master.BgWhite,anchor=NW)
            self.master.EffectCurrent=L
            self.master.Effects()
            self._Data.update({p:"X"})
            ConTmp.clear()
            return True
        
        return False


class Settings(Toplevel):
    def __init__(self, master, *args, **kwargs):
        Toplevel.__init__(self, master)
        self._Settings = False
        self._Sound = True
        self._ColorEff = True
        self.master = master
        self.BgBlack = master.BgBlack
        self.BgWhite = master.BgWhite

        self.config(bg=self.BgBlack,highlightbackground= self.BgWhite,
                highlightcolor= self.BgWhite,highlightthickness=1)
        self.wm_overrideredirect(1)
        self.wm_overrideredirect(0)
        self.attributes('-alpha', 0.85)
        self.withdraw()

        self.master._Grid(self, 20, 40)

        # Settings
        self.SettingLB = Label(self.master.options, text="Settings", relief="groove")
        self.SettingLB.config(fg= self.BgWhite, bg="black",borderwidth=2)
        self.SettingLB.grid(row=14, columnspan=4, ipadx=10, ipady=2, pady=2)

        self.SettingLB.bind("<Enter>", lambda evt:self.SettingLB.config(bg="#3d4246"))
        self.SettingLB.bind("<Leave>", lambda evt:self.SettingLB.config(bg="black"))
        self.SettingLB.bind("<Button-1>", lambda evt:self.SettingLB.config(relief="sunken"), add="+")
        self.SettingLB.bind("<ButtonRelease-1>", lambda evt:self.SettingLB.config(relief="groove"), add="+")

        self.SettingLB.bind("<Button-1>", self.Settings, add="+")
        self.unbind("<Button-1>")

        self._Note = Label(self, text=("Note: The difficulty will change next round."))
        self._Note.config(bg="black", fg="white", font=Font(size=9))
        self._Note.grid(rowspan=1, row=9, columnspan=17, column=16)

        self.ImpLabels()


    def ImpLabels(self):
        self.LightM = Label(self,text="☀",bg="black",fg="white",relief="groove",borderwidth=2)
        self.LightM.bind("<Enter>", lambda evt:self.LightM.config(bg="#3d4246"))
        self.LightM.bind("<Leave>", lambda evt:self.LightM.config(bg="black"))
        self.LightM.bind("<Button-1>", lambda evt:self.LightM.config(relief="sunken"), add="+")
        self.LightM.bind("<ButtonRelease-1>", lambda evt:self.LightM.config(relief="groove"), add="+")
        self.LightM.bind("<Button-1>", self.Light_Mode, add="+")
        self.LightM.grid(row=1, column=1, ipadx=10, ipady=2, pady=2)

        self.DarkM = Label(self,text="☾",bg="black",fg="white",relief="groove",borderwidth=2)
        self.DarkM.bind("<Enter>", lambda evt:self.DarkM.config(bg="#3d4246"))
        self.DarkM.bind("<Leave>", lambda evt:self.DarkM.config(bg="black"))
        self.DarkM.bind("<Button-1>", lambda evt:self.DarkM.config(relief="sunken"), add="+")
        self.DarkM.bind("<ButtonRelease-1>", lambda evt:self.DarkM.config(relief="groove"), add="+")
        self.DarkM.bind("<Button-1>", self.Dark_Mode, add="+")
        self.DarkM.grid(row=2, column=1, ipadx=10, ipady=2, pady=2)

        self.Easy = Label(self,text="Easy",bg="black",fg="white",relief="groove")
        self.Easy.bind("<Enter>", lambda evt:self.Easy.config(bg="#3d4246"))
        self.Easy.bind("<Leave>", lambda evt:self.Easy.config(bg="black"))
        self.Easy.bind("<Button-1>", lambda evt:self.Easy.config(relief="sunken"), add="+")
        self.Easy.bind("<ButtonRelease-1>", lambda evt:self.Easy.config(relief="groove"), add="+")
        self.Easy.bind("<Button-1>", lambda evt: self.Difficulty("easy"), add="+")
        self.Easy.grid(row=1, column=24, ipadx=30, ipady=2, pady=2)

        self.Medium = Label(self,text="Medium",bg="black",fg="white",relief="groove")
        self.Medium.bind("<Enter>", lambda evt:self.Medium.config(bg="#3d4246"))
        self.Medium.bind("<Leave>", lambda evt:self.Medium.config(bg="black"))
        self.Medium.bind("<Button-1>", lambda evt:self.Medium.config(relief="sunken"), add="+")
        self.Medium.bind("<ButtonRelease-1>", lambda evt:self.Medium.config(relief="groove"), add="+")
        self.Medium.bind("<Button-1>", lambda evt: self.Difficulty("medium"), add="+")
        self.Medium.grid(row=2, column=24, ipadx=20, ipady=2, pady=2)

        self.Hard = Label(self,text="Hard",bg="black",fg="white",relief="groove")
        self.Hard.bind("<Enter>", lambda evt:self.Hard.config(bg="#3d4246"))
        self.Hard.bind("<Leave>", lambda evt:self.Hard.config(bg="black"))
        self.Hard.bind("<Button-1>", lambda evt:self.Hard.config(relief="sunken"), add="+")
        self.Hard.bind("<ButtonRelease-1>", lambda evt:self.Hard.config(relief="groove"), add="+")
        self.Hard.bind("<Button-1>", lambda evt: self.Difficulty("hard"), add="+")
        self.Hard.grid(row=3, column=24, ipadx=30, ipady=2, pady=2)

        self.Unbeatable = Label(self,text="Unbeatable",bg="black",fg="white",relief="groove")
        self.Unbeatable.bind("<Enter>", lambda evt:self.Unbeatable.config(bg="#3d4246"))
        self.Unbeatable.bind("<Leave>", lambda evt:self.Unbeatable.config(bg="black"))
        self.Unbeatable.bind("<Button-1>", lambda evt:self.Unbeatable.config(relief="sunken"), add="+")
        self.Unbeatable.bind("<ButtonRelease-1>", lambda evt:self.Unbeatable.config(relief="groove"), add="+")
        self.Unbeatable.bind("<Button-1>",lambda evt: self.Difficulty("unbeatable"), add="+")
        self.Unbeatable.grid(row=4, column=24, ipadx=8.5, ipady=2, pady=2)

        self.Close = Label(self,text="Close",bg="black",fg="white",relief="groove",borderwidth=2)
        self.Close.bind("<Enter>", lambda evt:self.Close.config(bg="#3d4246"))
        self.Close.bind("<Leave>", lambda evt:self.Close.config(bg="black"))
        self.Close.bind("<Button-1>", lambda evt:self.Close.config(relief="sunken"), add="+")
        self.Close.bind("<ButtonRelease-1>", lambda evt:self.Close.config(relief="groove"), add="+")
        self.Close.bind("<Button-1>",self.Settings, add="+")
        self.Close.grid(row=17, column=36, ipadx=10, ipady=2, pady=2)

        self.Sound = Label(self,text="  ♬     ✔",bg="black",fg="white",relief="groove",borderwidth=2)
        self.Sound.bind("<Enter>", lambda evt:self.Sound.config(bg="#3d4246"))
        self.Sound.bind("<Leave>", lambda evt:self.Sound.config(bg="black"))
        self.Sound.bind("<Button-1>", lambda evt:self.Sound.config(relief="sunken"), add="+")
        self.Sound.bind("<ButtonRelease-1>", lambda evt:self.Sound.config(relief="groove"), add="+")
        self.Sound.bind("<Button-1>", self.Sound_Mode, add="+")
        self.Sound.grid(row=10,column=1, ipadx=10, ipady=2, pady=2)

        self.CrlEff = Label(self,text="Color ✔",bg="black",fg="white",relief="groove",borderwidth=2)
        self.CrlEff.bind("<Enter>", lambda evt:self.CrlEff.config(bg="#3d4246"))
        self.CrlEff.bind("<Leave>", lambda evt:self.CrlEff.config(bg="black"))
        self.CrlEff.bind("<Button-1>", lambda evt:self.CrlEff.config(relief="sunken"), add="+")
        self.CrlEff.bind("<ButtonRelease-1>", lambda evt:self.CrlEff.config(relief="groove"), add="+")
        self.CrlEff.bind("<Button-1>", self.ColorEffects, add="+")
        self.CrlEff.grid(row=9,column=1, ipadx=10, ipady=2, pady=2)

        self.Help = Label(self,text="?",bg="black",fg="white",relief="groove",borderwidth=2)
        self.Help.bind("<Enter>", lambda evt:self.Help.config(bg="#3d4246"))
        self.Help.bind("<Leave>", lambda evt:self.Help.config(bg="black"))
        self.Help.bind("<Button-1>", lambda evt:self.Help.config(relief="sunken"), add="+")
        self.Help.bind("<ButtonRelease-1>", lambda evt:self.Help.config(relief="groove"), add="+")
        self.Help.bind("<Button-1>", self._Help, add="+")
        self.Help.grid(row=1,column=39, ipadx=10, ipady=2, pady=2)

    def Settings(self, evt=None):
        if not self._Settings:
            geo = "400"+"x"+"200"+"+"+str(self.master.winfo_rootx()+50)+'+'+str(self.master.winfo_rooty()+70)
            self.lift()
            self.geometry(geo)
            self.deiconify()
            self.update_idletasks()
            self.grab_set()
            self._Settings = True
        else:
            self.withdraw()
            self.master.grab_set()
            self.update_idletasks()
            self._Settings = False
    
    def Light_Mode(self, evt=None):
        self.master.tb.light_mode()
        self.config(bg='white',highlightbackground="black",highlightcolor="black")
        self.master.config(bg='white',highlightbackground="black",highlightcolor="black")
        self.master.options.config(bg='white',highlightbackground="black",highlightcolor="black")
        for i in self.master.options.winfo_children():i.config(fg="black", bg="white")
        for i in self.winfo_children(): i.config(fg="black", bg="white")
        for i in range(1,25): self.master.Draw.itemconfig(i, fill='black')
        self.master.Draw.config(bg='white',highlightbackground="black",highlightcolor="black")
        self.SettingLB.bind("<Leave>", lambda evt:self.SettingLB.config(bg="white"))
        self.LightM.bind("<Leave>", lambda evt:self.LightM.config(bg="white"))
        self.DarkM.bind("<Leave>", lambda evt:self.DarkM.config(bg="white"))
        self.Easy.bind("<Leave>", lambda evt:self.Easy.config(bg="white"))
        self.Medium.bind("<Leave>", lambda evt:self.Medium.config(bg="white"))
        self.Hard.bind("<Leave>", lambda evt:self.Hard.config(bg="white"))
        self.Unbeatable.bind("<Leave>", lambda evt:self.Unbeatable.config(bg="white"))
        self.Sound.bind("<Leave>", lambda evt:self.Sound.config(bg="white"))
        self.Close.bind("<Leave>", lambda evt:self.Close.config(bg="white"))
        self.CrlEff.bind("<Leave>", lambda evt:self.CrlEff.config(bg="white"))
        self.Help.bind("<Leave>", lambda evt:self.Help.config(bg="white"))
        self.master.BgBlack = "white"
        self.master.BgWhite = "black"
    
    def Dark_Mode(self, evt=None):
        self.master.tb.dark_mode()
        self.config(bg='black',highlightbackground="white",highlightcolor="white")
        self.master.config(bg='black',highlightbackground="white",highlightcolor="white")
        self.master.options.config(bg='black',highlightbackground="white",highlightcolor="white")
        for i in self.master.options.winfo_children(): i.config(fg="white", bg="black")
        for i in self.winfo_children(): i.config(fg="white", bg="black")
        for i in range(1,25): self.master.Draw.itemconfig(i, fill='white') 
        self.master.Draw.config(bg='black',highlightbackground="white",highlightcolor="white")
        self.SettingLB.bind("<Leave>", lambda evt:self.SettingLB.config(bg="black"))
        self.LightM.bind("<Leave>", lambda evt:self.LightM.config(bg="black"))
        self.DarkM.bind("<Leave>", lambda evt:self.DarkM.config(bg="black"))
        self.Easy.bind("<Leave>", lambda evt:self.Easy.config(bg="black"))
        self.Medium.bind("<Leave>", lambda evt:self.Medium.config(bg="black"))
        self.Hard.bind("<Leave>", lambda evt:self.Hard.config(bg="black"))
        self.Unbeatable.bind("<Leave>", lambda evt:self.Unbeatable.config(bg="black"))
        self.Sound.bind("<Leave>", lambda evt:self.Sound.config(bg="black"))
        self.Close.bind("<Leave>", lambda evt:self.Close.config(bg="black"))
        self.CrlEff.bind("<Leave>", lambda evt:self.CrlEff.config(bg="black"))
        self.Help.bind("<Leave>", lambda evt:self.Help.config(bg="black"))
        self.master.BgBlack = "black"
        self.master.BgWhite = "white"
    
    def Sound_Mode(self, evt=None): 
        if self._Sound:
            self.Sound.config(text="  ♬     ✕")
            self.master.off = False
            self._Sound=False
        else:
            self.Sound.config(text="  ♬     ✔")
            self.master.off = True
            self._Sound=True
    
    def Difficulty(self, dif): 
        self.master.difficulty = dif

    def ColorEffects(self, evt=None):
        if self._ColorEff:
            self.master.AniLoop.Pause()
            self.CrlEff.config(text="Color ✕")
            if self.cget('bg')=="black":
                for i in (1,2,3,4): self.master.Draw.itemconfig(i,fill="white")
                self.master.Score.config(fg="white", bg="black")
                self.master.config(highlightcolor="white")
            else:
                for i in (1,2,3,4): self.master.Draw.itemconfig(i,fill="black")
                self.master.Score.config(fg="black", bg="white")
                self.master.config(highlightcolor="black")
            self._ColorEff = False
        else:
            if self.cget('bg')=="black":
                self.master.config(highlightcolor="white")
                self.master.Score.config(fg="white", bg="black")
            else:
                self.master.config(highlightcolor="black")
                self.master.Score.config(fg="black", bg="white")
            self.CrlEff.config(text="Color ✔")
            self.master.AniLoop.Play()
            self._ColorEff = True

    def _Help(self, evt=None):
        showinfo("Help",message="""
                        TIC-TAC-TOE
                    
                Version 1.20
                Make (7 Dec'18)
                    
                Developer: Saad Mairaj
                  Saadmairaj@yahoo.in
                    """)


if __name__ == "__main__":
    App = FrameBody()
    App.mainloop()
